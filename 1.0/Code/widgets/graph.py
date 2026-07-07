from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class VehicleGraph(QWidget):

    def __init__(self):
        super().__init__()

        self.figure = Figure(
            figsize=(8,4),
            facecolor="#050505"
        )

        self.canvas = FigureCanvasQTAgg(
            self.figure
        )

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


        self.ax_speed = self.figure.add_subplot(211)
        self.ax_rpm = self.figure.add_subplot(212)


        self.speed_line, = self.ax_speed.plot(
            [],
            [],
            color="red"
        )

        self.rpm_line, = self.ax_rpm.plot(
            [],
            [],
            color="orange"
        )


        self.style()



    def style(self):

        for ax in [
            self.ax_speed,
            self.ax_rpm
        ]:
            ax.set_facecolor("#050505")
            ax.tick_params(
                colors="white"
            )

            for spine in ax.spines.values():
                spine.set_color("white")


        self.ax_speed.set_title(
            "Vehicle Speed",
            color="white"
        )

        self.ax_rpm.set_title(
            "Engine RPM",
            color="white"
        )



    def update_graph(
        self,
        time_history,
        speed_history,
        rpm_history
    ):

        self.speed_line.set_data(
            time_history,
            speed_history
        )

        self.rpm_line.set_data(
            time_history,
            rpm_history
        )


        self.ax_speed.relim()
        self.ax_speed.autoscale_view()

        self.ax_rpm.relim()
        self.ax_rpm.autoscale_view()


        self.canvas.draw()