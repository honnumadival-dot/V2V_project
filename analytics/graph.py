import matplotlib.pyplot as plt
import random

x_data = []
y_data = []

plt.ion()

def show_graph(distance):

    x_data.append(len(x_data))
    y_data.append(distance)

    plt.clf()

    plt.title("Vehicle Distance Analytics")

    plt.xlabel("Time")
    plt.ylabel("Distance")

    plt.plot(x_data, y_data)

    plt.pause(0.01)