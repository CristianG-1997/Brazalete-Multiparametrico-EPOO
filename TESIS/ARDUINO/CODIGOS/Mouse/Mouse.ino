#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
#include <MPU6050_tockn.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_Sensor.h>
MPU6050 mpu6050(Wire);

const int pulsadorGPIO = 3;
const int ledGPIO = 27; 
bool estadoBoton =  false;
int btt;
Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &Wire);
int xy,xz;
BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32test"); //Bluetooth device name
   pinMode(ledGPIO, INPUT);
    Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
   // Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ; // Don't proceed, loop forever
  }
  display.display();
  delay(500); // Pause for 2 seconds
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setRotation(0);
}

void loop() {

  mpu6050.update();
  
  estadoBoton = digitalRead(ledGPIO);   
  
  if (estadoBoton == HIGH) {      
  btt=1;
  }  
  else {      
        btt=0;
  }

    xy=map(mpu6050.getAngleX(),-180,180,-10,10);  
    xz=map(mpu6050.getAngleY(),-180,180,-10,10);

  SerialBT.print(xy);
  SerialBT.print(" ");
  SerialBT.print(xz);
  SerialBT.print(" ");
  SerialBT.println(btt);
  display.display();
  delay(10);
}
