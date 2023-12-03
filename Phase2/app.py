from dash import Dash, html, callback, Input, Output, dcc
from threading import Thread
from datetime import datetime
# import dash_dangerously_set_inner_html
import dash_daq as daq
import RPi.GPIO as GPIO
import time
from bluepy.btle import Scanner

from time import sleep
# import pydash
# import bluetooth
import Freenove_DHT as DHT
# import board

# sending email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# reading email
import email
import imaplib

# mqtt
# import paho.mqtt.subscribe as subscribe
from MQTT import Controller
mqtt_server = '172.20.10.2' #Add your IP to connect to MQTT server
topicLightIntensity = "sensors/light/intensity"
topicRfid = "sensors/rfid/id"
light_controller = Controller(mqtt_server, topicLightIntensity)
rfid_controller = Controller(mqtt_server, topicRfid)
light_controller.start()
rfid_controller.start()

# Setup User settings
from UserSettings import UserSettings
global currentSettings
currentSettings = UserSettings()

# Setup LED 
from LED import LED
led_pin = 16
led = LED(led_pin, False)
LED_STATUS = False
lightCount = 0

max_brightness = 600
#LED pin for Light Intensity
# led_pin2 = 17

# Setup DHT11
DHT_PIN = 12 # GPIO pin for DHT sensor
FAN_STATUS = False # Initially, the motor is off
humidity = 0
temperature = 0 
tempCount = 0

# Setup Motor
from DC_Motor import DC_Motor 
# MOTOR_PIN = 17  # GPIO pin for the motor (replace with the actual pin number)
Motor1_pin = 15 # Enable Pin
Motor2_pin = 13 # Input Pin
Motor3_pin = 11 # Input Pin
motor = DC_Motor(Motor1_pin, Motor2_pin, Motor3_pin, False)
# MOTOR_STATUS = False  # Initially, the motor is off

# Email Information
subject = 'Checking Temperature'
smtp_server = 'smtp.gmail.com'
# sender_email = 'cookiecove8@gmail.com'
sender_email = 'python01100922@gmail.com'
# sender_password = 'skfp plbw ttkw xaip'
sender_password = 'txlzudjyidtoxtyj'
receiver_email = 'baduar10@gmail.com'
# receiver_email = currentSettings.user_email

emailCount = 0


app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        # html.Meta(charset="UTF-8"),
        html.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        html.Title("Smart Home Dashboard"),
        # Include AmCharts scripts
        html.Script(src="https://cdn.amcharts.com/lib/5/index.js"),  # alert("This alert box was called with the onload event");
        html.Script(src="https://cdn.amcharts.com/lib/5/xy.js"),
        html.Script(src="https://cdn.amcharts.com/lib/5/radar.js"),
        html.Script(src="https://cdn.amcharts.com/lib/5/themes/Animated.js"),

        # Include your custom script.js
        # html.Script(src="script.js"),
    ]),
    html.Div([
        html.Header([
            html.H1("Smart Home Dashboard", style={'color': '#ecf0f1'}),
        ]),
        html.Main([
            html.Div([
                html.Section(id="profile", children=[
                    html.H2("User Information"),
                    html.Div(
                        children=[
                            html.Div(
                                html.Img(src='assets/images/defaultpfp.jpg', id='User_PHOTO', width="100", height="100",
                                         style={"border-radius": "50%", "margin-bottom": "10px"}),
                                style={"text-align": "center"}
                            ),
                            html.Div([html.Strong("ID: "), html.Span(id='User_ID')]),
                            html.Div([html.Strong("Name: "), html.Span(id='User_NAME')]),
                            html.Div([html.Strong("Email: "), html.Span(id='User_EMAIL')]),
                            html.Div([html.Strong("Card ID: "), html.Span(id='User_CARDID')]),
                            html.Div([html.Strong("Temperature: "), html.Span(id='User_TEMP')]),
                            html.Div([html.Strong("Humidity: "), html.Span(id='User_HUM')]),
                            html.Div([html.Strong("Light Intensity: "), html.Span(id='User_LIGHT')]),
                        ],
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "alignItems": "center",
                            "margin": "20px",
                            # "max-width": "300px",  # Set your desired max-width
                        },
                    ),
                ],
                    style={
                        # "max-width": "300px",  # Set your desired max-width
                    },
                ),
                # html.Section(id="lightswitch", children=[
                #     html.H2("Phase 1 - Light Switch"),

                #     html.Div(children=[
                #         # daq.ToggleSwitch(id="click-light", on=False),
                #         html.Img(src='assets/images/LightOff.PNG', id='img_light', width="100", height="100"),
                #     ]),
                #     # html.Button('Switch Light', id='click_light', n_clicks=0),
                #     daq.BooleanSwitch(id='click_light', on=False),
                # ]),
                # html.Section(id="email", children=[
                    # html.H2("Phase 2 - Email"),
                    # html.Div([
                    # daq.ToggleSwitch(id="click-light", on=False),
                    # html.Img(src='assets/images/LightOff.PNG', id='img_light', width="100", height="100"),
                    # html.Div(children='Phase 2'),
                    # html.P("Press Button below to send email about temperature!"),
                    # html.Div(children='status email', id='status_email_sent')
                # ]),
                # html.Button('Send Email', id='sending_email', n_clicks=0),
                # ]),

                html.Div([
                    html.Div([
                        html.Section(id="dht11sensor", children=[
                            # html.H2("Phase 2 - DHT11 Sensor Data"),
                            html.Div([
                                # html.Div("Temperature: ", id='temperature'),
                                # html.Div("Humdity: ", id='humidity'),
                                html.Div([
                                    daq.Gauge(
                                        color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
                                        id="TempGauge",
                                        showCurrentValue=True,
                                        units="Temp " + u'\N{DEGREE SIGN}',
                                        label='Temperature',
                                        max=100,
                                        min=0,
                                        size=200,
                                        value=0,
                                    ),
                                    daq.Gauge(
                                        color={"gradient":True,"ranges":{"white":[0,5],"blue":[5,10]}},
                                        id="HumGauge",
                                        showCurrentValue=True,
                                        units="Hum %",
                                        label='Humidity',
                                        max=100,
                                        min=0,
                                        size=200,
                                        value=0,
                                    ),
                                    html.Img(src='assets/images/Fan2.PNG', id='status_fan', className="Fan_Off", width="250", height="250"),
                                ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr 1fr', 'grid-column-gap': '20px', 'grid-row-gap': '20px'}),
                            ]),
                        ]),
                        html.Section(id="Photoresistor Sensor Data", children=[
                            html.H2("Phase 3 - Photoresistor Sensor Data"),
                            html.Div([

                                # html.Div("Message:  ", id='sending_email_light'),
                                html.Div(style={'display': 'flex', 'justify-content': 'center' }, children=[
                                    html.Div([
                                        html.Div("Light: ", id='light_intensity'),
                                        html.Data(id='light_data', value=0),
                                        html.Img(src='assets/images/sun.png', id='room_brightness', width="170", height="170", style={'filter': 'brightness(100%)'}),  # style="filter: brightness(10%)"
                                    ]),
                                    html.Div([
                                        html.Div("LED Status", id=''),
                                        html.Img(src='assets/images/LightOff.PNG', id='img_light', width="170", height="170"),
                                    ]),
                                ]),
                                html.Div("", id='status_of_led', style={'padding-left': '80px', 'padding-top': '20px'}),
                            ]),
                            dcc.Interval(id='interval-component', interval=3*1000, n_intervals=0),
                        ]),
                    ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-column-gap': '20px', 'grid-row-gap': '20px'}),
                    html.Section(id="Bluetooth Devices", children=[
                        html.H2("Bluetooth Devices"),

                        # Blue rectangle container
                        html.Div(
                            children=[
                                # Left side: "Total nearby Bluetooth devices" label
                                html.Div(
                                    children=[
                                        html.H4("Total nearby Bluetooth devices", style={'color': '#ecf0f1'}),
                                    ],
                                    style={'flex': '50%', 'padding': '16px', 'box-sizing': 'border-box'},
                                ),

                                # Right side: Number of nearby Bluetooth devices
                                html.Div(
                                    children=[
                                        html.H1("N/A", id='bluetoothDiv', style={'color': 'black', 'margin': '0', 'background-color': 'white', 'border': '2px solid black', 'padding': '8px', 'border-radius': '5px', 'font-size': 'inherit'}),
                                    ],
                                    style={'flex': '50%', 'padding': '16px', 'box-sizing': 'border-box'},
                                ),
                            ],
                            style={'display': 'flex', 'background': '#3498db', 'border-radius': '10px', 'margin': '16px 0'},
                        ),

                        html.Button('Submit', id='bluetoothbtn', n_clicks=0),
                    ]),

                ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px'}),
            ], style={'display': 'grid', 'grid-template-columns': '0.2fr 1fr', 'grid-column-gap': '20px', 'grid-row-gap': '20px'})
        ]),
        # Footer
        # html.Footer([
        #     html.P("© 2023 Smart Home Dashboard", style={'color': '#ecf0f1'}),
        # ]),
    ]),
])


@callback(
    Output("room_brightness", "style"),
    Input('interval-component', 'n_intervals'),
    Input("light_data", "value")
)

def set_brightness_image(n_intervals, value):
    currrent_brightness = ((int(value) * 100) / max_brightness)
    return {'filter': f'brightness({currrent_brightness}%)'}

# Phase 1
# @callback(
#     Output("img_light", "src"),
#     Input("click_light", "on")
# )

# def toggle_led(on):
#     if on == True:
#         led.switchLight(True)
#         return 'assets/images/LightOn.PNG'
#     else:
#         led.switchLight(False)
#         return 'assets/images/LightOff.PNG'

# Phase 2
@callback(
    Output("status_fan", "className"),
    Input("TempGauge", "value")
)           

def checkTemp(value):
    # count = 0
    global tempCount
    global FAN_STATUS
    print(tempCount)
    print(FAN_STATUS)
    if value >= currentSettings.temperature and tempCount == 0:
        tempCount = 1
        print(tempCount)
        print('send about temperature email')
        
        message = f'The current temperature is {value:.2f}°C. Would you like to turn on the fan?'
        if send_email(subject, message, sender_email, sender_password, receiver_email) == True:
            # will have to find a way to stop the sending message waiting for a reply
            print("wait a 30 seconds")
            time.sleep(30)

            print("proceed to read email")
            if receive_email() == True:
                print ('Email sent successfully and User said Yes!')
                print('change fan status')
                FAN_STATUS = True
                # count = 0
                # return toggle_fan(True)
            else:
                print('Email sent successfully and User said No!') 
                print('change fan status')  
                tempCount = 0
                FAN_STATUS = False
                # return toggle_fan(False)
        else:
            print('Email sending failed!')
            tempCount = 0
            FAN_STATUS = False
            # return toggle_fan(False)

    elif value < currentSettings.temperature and tempCount == 1:
        tempCount = 0
        print("Temperature gone down")
        FAN_STATUS = False
        
    print(FAN_STATUS)
    motor.switchMotor(FAN_STATUS)
    return toggle_fan(FAN_STATUS)

def toggle_fan(fan_status):
    if fan_status == True:
        # return 'Fan Status: ON'
        return 'Fan_On'
    else:
        # return 'Fan Status: OFF'
        return 'Fan_Off'

def send_email(subject, message, sender_email, sender_password, receiver_email):
# Configure your email settings here
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False

def receive_email():

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(sender_email, sender_password)

    imap.select("Inbox")

    reply_subject = f'"RE:{subject}"'
    print(reply_subject)
    # _, msgnums = imap.search(None, f"FROM {sender_email} UNSEEN")
    _, msgnums = imap.search(None, f'SUBJECT {reply_subject} UNSEEN')

    print(msgnums)
    if msgnums[0]:
        msgnum = msgnums[0].split()[-1]
        _, data = imap.fetch(msgnum, "RFC822")
        # print(data) 

        message = email.message_from_bytes(data[0][1])

        print (f"message number:  {msgnums}")
        print (f"From: {message.get('From')}")
        print (f"To: {message.get('To')}")
        print (f"BCC: {message.get('BCC')}")
        print (f"Date: {message.get('Date')}")
        print (f"Subject: {message.get('Subject')}")

        print ("Content:")
        for part in message.walk():
            # if part.get_content_type() == "text/plain":
            #     print(part.as_string())
            # print(message.walk())
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))

            if content_type == "text/plain" and 'attachment' not in content_disposition: 
                body = part.get_payload()
                # print(body)

                first_line = body.split('\n', 1)[0]
                print(first_line)
                # print(part.as_string())
                
                # check if the response is yes 
                if first_line.strip().lower() == "yes":
                    print("User accepts")
                    #Turn on the motor
                    # GPIO.output(MOTOR_PIN, GPIO.HIGH)
                    # MOTOR_STATUS = True
                    return True
                else:
                    print("User declined")
                    #Turn off the motor
                    # GPIO.output(MOTOR_PIN, GPIO.LOW)
                    # MOTOR_STATUS = False
                    return False
    imap.close()

@callback(
    Output('TempGauge', 'value'),
    Output('HumGauge', 'value'),
    Input('interval-component', 'n_intervals')
)

def update_sensor_data(n_intervals):
    dht = DHT.DHT(DHT_PIN)
    for i in range(0,15):
        chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            print("DHT11,OK!")
            break
    print(f'Humidity: {dht.humidity:.2f}%')
    print(f'Temperature: {dht.temperature:.2f}°C')
    # return int(f'{dht.humidity:.2f}'), int(f'{dht.temperature:.2f}')
    return dht.temperature, dht.humidity

#Phase 3
@callback(
    Output('status_of_led', 'children'),
    Output("img_light", "src"),
    Input('light_data', 'value'),
)

# def setup_gpio():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(led_pin2, GPIO.OUT)
#     GPIO.output(led_pin2, GPIO.LOW)

# def turn_on_led():
#     GPIO.output(led_pin2, GPIO.HIGH)

# def turn_off_led():
#     GPIO.output(led_pin2, GPIO.LOW)

def checkIntensity(value):
    global lightCount
    global LED_STATUS
    light_value = int(value)
    # print(light_value)

    if light_value < currentSettings.brightness and lightCount == 0:
        lightCount = 1
        print("Light is ON")
        led.turn_on_led()
        LED_STATUS = True

        current_time = datetime.now().strftime("%H:%M")
        subject = f"The Light is ON at {current_time} time."
        message = f"The light turned on at {current_time} time due to low intensity."

        if send_email(subject, message, sender_email, sender_password, receiver_email):
            print("Email about light sent successfully")
            # Add a delay to avoid sending multiple emails in a short time
            time.sleep(30)
        else:
            print("Email sending failed!")

    elif light_value >= currentSettings.brightness and lightCount == 1:
        lightCount = 0
        print("Light is OFF")
        led.turn_off_led()
        LED_STATUS = False
    
    return status_LED(LED_STATUS), get_light_image(LED_STATUS)

# setup_gpio()

def status_LED(LED_STATUS):
    if (LED_STATUS == True):
        return "Message: Email has been sent"
    else:
        return ""
    
def get_light_image(LED_STATUS):
    if LED_STATUS == True:
        return 'assets/images/LightOn.PNG'
    else:
        return 'assets/images/LightOff.PNG'

# Replace this with your actual light intensity reading
# light_intensity_value = 300
# checkIntensity(light_intensity_value)
@callback(
    Output('light_intensity', 'children'),
    Output('light_data', 'value'),
    Input('interval-component', 'n_intervals')
)

def getDataLightfromArduino(n_intervals):
    lightvalue = light_controller.getLightInensity()
    strlightvalue = str(lightvalue)
    # print(f'light: {lightvalue}')
    return f"Light Intensity: {lightvalue}", strlightvalue

# Phase 4 
@app.callback(
    Output('User_ID', 'children'),
    Output('User_NAME', 'children'),
    Output('User_EMAIL', 'children'),
    Output('User_CARDID', 'children'),
    Output('User_TEMP', 'children'),
    Output('User_HUM', 'children'),
    Output('User_LIGHT', 'children'),
    Output('User_PHOTO', 'src'),
    Input('interval-component', 'n_intervals')
)

def getDataUserfromArduino(n_intervals):
    global emailCount
    global current_carId
    
    rfidvalue = rfid_controller.getRfidId()
    strRfidValue = str(rfidvalue)
    print(f'rfid ID: {rfidvalue}')

    # print('HELLOOOO')
    userData = getUserData(strRfidValue)
    # print(userData)
    # print('HIII')
    # if len(userData[0]) == 0 or rfidvalue == 0:
    if not userData or rfidvalue == 0:
        # print('HUH?!?!?!')
        return ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'assets/images/defaultpfp.jpg '
    else:
        # print('NICEE')
        id = userData[0][0]
        first_name = userData[0][1]
        last_name = userData[0][2]
        user_email = userData[0][3] 
        card_id = userData[0][4]
        temp = userData[0][5]
        hum = userData[0][6]
        light = userData[0][7]
        photo = userData[0][8]

        print(f'emailCount: before {emailCount}')
        if emailCount == 0:
            emailCount = 1
            current_carId = int(rfidvalue)
            print(f'emailCount: after {emailCount}')
            current_time = datetime.now().strftime("%H:%M")
            subject = f"User {first_name} {last_name} entered at {current_time} time."
            message = f"User {first_name} {last_name} enetred at {current_time} after tapping card."

            if send_email(subject, message, sender_email, sender_password, receiver_email):
                print("Email to User sent successfully")
                # Add a delay to avoid sending multiple emails in a short time
                time.sleep(30)
            else:
                print("Email sending failed!")
        
        # if int(rfidvalue) != currentSettings.card_id:
        if current_carId != int(rfidvalue):
            emailCount = 0
            print(f'emailCount: change {emailCount}')

        # print(userData[0][3])

        # set current user settings
        currentSettings.temperature = temp
        currentSettings.brightness = light
        currentSettings.card_id = card_id
        currentSettings.user_email = user_email

        id_display = f' {id}'
        name_display = f' {first_name} {last_name}'
        email_display = f' {user_email}'
        cardID_display = f' {card_id}'
        temp_display = f' {temp}'
        hum_display = f' {hum}'
        light_display = f' {light}'
        photo_display = f' {photo}'
        return id_display, name_display, email_display, cardID_display, temp_display, hum_display, light_display, photo_display

def getUserData(rfidID):
    return rfid_controller.getDisplayData(rfidID)

# Phase 4 - Bluetooth
@app.callback(
    Output("bluetoothDiv", "children"),
    Input('bluetoothbtn', 'n_clicks'),
    prevent_initial_call=True
)

def update_bluetooth_device_count(n_clicks):
    print("Scanning for nearby Bluetooth devices...")
    
    start_time = time.time()  # Record the start time of the scan
    scan_duration = 10.0  # Set the desired duration for the scan (in seconds)
    
    num_devices = 0
    
    scanner = Scanner()
    
    while (time.time() - start_time) < scan_duration:
        devices = scanner.scan(2.0)  # Scan for 2 seconds (adjust as needed)
        
        for device in devices:
            if -100 < device.rssi < -75:
                num_devices += 1
    
    print("Nearby Devices Found")
    return num_devices

    # Add a delay between scans to avoid overwhelming the system
    time.sleep(60)  # Adjust the delay as needed

# run app
if __name__ == '__main__':
    # app.run(host='172.20.10.2', debug=True)
    app.run(debug=True)