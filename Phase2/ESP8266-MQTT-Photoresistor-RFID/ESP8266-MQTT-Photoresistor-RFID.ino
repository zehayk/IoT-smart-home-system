// Photoresistor
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Arduino.h>

// RFID
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN D8
#define RST_PIN D0

// Photoresistor
int sensorVal = 0;
const int ANALOG_READ_PIN = A0; 

const char* ssid = "yourWifi";
const char* password = "pass";
const char* mqtt_server = "IPOfRpi"; 

WiFiClient vanieriot;
PubSubClient client(vanieriot); 

// RFID
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;
// Init array that will store new NUID
//byte nuidPICC[4];


void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP-8266 IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messagein;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messagein += (char)message[i];
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
        if (client.connect("vanieriot")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 3 seconds");
      // Wait 5 seconds before retrying
      delay(1500);
    }
 }
}

String GettingDec(byte *buffer, byte bufferSize) {
  String strId = "";
  for (byte i = 0; i < bufferSize; i++) {
    strId += buffer[i], DEC;
  }
//  Serial.print(strId);
  return strId;
}

void setup() {
  Serial.begin(115200);
  //MQTT
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // RFID
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522
}

void loop() {
//  ESP.wdtFeed();
//  delay(0);
  delay(1000);
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("vanieriot");
  
  // photoresistor
  sensorVal = analogRead(ANALOG_READ_PIN);
  Serial.println(sensorVal);
  char cstr[16];
  itoa(sensorVal,cstr, 10);
  client.publish("sensors/light/intensity", cstr);

  // RFID
  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent())
    return;
  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;
  String id = GettingDec(rfid.uid.uidByte, rfid.uid.size);
  Serial.println(id);
  
   
  // Halt PICC
  rfid.PICC_HaltA();
  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
  
  client.publish("sensors/rfid/id", id.c_str());
}
