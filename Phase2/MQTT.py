import paho.mqtt.client as mqtt
import threading as threading
from time import sleep
from database import database

class Controller():   
    global db  
    rfid_value = 0
    light_value = 0
    db = database('users.db')

    def __init__(self, broker_Address, topic):
        self.broker_Address = broker_Address
        self.topic = topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message  

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected tp MQTT Broker at {self.broker_Address}")
            self.client.subscribe(self.topic)
        else:
            print("Failed to connect, retun code: ", rc)

    def on_message(self, client, userdata, msg):
        # print(f"Recieved messaage on topic '{self.topic}' : {str(msg.payload.decode('utf-8'))}")

        if (self.topic == "sensors/light/intensity"):
            self.light_value = int(msg.payload.decode('utf-8'))
            # print(self.light_value)
        
        if (self.topic == "sensors/rfid/id"):
            self.rfid_value = int(msg.payload.decode('utf-8'))
            # print(self.rfid_value)

    def getLightInensity(self):
        value = self.light_value
        # print(value)
        return value
    
    def getRfidId(self):
        str_value = str(self.rfid_value)
        return str_value
    
    def getDisplayData(self, userID):
        userData = db.getUserdata_table(userID)
        print(len(userData))
        # if len(userData) == 0:
            # return 10000
        # else:
        return userData
    
    def start(self):
        self.client.connect(self.broker_Address, 1883)
        # self.client.loop_forever()
        self.client.loop_start()

if __name__ == '__main__':
    mqtt_server = 'yourIP'
    topicLightIntensity = "sensors/light/intensity"
    topicRfid = "sensors/rfid/id"
    controller1 = Controller(mqtt_server, topicLightIntensity)
    controller2 = Controller(mqtt_server, topicRfid)
    photoresistorThread = threading.Thread(target=controller1.start)
    rfidThread = threading.Thread(target=controller2.start)
    photoresistorThread.start()
    rfidThread.start()

    while(True):
        lightvalue = controller1.getLightInensity()
        print(lightvalue)
        value = controller2.getRfidId()
        print(value)
        userData = controller2.getDisplayData(value)
        if len(userData) != 0:
            print(userData[0])
        else:
            print("no data")
       
        sleep(1)
      