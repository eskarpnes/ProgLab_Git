/*
 * Oving 1, Morse code
 * Connect with python and send serial data
 * LED states:
 *  1 green: dot          (SEND 0)
 *  2 green: dash         (SEND 1)
 *  short pause: red      (SEND 2)
 *  long pause: all flash (SEND 3)
 */

int BTN(8),
    SHORTPRESS(200),
    LONGPRESS(300),
    SHORTBREAK(600),
    LONGBREAK(1200),
    RESET(3000);

void light(int led){digitalWrite(led,1);}
void dim(int led){digitalWrite(led,0);}
void lightAll(){light(4); light(3); light(2);}
void dimAll(){dim(4); dim(3); dim(2);}
void blinkLeds(int del, int times){
  for (int i=0;i<times;i++){
    lightAll();
    delay(del);
    dimAll();
    delay(del);
  }
}

void shortPress(){
  writeMorse(0);
  light(4); delay(50); dim(4);
}
void longPress(){
  writeMorse(1);
  light(4); light(3);
  delay(50);
  dim(4); dim(3);
}
void shortBreak(){
  writeMorse(2);
  dim(2);
}
void longBreak(){
  writeMorse(3);
  blinkLeds(300,1);
}
void resetMsg(){
  writeMorse(4);
  blinkLeds(50,10);
}

void writeMorse(int code){
  Serial.println(code);
  delay(100);
}

void setup() {
  Serial.begin(9600);
  pinMode(4,OUTPUT); //green short
  pinMode(3,OUTPUT); //green long
  pinMode(2,OUTPUT); //red for breaks
  pinMode(8,INPUT);
}

unsigned long timestamp, btnDur, breakDur;
bool started = false, activeWord = false, noBreakLast = false;
void loop(){
  if (digitalRead(BTN)){
    started = true;
    timestamp = millis();
    while (digitalRead(BTN)){
      btnDur = millis()-timestamp;
      if (btnDur>=RESET) break;
      //if (btnDur>=LONGPRESS) light(4); light(3);
    }
    noBreakLast=true; //allows a break after a word/letter
    if (btnDur>=RESET){
      resetMsg();
      noBreakLast=false; //no break after reset
    }
    else if (btnDur >= LONGPRESS) longPress();
    else shortPress();
  }
  else if (started && noBreakLast && !activeWord && !digitalRead(BTN)){
    timestamp = millis();
    while (!digitalRead(BTN)){
      breakDur = millis()-timestamp;
      if (breakDur>=LONGBREAK){
        //lightLeds(leds,3,500);
        longBreak();
        break;
      }
      else if (breakDur>SHORTBREAK && breakDur<LONGBREAK){
        light(2);
        //keep the light on to indicate
        //that you can keep typing
      }
    }
    if (breakDur<LONGBREAK && breakDur>SHORTBREAK){
      shortBreak();
    }
    noBreakLast = false;
  }
}
