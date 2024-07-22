import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
from pyargus.directionEstimation import gen_ula_scanning_vectors, DOA_MEM

# Parameters
sampling_rate = 48000  # Hz
N = 1024  # Number of samples to use for FFT
M = 2  # Number of sensors (microphones)
spacing = 0.018  # Spacing between microphones in meters
speed_of_sound = 343  # Speed of sound in m/s

# Initialize data lists
x_data, y_data = [], []

# Open serial connection
with serial.Serial('/dev/ttyUSB0', 230400, timeout=4) as ser:
    # Initialize the plot
    figure, (ax_signal, ax_doa) = plt.subplots(2, 1)
    line1, = ax_signal.plot([], [], '-', label='Mic 1')
    line2, = ax_signal.plot([], [], '-.', label='Mic 2')
    ax_signal.legend()
    ax_signal.set_title('Microphone Signals')
    ax_signal.set_xlabel('Time (s)')
    ax_signal.set_ylabel('Amplitude')
    ax_signal.grid(True)

    angle_marker, = ax_doa.plot([], [], 'ro', label='Estimated DOA')
    ax_doa.legend()
    ax_doa.set_title('Direction of Arrival')
    ax_doa.set_xlabel('Time (s)')
    ax_doa.set_ylabel('Angle (degrees)')
    ax_doa.set_xlim(0, 10)  # Set appropriate x-axis limits
    ax_doa.set_ylim(-90, 90)  # Set angle limits
    ax_doa.grid(True)

    def update(frame):
        l = ser.readline()
        try:
            data = l.decode("utf-8").split(',')
            data1 = []
            data2 = []
            for dat in data[:-1]:
                c1, c2 = dat.split(' ')
                data1.append(int(c1))
                data2.append(int(c2))

            # Normalize the data
            data1 = np.array(data1)
            data2 = np.array(data2)
            data1 = 2 * (data1 / 4095) - 1
            data2 = 2 * (data2 / 4095) - 1

            num_samples = len(data1)
            time_values = np.linspace(0, num_samples / sampling_rate, num_samples)

            # Set the data for the plots
            line1.set_data(time_values, data1)
            line2.set_data(time_values, data2)
            ax_signal.relim()
            ax_signal.autoscale_view()

            # Beamforming calculations
            received_signals = np.array([data1, data2], dtype=complex)
            R = np.cov(received_signals)

            # Generate steering vectors
            angle_grid = np.linspace(-90, 90, 181)
            steering_vectors = gen_ula_scanning_vectors(M, spacing / speed_of_sound, angle_grid)

            # Perform MVDR beamforming
            mvdr_output = DOA_MEM(R, steering_vectors)

            # Find the angle of arrival (DOA)
            doa_angle = angle_grid[np.argmax(mvdr_output)]

            # Update DOA plot
            angle_marker.set_data(time_values[-1], doa_angle)

            return line1, line2, angle_marker
        except Exception as e:
            print(e)
            return line1, line2, angle_marker

    # Run the animation
    animation = FuncAnimation(figure, update, interval=1000)  # Update every second
    plt.show()
