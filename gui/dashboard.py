import tkinter as tk

class Dashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("V2V Dashboard")

        self.canvas = tk.Canvas(self.root, width=600, height=300, bg="white")
        self.canvas.pack()

        self.vehicles = {}

    def update_vehicle(self, vid, distance, risk):
        x = 50 + (100 - distance) * 3
        y = 150

        color = "green"
        if risk == "WARNING":
            color = "orange"
        elif risk == "CRITICAL":
            color = "red"

        if vid in self.vehicles:
            self.canvas.coords(self.vehicles[vid], x, y, x+40, y+20)
            self.canvas.itemconfig(self.vehicles[vid], fill=color)
        else:
            rect = self.canvas.create_rectangle(x, y, x+40, y+20, fill=color)
            self.vehicles[vid] = rect

    def run(self):
        self.root.update()