import numpy as np
import math
import cmath

# Global variables
time_inc = 0.0001  # Sample interval, 10000Hz sample rate
t = 0  # Time variable
sr = 10000  # Sample rate
a = 1  # [cm]
A = 1  # Amplitude
c = 33000  # [cm/s]
freq = 300  # [Hz]
N = 1024  # FFT size

r = 140  # [cm]
th = 45  # Degrees
d1 = 0
d2 = 0

PI = math.pi

def show(title, buf, sr, N):
    print(title)
    for i in range(N//2):
        frequency = (sr / N) * i
        magnitude = np.abs(buf[i])
        phase = np.angle(buf[i])
        print(f"{frequency:.2f} Hz: {magnitude:.6f} (magnitude), {phase:.6f} (phase)")
    print("-----------------------------------------------------------------------------")

def gen_ref():


def main():
    global t, d1, d2
    th_rad = (45 / 180) * PI

    mic1 = np.zeros(N, dtype=np.uint16)
    mic2 = np.zeros(N, dtype=np.uint16)

    d1 = np.sqrt(r*r - r*np.cos(th_rad) + 0.25)
    d2 = np.sqrt(r*r + r*np.cos(th_rad) + 0.25)
    for i in range(N):
        mic1[i] = ((A/d1) * np.sin(2 * PI * freq * (t - d1/c)) + 1) * 2047.5
        mic2[i] = ((A/d2) * np.sin(2 * PI * freq * (t - d2/c)) + 1) * 2047.5
        t += time_inc

    buf1 = (mic1 / 2047.5) - 1 + 0j  # Convert to complex numbers
    buf2 = (mic2 / 2047.5) - 1 + 0j  # Convert to complex numbers

    fft_buf1 = np.fft.fft(buf1)
    show("FFT (Mic1):", fft_buf1, sr, N)

    fft_buf2 = np.fft.fft(buf2)
    show("FFT (Mic2):", fft_buf2, sr, N)

if __name__ == "__main__":
    main()
