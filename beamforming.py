import numpy as np
import matplotlib.pyplot as plt

# Parameters
signal_freq = 1  # Hz
sampling_rate = 10000  # Hz
N = 1024  # Number of samples
M = 2  # Number of sensors (microphones)
spacing = 0.02  # Spacing between microphones in meters
speed_of_sound = 343  # Speed of sound in m/s
wavelength = speed_of_sound / signal_freq  # Wavelength of the signal

# Generate a signal
t = np.arange(N) / sampling_rate
signal = np.sin(2 * np.pi * signal_freq * t + 1)

# Simulate received signals at different sensors
received_signals = np.zeros((M, N), dtype=complex)
theta_deg = 30  # Angle of arrival in degrees
theta_rad = np.deg2rad(theta_deg)

# Calculate phase shifts for each sensor
for m in range(M):
    phase_shift = np.exp(-1j * 2 * np.pi * spacing * m * np.sin(theta_rad) / wavelength)
    received_signals[m, :] = signal * phase_shift

# Define covariance matrix
R = np.cov(received_signals)

# Generate steering vectors manually
def generate_steering_vectors(M, d, angles, wavelength):
    steering_vectors = np.zeros((M, len(angles)), dtype=complex)
    for idx, angle in enumerate(angles):
        theta = np.deg2rad(angle)
        for m in range(M):
            steering_vectors[m, idx] = np.exp(-1j * 2 * np.pi * d * m * np.sin(theta) / wavelength)
    return steering_vectors

angle_grid = np.linspace(-90, 90, 181)
steering_vectors = generate_steering_vectors(M, spacing, angle_grid, wavelength)

# Perform MVDR beamforming
def mvdr_beamforming(R, steering_vectors):
    num_angles = steering_vectors.shape[1]
    output_power = np.zeros(num_angles)

    for i in range(num_angles):
        a_theta = steering_vectors[:, i]
        a_theta_H = np.conjugate(a_theta).T
        numerator = np.dot(a_theta_H, a_theta)
        denominator = np.dot(np.dot(a_theta_H, np.linalg.inv(R)), a_theta)
        output_power[i] = np.abs(numerator / denominator)

    return output_power

mvdr_output = mvdr_beamforming(R, steering_vectors)

# Plot the MVDR beamforming output
plt.figure(figsize=(10, 6))
plt.plot(angle_grid, mvdr_output)
plt.title('Beamforming Output (MVDR)')
plt.xlabel('Angle (degrees)')
plt.ylabel('Output power')
plt.grid()
plt.show()
