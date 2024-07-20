#include<stdio.h>
#include<math.h>
#include<stdint.h>
#include <complex.h>

//global variables
float timeInc = 0.0001;float t = 0;// sample rate 10000Hz
float sr = 10000; // sample rate

float a = 1; // [cm]
float A = 1; // amplituda
int c = 33000; // [cm/s]
int freq = 300; // [Hz]
int N = 1024; //4096; // fft size

long double r = 140; //[cm]
long double th = 45; // stepeni
long double d1, d2; // razdaljine mikrofona od izvora



double PI = M_PI;
typedef double complex cplx;

void _fft(cplx buf[], cplx out[], int n, int step){
    if (step < n) {
        _fft(out, buf, n, step * 2);
        _fft(out + step, buf + step, n, step * 2);

        for (int i = 0; i < n; i += 2 * step) {
            cplx t = cexp(-I * PI * i / n) * out[i + step];
            buf[i / 2]     = out[i] + t;
            buf[(i + n)/2] = out[i] - t;
        }
    }
}

void fft(cplx buf[], int n){
    cplx out[n];
    for (int i = 0; i < n; i++) out[i] = buf[i];

    _fft(buf, out, n, 1);
}

void show(const char * s, cplx buf[]) {
    printf("%s\n", s);
    for (int i = 0; i < N/2; i++)
        if (!cimag(buf[i]))
            printf("%f, %g \n", (sr/N)*i,creal(buf[i]));
        else
            printf("%f, (%g, %g) \n", (sr/N)*i, creal(buf[i]), cimag(buf[i]));
    printf("-----------------------------------------------------------------------------\n");
}
/*
    cplx buf[] = {1, 1, 1, 1, 0, 0, 0, 0};

    show("Data: ", buf);
    fft(buf, 8);
    show("\nFFT : ", buf);
*/
int main(){
    long double thRad = (45/180)*PI;
    cplx buf1[N], buf2[N];
    uint16_t mic1[N], mic2[N]; // izabrana duzina koja je stepen dvojike zbog fft

    d1 = sqrt(r*r - r*cos(thRad) + 0.25);
    d2 = sqrt(r*r + r*cos(thRad) + 0.25);
    for(int i = 0; i < N; i++){
        mic1[i] = ((A/d1)*sin(2*PI*freq*(t-d1/c)) + 1)*2047.5;
        mic2[i] = ((A/d2)*sin(2*PI*freq*(t-d2/c)) + 1)*2047.5;
        t += timeInc;
    }
    for(int i = 0; i < N; i++){
        buf1[i] = (cplx)((mic1[i]/2047.5)-1);
        buf2[i] = (cplx)((mic2[i]/2047.5)-1);
    }

    fft(buf1, N);
    show("FFT :", buf1);

    fft(buf2, N);
    show("\nFFT :", buf2);


    return 0;
}
