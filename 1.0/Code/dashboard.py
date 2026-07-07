import matplotlib.pyplot as plt

plt.ion()

fig, (ax_speed, ax_rpm) = plt.subplots(2, 1, figsize=(10, 8))

speed_line, = ax_speed.plot([], [], label="Speed")
rpm_line, = ax_rpm.plot([], [], label="RPM")

ax_speed.set_title("Vehicle Speed")
ax_speed.set_ylabel("MPH")

ax_rpm.set_title("Engine RPM")
ax_rpm.set_ylabel("RPM")
ax_rpm.set_xlabel("Time")

ax_speed.legend()
ax_rpm.legend()

def update_graphs(time_history, speed_history, rpm_history):
    speed_line.set_data(time_history, speed_history)
    rpm_line.set_data(time_history, rpm_history)

    ax_speed.relim()
    ax_speed.autoscale_view()

    ax_rpm.relim()
    ax_rpm.autoscale_view()

    plt.draw()
    plt.pause(0.01)
    
