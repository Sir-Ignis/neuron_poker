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
from tensorflow.keras.callbacks import TensorBoard, Callback
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU, Flatten
from tensorflow.keras.optimizers import Adam

from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.agents import DQNAgent
from rl.core import Processor
from rl.callbacks import ModelIntervalCheckpoint, FileLogger
autoplay = True  # play automatically if played against keras-rl

window_length = 1
nb_max_start_steps = 1  # random action
train_interval = 4 # train every n steps
nb_steps_warmup = 1000  # before training starts, should be higher than start steps
nb_steps = 2000000
memory_limit = nb_steps
batch_size = 512  # items sampled from memory to train
enable_double_dqn = False

log = logging.getLogger(__name__)    
Q_VALUES = None # used so we can pass q values to processor

FILE_PATH = '../trained/tmp/'
FILE_PATH_2 = '../test/tmp/'

metrics_episodes_interval = 10 # write metrics to file every n episodes
checkpoint_steps_interval = 1000 # save checkpoints of model weights every n steps

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
        self.model.save_weights(self.filepath,overwrite=True)


def plot_metrics(metrics_file_path):
    d = pd.read_json(metrics_file_path)
    l = pd.DataFrame(d['loss'])
    a = pd.DataFrame(d['accuracy'])
    l = l.dropna()
    a = a.dropna()
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
    metrics_path = 'accuracy_and_loss.png'
    fig.savefig(FILE_PATH_2+metrics_path)

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
    bb_path = 'cumulative_bb_won.png'
    plt.savefig(FILE_PATH_2+bb_path)
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
        input_shape = self.env.observation_space
        self.model = Sequential()
        self.model.add(Dense(256, input_shape=input_shape))
        self.model.add(LeakyReLU(alpha=0.4))
        self.model.add(Dropout(0.2))
        self.model.add(BatchNormalization())
        self.model.add(Dense(256))
        self.model.add(LeakyReLU(alpha=0.3))
        self.model.add(Dropout(0.2))
        self.model.add(BatchNormalization())
        self.model.add(Dense(256))
        self.model.add(LeakyReLU(alpha=0.3))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(nb_actions, activation='sigmoid'))

        # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
        # even the metrics!
        memory = SequentialMemory(limit=memory_limit, window_length=window_length)
        policy = TrumpPolicy()
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

    def train(self, env_name, steps):
        """ Train a model """
        # initiate training loop
        timestr = time.strftime("%Y%m%d-%H%M%S") + "_" + str(env_name)
        
        log_dir = FILE_PATH+"metrics_{}".format(timestr)
        metrics = FileLogger(filepath=log_dir, interval=metrics_episodes_interval)

        ckpt_dir = FILE_PATH+"{}/ckpt".format(timestr)
        interval_checkpoints = ModelCheckpoint(filepath=ckpt_dir,interval=checkpoint_steps_interval)
        
        self.dqn.fit(self.env, nb_max_start_steps=nb_max_start_steps, nb_steps=steps, visualize=False, verbose=2,
                     start_step_policy=self.start_step_policy, callbacks=[metrics, interval_checkpoints])

        
        arch_dir = FILE_PATH+"dqn_{}_json.json".format(env_name)
        dqn_json = self.model.to_json()
        with open(arch_dir, "w") as json_file:
            json.dump(dqn_json, json_file)


        # After training is done, we save the final weights.
        weights_dir = FILE_PATH+'dqn_{}_weights.h5'.format(env_name)
        self.dqn.save_weights(weights_dir, overwrite=True)
        
        league_table = self.env.league_table
        bbg = self.env.bbg_data
        games = self.env.games
        hands = self.env.hands
        if(games < 2):
            print('Error: Less than 2 games were completed!')
        else:
            if (league_table is not None) and (league_table.size == 2):
                # games won and lost by the agent (assumes agent is at index 1)
                print('Games Won: '+str(league_table[1]))
                print("Games Lost: "+str(league_table[0]))
            plot_metrics(log_dir)
            plot_cumulative_bb(bbg)
            wr = win_rate(hands, bbg)
            print('Win rate (bb/h) = %s'%wr)
        

    def load(self, env_name):
        """Load a model"""

        # Load the architecture
        with open('dqn_{}_json.json'.format(env_name), 'r') as architecture_json:
            dqn_json = json.load(architecture_json)

        self.model = model_from_json(dqn_json)
        self.model.load_weights('dqn_{}_weights.h5'.format(env_name))

    def play(self, env_name='dqn', nb_steps=10000, render=False):
        """Let the agent play"""
        memory = SequentialMemory(limit=memory_limit, window_length=window_length)
        policy = TrumpPolicy()
        timestr = time.strftime("%Y%m%d-%H%M%S") + "_" + str(env_name)  
        
        ckpt_dir = FILE_PATH_2+"{}/ckpt".format(timestr)
        interval_checkpoints = ModelCheckpoint(filepath=ckpt_dir,interval=1000)
        nb_actions = self.env.action_space.n
        log_dir = FILE_PATH_2+"metrics_{}".format(timestr)
        metrics = FileLogger(filepath=log_dir, interval=10)

        self.dqn = DQNAgent(model=self.model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=nb_steps_warmup,
                            target_model_update=1e-2, policy=policy,
                            processor=CustomProcessor(),
                            batch_size=batch_size, train_interval=train_interval, enable_double_dqn=enable_double_dqn)
        

        self.dqn.compile(optimizer=Adam(lr=1e-4, clipnorm=1), metrics=['mae','accuracy']) # pylint: disable=no-member

        self.dqn.fit(self.env, nb_max_start_steps=nb_max_start_steps, nb_steps=nb_steps, visualize=False, verbose=2,
                     start_step_policy=self.start_step_policy, callbacks=[metrics, interval_checkpoints])

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
class TrumpPolicy(EpsGreedyQPolicy):
    """Adaptive EpsGreedyQPolicy when making decision based on neural network."""

    def __init__(self, eps=0.05):
        super(EpsGreedyQPolicy, self).__init__()
        self.eps = eps
        self.eps_warmup = 1 # 100% random actions in warm up phase to maximize exploitation
    def select_action(self, q_values):
        """Return the selected action
        # Arguments
            q_values (np.ndarray): List of the estimations of Q for each action
        # Returns
            Selection action
        """
        global Q_VALUES
        Q_VALUES = q_values.copy()
        assert q_values.ndim == 1
        nb_actions = q_values.shape[0]
        
        if np.random.uniform() < self.eps or self.agent.step < nb_steps_warmup:
            action = np.random.randint(0, nb_actions)
        else:
            action = np.argmax(q_values)
        return action

   
class CustomProcessor(Processor):
    """The agent and the environment"""

    def __init__(self):
        """initizlie properties"""
        self.legal_moves_limit = None
        self.eps = 0.05
    
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
        """Selects legal action using epsilon greedy policy"""
        if 'legal_moves_limit' in self.__dict__ and self.legal_moves_limit is not None:
            self.legal_moves_limit = [move.value for move in self.legal_moves_limit]
            if action not in self.legal_moves_limit:
                log.info('Action %s not in legal moves limit!'%action)
                global Q_VALUES
                q_values = Q_VALUES.copy()
                q_values = q_values.tolist()
                while action not in self.legal_moves_limit:
                    del q_values[action]
                    if np.random.uniform() < self.eps:
                        action = np.random.randint(0, len(q_values))
                    else:
                        action = np.argmax(q_values)
                log.info('Choosen processed action: %s'%action)
        return action
