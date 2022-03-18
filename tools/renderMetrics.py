import matplotlib.pyplot as plt
import pandas as pd

metrics_file_path = '../../trained/tmp/metrics.txt'
def plot_loss_and_accuracy(metrics_file_path):
    d = pd.read_json(metrics_file_path)
    l = pd.DataFrame(d['loss'])
    a = pd.DataFrame(d['accuracy'])
    l = l.dropna()
    a = a.dropna()
    fig, (m1, m2) = plt.subplots(nrows=1, ncols=2, figsize=(12,6))
    m1.set_title('Loss per episode')
    m1.set_xlabel('Episode')
    m1.set_ylabel('Loss')
    m2.set_title('Accuracy per episode')
    m2.set_xlabel('Episode')
    m2.set_ylabel('Accuracy')
    m1.plot(l, label='loss')
    m2.plot(a, label='accuracy')
    fig_path = '../../trained/tmp/loss_and_accuracy.svg'
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


plot_loss_and_accuracy(metrics_file_path)
plot_reward(metrics_file_path)