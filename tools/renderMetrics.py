import matplotlib.pyplot as plt
import pandas as pd

def plot_loss_and_accuracy(metrics_file_path):
    d = pd.read_json(metrics_file_path)
    l = pd.DataFrame(d['loss'])
    a = pd.DataFrame(d['accuracy'])
    l = l.dropna()
    a = a.dropna()
    fig, (m1, m2) = plt.subplots(nrows=1, ncols=2, figsize=(6,3))
    #removed axis and title labels to save space
    #m1.set_title('Loss per episode')
    #m1.set_xlabel('Episode')
    #m1.set_ylabel('Loss')
    #m2.set_title('Accuracy per episode')
    #m2.set_xlabel('Episode')
    #m2.set_ylabel('Accuracy')
    m1.plot(l, label='loss')
    m2.plot(a, label='accuracy')
    fig_path = "/home/daniel/Project/trained/tmp/loss_and_accuracy.png"
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.show()


def multi_plot_loss_and_accuracy(metrics_file_path, metrics_file_path2):
    d = pd.read_json(metrics_file_path)
    l = pd.DataFrame(d['loss'])
    a = pd.DataFrame(d['accuracy'])
    l = l.dropna()
    a = a.dropna()

    d2 = pd.read_json(metrics_file_path2)
    l2 = pd.DataFrame(d2['loss'])
    a2 = pd.DataFrame(d2['accuracy'])
    l2 = l2.dropna()
    a2 = a2.dropna() 

    fig, (p1, p2, p3, p4) = plt.subplots(nrows=1, ncols=4, figsize=(12,3))
    #m1.set_title('Loss per episode')
    p1.set_xlabel('Episode')
    p1.set_ylabel('Loss')
    #m2.set_title('Accuracy per episode')
    p3.set_xlabel('Episode')
    p3.set_ylabel('Accuracy')
    p1.plot(l, label='loss')
    p2.plot(l2, label="loss")
    p3.plot(a, label='accuracy')
    p4.plot(a2, label="accuracy")
    fig_path = "/home/daniel/Project/trained/tmp/loss_and_accuracy.png"
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.show()


def plot_loss_and_accuracy_n(metrics_file_path, n):
    """ n is number of rows to select """
    d = pd.read_json(metrics_file_path)
    l = pd.DataFrame(d['loss'])
    a = pd.DataFrame(d['accuracy'])
    l = l.dropna()
    a = a.dropna()
    l = l.head(n)
    a = a.head(n)
    fig, (m1, m2) = plt.subplots(nrows=1, ncols=2, figsize=(4,3))
    m1.set_title('Loss per episode')
    m1.set_xlabel('Episode')
    m1.set_ylabel('Loss')
    m2.set_title('Accuracy per episode')
    m2.set_xlabel('Episode')
    m2.set_ylabel('Accuracy')
    m1.plot(l, label='loss')
    m2.plot(a, label='accuracy')
    fig_path = '../../trained/dqn_old_reward_equity_20_30/loss_and_accuracy.svg'
    plt.savefig(fig_path)
    plt.show()


def plot_reward(metrics_file_path):
    d = pd.read_json(metrics_file_path)
    r = pd.DataFrame(d['episode_reward'])
    fig, rplt = plt.subplots(figsize=(12,6))
    rplt.set_title('Reward per episode');
    rplt.set_xlabel('Episode')
    rplt.set_ylabel('Reward')
    rplt.plot(r, label="reward")
    fig_path = '../../trained/tmp/reward.svg'
    plt.savefig(fig_path)
    plt.show()

#plot_loss_and_accuracy_n("../../trained/dqn_old_reward_equity_20_30/metrics_20220318-213910_dqn1", 100000)
metrics_file_path  = "/home/daniel/Project/trained/DDQN_20_30_equity/metrics_20220318-094714_dqn1"
metrics_file_path2 = "/home/daniel/Project/trained/DDQN_20_30_equity_old_reward/metrics_20220319-155040_dqn1"

#multi_plot_loss_and_accuracy(metrics_file_path, metrics_file_path2)
plot_loss_and_accuracy(metrics_file_path2)