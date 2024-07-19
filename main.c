#include<stdio.h>
#include<math.h>

//global variables
long double timeInc = 0.00001;
float a = 0.5; // [cm]
float A = 1; // amplituda
int c = 33000; // [cm/s]
int freq = 200; // [Hz]

long double r = 300; //[cm]
long double th = 45; // stepeni
long double d1, d2; // razdaljine mikrofona od izvora

int mic1[90000], mic2[90000];

int main(){
    long double thRad = (45/180)*M_PI;

    for(int i = 0; i < 90000; i++){

    }
    return 0;
}
