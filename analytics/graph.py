import matplotlib.pyplot as plt

history = {}

def update_graph(vid, distance):
    if vid not in history:
        history[vid] = []

    history[vid].append(distance)

    if len(history[vid]) > 20:
        history[vid].pop(0)

def show_graph():
    plt.clf()

    for vid, values in history.items():
        plt.plot(values, label=f"Vehicle {vid}")

    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Distance")
    plt.title("V2V Distance Trend")

    plt.pause(0.01)