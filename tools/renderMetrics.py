import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
    l = l.head(3000)
    l = l.dropna()
    a = a.head(3000)
    a = a.dropna()

    d2 = pd.read_json(metrics_file_path2)
    l2 = pd.DataFrame(d2['loss'])
    a2 = pd.DataFrame(d2['accuracy'])
    l2 = l2.head(3000)
    l2 = l2.dropna()
    a2 = a2.head(3000)
    a2 = a2.dropna() 

    fig, (p1, p2) = plt.subplots(nrows=1, ncols=2, figsize=(12,3))
    p1.set_xlabel('Episode')
    p1.set_ylabel('Loss')
    p2.set_xlabel('Episode')
    p2.set_ylabel('Accuracy')
    p1.plot(l, label='loss')
    p1.plot(l2, label="loss")
    p2.plot(a, label='accuracy')
    p2.plot(a2, label="accuracy")
    fig_path = "/home/daniel/Project/trained/tmp/Combined_LA_plots.png"
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.show()


import matplotlib.ticker as mticker

class Labeloffset():
    def __init__(self,  ax, label="", axis="y"):
        self.axis = {"y":ax.yaxis, "x":ax.xaxis}[axis]
        self.label=label
        ax.callbacks.connect(axis+'lim_changed', self.update)
        ax.figure.canvas.draw()
        self.update(None)

    def update(self, lim):
        fmt = self.axis.get_major_formatter()
        self.axis.offsetText.set_visible(False)
        self.axis.set_label_text(self.label + " "+ fmt.get_offset() )



def combined_loss_plot(metrics_file_path, metrics_file_path2):
    d = pd.read_json(metrics_file_path)
    l = pd.DataFrame(d['loss'])
    l = l.dropna()

    d2 = pd.read_json(metrics_file_path2)
    l2 = pd.DataFrame(d2['loss'])
    l2 = l2.dropna()
    
    fig=plt.figure(figsize=(6,3))
    plt.rc('font', size=11)
    ax2=fig.add_subplot(111, label="1")
    ax=fig.add_subplot(111, label="2", frame_on=False)

    ax.plot(l, color="C0")
    ax.set_xlabel("episode")
    ax.tick_params(axis='x', colors="C0")
    ax.tick_params(axis='y', colors="C0")
    ax.set_ylabel("loss", color="C0")

    """
    ymin, ymax = ax.get_ylim()
    # shift the graph up adjust the y_tick labels
    ax.set_ylim(-ymax,ymax)
    step_size = 10e3
    ax.set_yticks(np.arange(0, ymax, step_size))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(-3,3), useMathText=True)
    """

    ax2.plot(l2, color="C1")
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()  
    ax2.xaxis.set_label_position('top') 
    ax2.yaxis.set_label_position('right') 
    ax2.set_ylabel("loss", color="C1")
    ax2.tick_params(axis='x', colors="C1")
    ax2.tick_params(axis='y', colors="C1")

    """
    # adjust the y_tick labels
    ymin, ymax = ax2.get_ylim()
    step_size = 1000
    ax2.set_yticks(np.arange(0, ymax, step_size))
    ax2.ticklabel_format(style='sci', axis='y', scilimits=(-3,3), useMathText=True)
    """
    #move scaling labeling to y-axis
    formatter = mticker.ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3,3))
    ax.yaxis.set_major_formatter(formatter)
    Labeloffset(ax, label="loss", axis="y")

    formatter2 = mticker.ScalarFormatter(useMathText=True)
    formatter2.set_powerlimits((-3,3))
    ax2.yaxis.set_major_formatter(formatter2)
    Labeloffset(ax2, label="loss", axis="y")


    fig_path = "/home/daniel/Project/trained/tmp/combined_loss_plot.png"
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.show()

def combined_accuracy_plot(metrics_file_path, metrics_file_path2):
    d = pd.read_json(metrics_file_path)
    a = pd.DataFrame(d['accuracy'])
    a = a.dropna()

    d2 = pd.read_json(metrics_file_path2)
    a2 = pd.DataFrame(d2['accuracy'])
    a2 = a2.dropna()
    
    fig=plt.figure(figsize=(6,3))
    plt.rc('font', size=11)
    ax=fig.add_subplot(111, label="1")
    ax2=fig.add_subplot(111, label="2", sharey=ax, frame_on=False)

    ax.plot(a, color="C0")
    ax.set_xlabel("episode")
    ax.tick_params(axis='x', colors="C0")
    ax.tick_params(axis='y', colors="C0")
    ax.set_ylabel("accuracy")

    ax2.plot(a2, color="C1")
    ax2.xaxis.tick_top()
    #ax2.yaxis.tick_right()  
    ax2.xaxis.set_label_position('top') 
    #ax2.yaxis.set_label_position('right') 
    #ax2.set_ylabel("accuracy", color="C1")
    ax2.tick_params(axis='x', colors="C1")

    fig_path = "/home/daniel/Project/trained/tmp/combined_accuracy_plot.png"
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.show()



def la_multi_plot(metrics_file_path, metrics_file_path2):
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
    p1.plot(l, label="loss")
    p1.set_xlabel('episode')
    p1.set_ylabel("loss")
    p1.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
    p2.plot(a, label="accuracy")
    p2.set_xlabel("episode")
    p2.set_ylabel("accuracy")
    p3.plot(l2, label="loss ")
    p3.set_xlabel('episode')
    p3.set_ylabel("loss")
    p3.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
    p4.plot(a2, label="accuracy")
    p4.set_xlabel("episode")
    p4.set_ylabel("accuracy")
    fig_path = "/home/daniel/Project/trained/tmp/LA_combined_plot_scaled.png"
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
    rplt.set_title('Reward per episode')
    rplt.set_xlabel('Episode')
    rplt.set_ylabel('Reward')
    rplt.plot(r, label="reward")
    fig_path = '../../trained/tmp/reward.svg'
    plt.savefig(fig_path)
    plt.show()

metrics_file_path  = "/home/daniel/Project/trained/DDQN_20_30_equity/metrics_20220318-094714_dqn1"
metrics_file_path2 = "/home/daniel/Project/trained/DDQN_20_30_equity_old_reward/metrics_20220319-155040_dqn1"

#combined_loss_plot(metrics_file_path, metrics_file_path2)
combined_accuracy_plot(metrics_file_path, metrics_file_path2)
