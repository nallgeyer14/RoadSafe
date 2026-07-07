import math

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class Gauge(QWidget):

    def __init__(self, title, min_value, max_value):
        super().__init__()

        self.title = title
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value


        self.figure = Figure(
            figsize=(3,3),
            facecolor="#111111"
        )

        self.canvas = FigureCanvasQTAgg(self.figure)


        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


        self.ax = self.figure.add_subplot(111)

        self.draw_gauge()



    def draw_gauge(self):

        self.ax.clear()

        self.ax.set_facecolor("#111111")
        self.figure.patch.set_facecolor("#111111")

        self.ax.set_xlim(-1.2,1.2)
        self.ax.set_ylim(-1.2,1.2)

        self.ax.axis("off")


        # Outer circle
        circle = self.ax.add_patch(
            __import__("matplotlib").patches.Circle(
                (0,0),
                1,
                fill=False,
                linewidth=3,
                edgecolor="white"
            )
        )


        # Tick marks
        for i in range(0,11):

            angle = math.radians(
                180 - (i * 18)
            )

            x1 = .85 * math.cos(angle)
            y1 = .85 * math.sin(angle)

            x2 = 1.0 * math.cos(angle)
            y2 = 1.0 * math.sin(angle)


            self.ax.plot(
                [x1,x2],
                [y1,y2],
                linewidth=2,
                color="white"
            )


        # Needle

        percent = (
            self.value-self.min_value
        ) / (
            self.max_value-self.min_value
        )


        angle = math.radians(
            180 - percent*180
        )


        x = .75 * math.cos(angle)
        y = .75 * math.sin(angle)


        self.ax.plot(
            [0,x],
            [0,y],
            linewidth=3,
            color="red"
        )


        # Center dot

        self.ax.scatter(
            0,
            0,
            s=80,
            color="white"
        )


        # Value

        self.ax.text(
            0,
            -.1,
            f"{self.value:.0f}",
            ha="center",
            va="center",
            fontsize=25,
            color="white"
        )


        self.ax.text(
            0,
            -.35,
            self.title,
            ha="center",
            fontsize=12,
            color="white"
        )


        self.canvas.draw()



    def update_value(self,value):

        self.value = max(
            self.min_value,
            min(value,self.max_value)
        )

        self.draw_gauge()