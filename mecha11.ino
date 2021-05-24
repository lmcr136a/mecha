#include "BluetoothSerial.h"

BluetoothSerial bt;

#define buttonA 15
#define buttonB 4
#define cl 22
#define dt 23

#define trigx 33
#define echox 32
#define trigy 27
#define echoy 14
#define trigz 26
#define echoz 25
#define error 300

int mod = 0;
String modstr = "default";
int AState = 0;
int BState = 0;
//float lx = 0; float ly = 0; float lz = 0;

int count = 0;
int newCl, preCl;
int interval = 5;
int NumofMod = 7

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(buttonA,INPUT);  pinMode(buttonB,INPUT);
  pinMode(cl, INPUT); pinMode(dt, INPUT);
  pinMode(trigx,OUTPUT);  pinMode(trigy,OUTPUT);  pinMode(trigz,OUTPUT);
  pinMode(echox,INPUT);  pinMode(echoy,INPUT);  pinMode(echoz,INPUT);

  preCl = digitalRead(cl);

  bt.begin("ESP32_SPP");
}

void loop() {
  // put your main code here, to run repeatedly:

  newCl = digitalRead(cl);
  if(newCl != preCl){
    if(digitalRead(dt)!=newCl){
      count--;
    }
    else{
      count++;
    }
  }

  preCl = newCl;

  AState = digitalRead(buttonA);
  BState = digitalRead(buttonB);

  if(count>(NumofMod*interval) - 1) count = 0;
  if(count<0) count = (NumofMod*interval) - 1;

  mod = count/interval;

  //Mode: default, rect, colored_rect, circle, colored_circle, cube, color
  switch (mod) {
    case 0 :
        modstr = "default";  break;
    case 1 :
        modstr = "rect";  break;
    case 2 :
        modstr = "colored_rect";  break;
    case 3 :
        modstr = "circle";  break;
    case 4 :
        modstr = "colored_circle";  break;
    case 5 :
        modstr = "cube";  break;
    case 6 :
        modstr = "color";  break;
    default :  break;
  }

  digitalWrite(trigx,HIGH); delayMicroseconds(10); digitalWrite(trigx,LOW);
  float tx = pulseIn(echox,HIGH,30000); float dx = tx * 0.17;
  digitalWrite(trigy,HIGH); delayMicroseconds(10); digitalWrite(trigy,LOW);
  float ty = pulseIn(echoy,HIGH,30000); float dy = ty * 0.17;
  digitalWrite(trigz,HIGH); delayMicroseconds(10); digitalWrite(trigz,LOW);
  float tz = pulseIn(echoz,HIGH,30000); float dz = tz * 0.17;
//  if (abs(dx-lx) > error) {
//    modstr = "X";
//  } else if (abs(dy-ly) > error) {
//    modstr = "X";
//  } else if (abs(dz-lz) > error){
//    modstr = "X";
// }
  //이상한 값이 나오면 X 출력
//  lx = dx;  ly = dy; lz = dz;

  bt.println(String(AState)+","+String(BState)+","+modstr+","+String(dx)+","+String(dy)+","+String(dz));
  delay(50);
}