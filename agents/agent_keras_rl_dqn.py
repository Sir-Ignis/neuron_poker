"""Player based on a trained neural network"""
# pylint: disable=wrong-import-order
import logging
import time

import numpy as np

from gym_env.env import Action

import tensorflow as tf
import json
import matplotlib.pyplot as plt
import pandas as pd
import random

from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
from tensorflow.keras.optimizers import Adam

from rl.policy import GreedyQPolicy
from rl.memory import SequentialMemory
from rl.agents import DQNAgent
from rl.core import Processor
from rl.callbacks import ModelIntervalCheckpoint, FileLogger
autoplay = True  # play automatically if played against keras-rl

window_length = 1
nb_max_start_steps = 1  # random action
train_interval = 100  # train every 100 steps
nb_steps_warmup = 500  # before training starts, should be higher than start steps
nb_steps = 200000
memory_limit = int(nb_steps / 2)
batch_size = 256  # items sampled from memory to train
enable_double_dqn = False

log = logging.getLogger(__name__)    

class ModelCheckpoint(ModelIntervalCheckpoint):
    def __init__(self, filepath, interval, verbose=0):
        super(ModelIntervalCheckpoint, self).__init__()
        self.filepath = filepath
        self.interval = interval
        self.verbose = verbose
        self.total_steps = 0

    def on_step_end(self, step, logs={}):
        """ Save weights at interval steps during training"""
        self.total_steps += 1
        if self.total_steps % self.interval != 0:
            # Nothing to do.
            return

        filepath = self.filepath
        if self.verbose > 0:
            log.info('Step {}: saving model weights to {}'.format(
                self.total_steps, filepath))
        self.model.model.save_weights(self.filepath)


def plot_metrics(metrics_file_path):
    d = pd.read_json(metrics_file_path)
    l = pd.DataFrame(d['loss'])
    a = pd.DataFrame(d['accuracy'])
    l.dropna()
    a.dropna()
    fig, (m1, m2) = plt.subplots(nrows=1, ncols=2)
    m1.set_title('Loss per episode')
    m1.set_xlabel('Episode')
    m1.set_ylabel('Loss')
    m2.set_title('Accuracy per episode')
    m2.set_xlabel('Episode')
    m2.set_ylabel('Accuracy')
    m1.plot(l, label='loss')
    m2.plot(a, label='accuracy')
    plt.show()

def plot_bbg(big_blinds_data):
    plt.xlabel('Episode')
    plt.ylabel('bb/g')
    plt.title('Big Blinds Won Per Game')
    x_pos = [i for i, _ in enumerate(big_blinds_data)]
    plt.plot(x_pos, big_blinds_data, color='b')
    plt.show()

def plot_cumulative_bb(big_blinds_data):
    plt.xlabel('Episode')
    plt.ylabel('Cumulative BB won')
    plt.title('Cumulative Big Blinds Won')
    x_pos = [i for i, _ in enumerate(big_blinds_data)]
    y_pos = []
    for i in range(len(x_pos)):
        y_pos.append(sum(big_blinds_data[:i+1]))
    print("x: %s, y: %s"%(len(x_pos),len(y_pos)))
    plt.plot(x_pos, y_pos, color='b')
    plt.show()


def win_rate(number_of_hands, big_blinds_data):
    """ returns the game win rate in bb/100 """
    # winrate in bb/100 = (Profit in bb  / Number of hands) * 100
    profit_in_bb = sum(big_blinds_data)
    win_rate = (profit_in_bb / number_of_hands)
    print('hands = %s'%number_of_hands)
    print('profit in bb = %s'%profit_in_bb)
    return win_rate

class Player:
    """Mandatory class with the player methods"""

    def __init__(self, name='DQN', load_model=None, env=None):
        """Initiaization of an agent"""
        self.equity_alive = 0
        self.actions = []
        self.last_action_in_stage = ''
        self.temp_stack = []
        self.name = name
        self.autoplay = True

        self.dqn = None
        self.model = None
        self.env = env

        if load_model:
            self.load(load_model)

    def initiate_agent(self, env):
        """initiate a deep Q agent"""
        tf.compat.v1.disable_eager_execution()

        self.env = env

        nb_actions = self.env.action_space.n

        self.model = Sequential()
        self.model.add(Dense(256, input_shape=env.observation_space))
        self.model.add(LeakyReLU(alpha=0.5))
        self.model.add(Dropout(0.2))
        self.model.add(BatchNormalization())
        self.model.add(Dense(256))
        self.model.add(LeakyReLU(alpha=0.3))
        self.model.add(Dropout(0.2))
        self.model.add(BatchNormalization())
        self.model.add(Dense(256))
        self.model.add(LeakyReLU(alpha=0.3))
        self.model.add(Dropout(0.2))
        self.model.add(BatchNormalization())
        self.model.add(Dense(nb_actions, activation='sigmoid'))

        # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
        # even the metrics!
        memory = SequentialMemory(limit=memory_limit, window_length=window_length)
        policy = TrumpPolicy()

        nb_actions = env.action_space.n

        self.dqn = DQNAgent(model=self.model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=nb_steps_warmup,
                            target_model_update=1e-2, policy=policy,
                            processor=CustomProcessor(),
                            batch_size=batch_size, train_interval=train_interval, enable_double_dqn=enable_double_dqn)
        self.dqn.compile(optimizer=Adam(lr=1e-4, clipnorm=1), metrics=['mae','accuracy'])

    def start_step_policy(self, observation):
        """Custom policy for random decisions for warm up."""
        log.info("Random action")
        _ = observation
        action = self.env.action_space.sample()
        return action

    def train(self, env_name):
        """ Train a model """
        # initiate training loop
        timestr = time.strftime("%Y%m%d-%H%M%S") + "_" + str(env_name)
        
        log_dir = "./tmp/metrics_{}".format(timestr)
        metrics = FileLogger(filepath=log_dir, interval=10)

        """
        tensorboard = TensorBoard(log_dir='./Graph/train-fit/{}'.format(timestr), histogram_freq=0, write_graph=True,
                                  write_images=False)
        """

        interval_checkpoints = ModelCheckpoint(filepath='./Checkpoints/{}/ckpt'.format(timestr),interval=1000)
        
        self.dqn.fit(self.env, nb_max_start_steps=nb_max_start_steps, nb_steps=nb_steps, visualize=False, verbose=2,
                     start_step_policy=self.start_step_policy, callbacks=[metrics, interval_checkpoints])
        """
        self.dqn.fit(self.env, nb_max_start_steps=nb_max_start_steps, nb_steps=nb_steps, visualize=False, verbose=2,
                     start_step_policy=self.start_step_policy)
        # Save the architecture
        """
        dqn_json = self.model.to_json()
        with open("dqn_{}_json.json".format(env_name), "w") as json_file:
            json.dump(dqn_json, json_file)


        # After training is done, we save the final weights.
        self.dqn.save_weights('dqn_{}_weights.h5'.format(env_name), overwrite=True)

        """
        tensorboard = TensorBoard(log_dir='./Graph/train-test/{}'.format(timestr), histogram_freq=0, write_graph=True,
                                  write_images=False)
        
        # Finally, evaluate our algorithm for 10 episodes.
        self.dqn.test(self.env, nb_episodes=10, visualize=False, callbacks=[tensorboard])
        """
        
        bbg = self.env.bbg_data
        games = self.env.games
        hands = self.env.hands
        if(games == 0):
            print('Error: no games were completed!')
        else:
            plot_metrics(log_dir)
            plot_cumulative_bb(bbg)
            wr = win_rate(hands, bbg)
            print('Win rate (bb/100) = %s'%wr)
        

    def load(self, env_name):
        """Load a model"""

        # Load the architecture
        with open('dqn_{}_json.json'.format(env_name), 'r') as architecture_json:
            dqn_json = json.load(architecture_json)

        self.model = model_from_json(dqn_json)
        self.model.load_weights('dqn_{}_weights.h5'.format(env_name))

    def play(self, nb_episodes=5, render=False):
        """Let the agent play"""
        memory = SequentialMemory(limit=memory_limit, window_length=window_length)
        policy = TrumpPolicy()

        class CustomProcessor(Processor):  # pylint: disable=redefined-outer-name
            """The agent and the environment"""

            def process_state_batch(self, batch):
                """
                Given a state batch, I want to remove the second dimension, because it's
                useless and prevents me from feeding the tensor into my CNN
                """
                return np.squeeze(batch, axis=1)

            def process_info(self, info):
                processed_info = info['player_data']
                if 'stack' in processed_info:
                    processed_info = {'x': 1}
                return processed_info

        nb_actions = self.env.action_space.n

        self.dqn = DQNAgent(model=self.model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=nb_steps_warmup,
                            target_model_update=1e-2, policy=policy,
                            processor=CustomProcessor(),
                            batch_size=batch_size, train_interval=train_interval, enable_double_dqn=enable_double_dqn)
        self.dqn.compile(Adam(lr=1e-3), metrics=['mae'])  # pylint: disable=no-member

        self.dqn.test(self.env, nb_episodes=nb_episodes, visualize=render)

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        """Mandatory method that calculates the move based on the observation array and the action space."""
        _ = observation  # not using the observation for random decision
        _ = info

        this_player_action_space = {Action.FOLD, Action.CHECK, Action.CALL, Action.RAISE_POT, Action.RAISE_HALF_POT,
                                    Action.RAISE_2POT, Action.ALL_IN}
        _ = this_player_action_space.intersection(set(action_space))

        action = None
        return action

# replaced old policy
# see https://github.com/dickreuter/neuron_poker/blob/master/agents/agent_keras_rl_dqn.py#L168 for old policy
class TrumpPolicy(GreedyQPolicy):
    """Custom policy when making decision based on neural network."""

    def select_action(self, q_values):
        """Return the selected action

        # Arguments
            q_values (np.ndarray): List of the estimations of Q for each action

        # Returns
            Selection action
        """
        assert q_values.ndim == 1
        action = np.argmax(q_values)
        log.info(f"Chosen action by keras-rl {action} - q values: {q_values}")
        return action

   
class CustomProcessor(Processor):
    """The agent and the environment"""

    def __init__(self):
        """initizlie properties"""
        self.legal_moves_limit = None

    def process_state_batch(self, batch):
        """Remove second dimension to make it possible to pass it into cnn"""
        return np.squeeze(batch, axis=1)

    def process_info(self, info):
        if 'legal_moves' in info.keys():
            self.legal_moves_limit = info['legal_moves']
        else:
            self.legal_moves_limit = None
        return {'x': 1}  # on arrays allowed it seems

    def process_action(self, action):
        """Find nearest legal action"""
        if 'legal_moves_limit' in self.__dict__ and self.legal_moves_limit is not None:
            self.legal_moves_limit = [move.value for move in self.legal_moves_limit]
            if action not in self.legal_moves_limit:
                log.info('Action %s not in legal moves limit!'%action)
                for i in range(5):
                    action += i
                    if action in self.legal_moves_limit:
                        break
                    action -= i * 2
                    if action in self.legal_moves_limit:
                        break
                    action += i
                if action not in self.legal_moves_limit:
                    action = random.choice(self.legal_moves_limit)
                log.info('Choosen processed action: %s'%action)
        return action
