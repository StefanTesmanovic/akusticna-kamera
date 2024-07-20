#include<stdio.h>
#include<math.h>
#include<stdint.h>

//global variables
float timeInc = 0.0001;float t = 0;// sample rate 10KHz
float a = 0.5; // [cm]
float A = 1; // amplituda
int c = 33000; // [cm/s]
int freq = 200; // [Hz]

long double r = 300; //[cm]
long double th = 45; // stepeni
long double d1, d2; // razdaljine mikrofona od izvora

uint16_t mic1[4096], mic2[4096]; // izabrana duzina koja je stepen dvojike zbog fft

int main(){
    long double thRad = (45/180)*M_PI;
    d1 = sqrt(r*r - r*cos(thRad) + 0.25);
    d2 = sqrt(r*r + r*cos(thRad) + 0.25);
    for(int i = 0; i < 4096; i++){
        mic1[i] = ((A/d1)*sin(2*M_PI*freq*(t-d1/c)) + 1)*2048;
        mic2[i] = ((A/d2)*sin(2*M_PI*freq*(t-d2/c)) + 1)*2048;
        t += timeInc;
    }
    return 0;
}
