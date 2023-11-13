from dash import Dash, html, callback, Input, Output, dcc
from datetime import datetime
# import dash_dangerously_set_inner_html
import dash_daq as daq
import RPi.GPIO as GPIO
import time
from time import sleep
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
import paho.mqtt.subscribe as subscribe

# Setup LED 
from LED import LED
led_pin = 16
led = LED(led_pin, False)
LED_STATUS = False

max_brightness = 600
#LED pin for Light Intensity
# led_pin2 = 17

# Setup DHT11
DHT_PIN = 12 # GPIO pin for DHT sensor
FAN_STATUS = False # Initially, the motor is off
humidity = 0
temperature = 0 
count = 0

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
sender_email = 'cookiecove8@gmail.com'
sender_password = 'skfp plbw ttkw xaip'
receiver_email = 'baduar10@gmail.com'


external_scripts = [
    # "https://cdn.amcharts.com/lib/5/index.js",
    # "https://cdn.amcharts.com/lib/5/xy.js",
    # "https://cdn.amcharts.com/lib/5/radar.js",
    # "https://cdn.amcharts.com/lib/5/themes/Animated.js",
    # 'tempChart.js',
    # 'humidityChart.js'
]

external_stylesheets = [
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # {
    #     'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
    #     'rel': 'stylesheet',
    #     'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
    #     'crossorigin': 'anonymous'
    # }
]
with open("tempChart.js", "r") as file:
    tempChartScript = file.read()
with open("humidityChart.js", "r") as file:
    humChartScript = file.read()


# app = Dash(__name__)
app = Dash(__name__, external_scripts=external_scripts, external_stylesheets=external_stylesheets)

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
        html.Nav([
            dcc.Link("Devices", href="#devices", style={'color': '#ecf0f1', 'margin': '0 1em'}),
            dcc.Link("Sensors", href="#sensors", style={'color': '#ecf0f1', 'margin': '0 1em'}),
            dcc.Link("Controls", href="#controls", style={'color': '#ecf0f1', 'margin': '0 1em'}),
        ]),
        html.Main([
            html.Section(id="lightswitch", children=[
                html.H2("Phase 1 - Light Switch"),

                html.Div(children=[
                    # daq.ToggleSwitch(id="click-light", on=False),
                    html.Img(src='assets/images/LightOff.PNG', id='img_light', width="100", height="100"),
                ]),
                # html.Button('Switch Light', id='click_light', n_clicks=0),
                daq.BooleanSwitch(id='click_light', on=False),
            ]),
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
            html.Section(id="dht11sensor", children=[
                html.H2("Phase 2 - DHT11 Sensor Data"),
                html.Div([
                    # html.Div("Temperature: ", id='temperature'),
                    # html.Div("Humdity: ", id='humidity'),
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
                ]),
            ]),
            html.Section(id="", children=[
                html.H2("Phase 3 - Photoresistor Sensor Data"),
                html.Div([
                    html.Div("Light: ", id='light_intensity'),
                    html.Data(id='light_data', value=0),
                    html.Div("Status of light:  ", id='status_of_led'),
                    html.Div("Message:  ", id='sending_email_light'),
                    html.Img(src='assets/images/sun.png', id='room_brightness', width="250", height="250", style={'filter': 'brightness(100%)'}),  # style="filter: brightness(10%)"
                ]),
                dcc.Interval(id='interval-component', interval=3*1000, n_intervals=0),
            ]),
        ]),
        # Footer
        html.Footer([
            html.P("© 2023 Smart Home Dashboard", style={'color': '#ecf0f1'}),
        ]),
    ]),
])


@callback(
    Output("room_brightness", "style"),
    Input('interval-component', 'n_intervals'),
    Input("light_data", "value")
)

def set_brightness_image(n_intervals, value):
    print("NIGGGER")
    return {'filter': f'brightness({int((value * 100) / max_brightness)}%)'}

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
    global count
    global FAN_STATUS
    print(count)
    print(FAN_STATUS)
    if value >= 24 and count == 0:
        count = 1
        print(count)
        print('send email')
        
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
                count = 0
                # return toggle_fan(True)
            else:
                print('Email sent successfully and User said No!') 
                print('change fan status')  
                count = 0
                FAN_STATUS = False
                # return toggle_fan(False)
        else:
            print('Email sending failed!')
            count = 0
            FAN_STATUS = False
            # return toggle_fan(False)
        
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
    global count
    global LED_STATUS
    light_value = int(value)
    # print(light_value)

    if light_value < 400 and count == 0:
        count = 1
        print("Light is ON")
        led.turn_on_led()
        LED_STATUS = True

        current_time = datetime.now().strftime("%H:%M")
        subject = f"The Light is ON at {current_time} time."
        message = f"The light turned on at {current_time} time due to low intensity."

        if send_email(subject, message, sender_email, sender_password, receiver_email):
            print("Email sent successfully")
            # Add a delay to avoid sending multiple emails in a short time
            time.sleep(30)
        else:
            print("Email sending failed!")

    elif light_value >= 400 and count == 1:
        count = 0
        print("Light is OFF")
        led.turn_off_led()
        LED_STATUS = False
    
    return status_LED(LED_STATUS)

# setup_gpio()

def status_LED(LED_STATUS):
    if (LED_STATUS == True):
        return "Status of light: LED is on and Email has been sent"
    else:
        return "Status of light: LED is off"

# Replace this with your actual light intensity reading
# light_intensity_value = 300
# checkIntensity(light_intensity_value)
@callback(
    Output('light_intensity', 'children'),
    Output('light_data', 'value'),
    Input('interval-component', 'n_intervals')
)

def getDatafromArduino(n_intervals):
    msg = subscribe.simple("sensors/light/intensity")
    # print("%s %s" % (msg.topic, msg.payload))
    bytes_val = msg.payload

    str_value = str(bytes_val)
    lenghtOfVal = len(str_value) - 1
    light_value = int(str(bytes_val)[2:lenghtOfVal])

    str_lightvalue = str(light_value)
    # print(light_value)
    return light_value, str_lightvalue

# run app
if __name__ == '__main__':
    app.run(debug=True)