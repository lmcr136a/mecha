#define buttonA 3
#define buttonB 4
#define buttonMod 5

#define trigx 6
#define echox 7
#define trigy 8
#define echoy 9
#define trigz 10
#define echoz 11
#define error 300

int mod = 0;
String modstr = "A";
int buttonState = 0;
int lastButtonState = 0;
int AState = 0;
int BState = 0;
float lx = 0; float ly = 0; float lz = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(buttonA,INPUT);  pinMode(buttonB,INPUT);  pinMode(buttonMod,INPUT);
  pinMode(trigx,OUTPUT);  pinMode(trigy,OUTPUT);  pinMode(trigz,OUTPUT);
  pinMode(echox,INPUT);  pinMode(echoy,INPUT);  pinMode(echoz,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  buttonState = digitalRead(buttonMod);  
  AState = digitalRead(buttonA);
  BState = digitalRead(buttonB);

    
  if (buttonState != lastButtonState) {
    if (buttonState == HIGH) {
      mod++;
      if (mod==4) mod=0;
    }
  }
  lastButtonState = buttonState;

  switch (mod) {
    case 0 :
        modstr = "A";  break;
    case 1 :
        modstr = "B";  break;
    case 2 :
        modstr = "C";  break;
    case 3 :
        modstr = "D";  break;
    default :  break;
  }

  if (mod == 0) {
    if(AState == 1) {
      modstr = "a";
    }    
  }
  if (mod == 1) {
    if(AState == 1) {
      modstr = "b";
    }    
  }
  if (mod == 2) {
    if(AState == 1) {
      modstr = "c";
    }    
  }
  if (mod == 3) {
    if(AState == 1) {
      modstr = "d";
    }    
  }

  digitalWrite(trigx,HIGH); delayMicroseconds(10); digitalWrite(trigx,LOW);
  float tx = pulseIn(echox,HIGH); float dx = tx * 0.17; 
  digitalWrite(trigy,HIGH); delayMicroseconds(10); digitalWrite(trigy,LOW);
  float ty = pulseIn(echoy,HIGH); float dy = ty * 0.17;
  digitalWrite(trigz,HIGH); delayMicroseconds(10); digitalWrite(trigz,LOW);
  float tz = pulseIn(echoz,HIGH); float dz = tz * 0.17;
//  if (abs(dx-lx) > error) {
//    modstr = "X";
//  } else if (abs(dy-ly) > error) {
//    modstr = "X";
//  } else if (abs(dz-lz) > error){
//    modstr = "X";
// }
  //이상한 값이 나오면 X 출력
  lx = dx;  ly = dy; lz = dz;

  Serial.println(modstr+","+String(dx)+","+String(dy)+","+String(dz));
  //Serial.println(String(dx)+","+String(dy)+","+String(dz));
  
  delay(50);
}
