import tkinter as tk

class Dashboard:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("🚗 V2V Smart Dashboard")

        self.root.geometry("900x500")

        self.canvas = tk.Canvas(
            self.root,
            width=900,
            height=500,
            bg="black"
        )

        self.canvas.pack()

        self.vehicles = {}

    def update_vehicle(self,
                       vid,
                       distance,
                       risk):

        x = 50 + distance * 5

        y = 100 + vid * 100

        color = "green"

        if risk == "WARNING":
            color = "orange"

        elif risk == "CRITICAL":
            color = "red"

        if vid in self.vehicles:

            self.canvas.delete(
                self.vehicles[vid]
            )

        car = self.canvas.create_rectangle(
            x,
            y,
            x + 80,
            y + 40,
            fill=color
        )

        self.canvas.create_text(
            x + 40,
            y - 15,
            text=f"Vehicle {vid}",
            fill="white"
        )

        self.vehicles[vid] = car

        self.root.update()

    def run(self):
        self.root.update()