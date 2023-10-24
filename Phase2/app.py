from dash import Dash, html, callback, Input, Output, dcc
import RPi.GPIO as GPIO
import time
from time import sleep
import Freenove_DHT as DHT
# import board

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import email
import imaplib

# Setup LED 
# led_pin = 11
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(led_pin, GPIO.OUT)
# GPIO.output(led_pin, GPIO.LOW) 
# GPIO.setwarnings(False)

# Setup DHT11
# DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 11 # GPIO pin for DHT sensor
FAN_STATUS = False # Initially, fan is off

humidity = 0
temperature = 0 

# Email Information
subject = 'Check Temp'
message = 'The current temperature is ***. Would you like to turn on the fan?'

smtp_server = 'smtp.gmail.com'
sender_email = 'cookiecove8@gmail.com'
sender_password = 'skfp plbw ttkw xaip'
receiver_email = 'baduar10@gmail.com'

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Practicing Dash'),
    
    html.Div(children=[
        html.Div(children='Phase 1'),
        # daq.ToggleSwitch(id="click-light", on=False),
        html.Img(src='assets/images/LightOff.PNG', id='img_light', width="100", height="100"),
    ]),
    html.Button('Switch Light', id='click_light', n_clicks=0),

    html.Br(),
    html.Br(),

    html.Div([
        # daq.ToggleSwitch(id="click-light", on=False),
        # html.Img(src='assets/images/LightOff.PNG', id='img_light', width="100", height="100"),
        html.Div(children='Phase 2'),
        html.P("Press Button below to send email about temperature!"),
        html.Div(children='status email', id='status_email_sent')
    ]),
    html.Button('Send Email', id='sending_email', n_clicks=0),

    html.Br(),
    html.Br(),

    html.H1('DHT11 Sensor Data'),
    html.Div([
        html.Div("Humdity: ", id='humidity'),
        html.Div("Temperature: ", id='temperature'),
    ]),
    dcc.Interval(id='interval-component', interval=3*1000, n_intervals=0),
])

# Phase 1
# @callback(
#     Output("img_light", "src"),
#     Input("click_light", "n_clicks")
# )

# def click_counter(n_clicks):
#     return f"The html.Div above has been clicked this many times: {n_clicks}"

# def toggle_led(n_clicks):
#     if GPIO.input(led_pin) == GPIO.LOW:
#         GPIO.output(led_pin, GPIO.HIGH)
#         return 'assets/images/LightOn.PNG'
#     elif GPIO.input(led_pin) == GPIO.HIGH:
#         GPIO.output(led_pin, GPIO.LOW)
#         return 'assets/images/LightOff.PNG'

# Phase 2
@callback(
    Output("status_email_sent", "children"),
    Input("sending_email", "n_clicks")
)

def sending_email(n_clicks):
    if send_email(subject, message, sender_email, sender_password, receiver_email) == True:
        print("wait a bit")
        time.sleep(30)
        print("proceed to read email")
        if receive_email() == True:
            return 'Email sent successfully and User said Yes!'
        else:
            return 'Email sent successfully and User said No!'
    else:
        return 'Email sending failed!'

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
                    return True
                else:
                    print("User declined")
                    return False
    imap.close()

@callback(
    # Output("status_email_sent", "children"),
    # Input("HumiTemp_read", "n_clicks")
    Output('humidity', 'children'),
    Output('temperature', 'children'),
    Input('interval-component', 'n_intervals')
)

# def update_sensor_data(n_intervals):
#     humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
#     if humidity is not None and temperature is not None:
#         return f'Humidity: {humidity:.2f}%', f'Temperature: {temperature:.2f}°C'
#     else:
#         return 'Failed to read data', 'Failed to read data'
    
# def read_temperature_humidity():
#     humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
#     return humidity, temperature

def update_sensor_data(n_intervals):
    dht = DHT.DHT(DHT_PIN)
    for i in range(0,15):
        chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            print("DHT11,OK!")
            break
    print(f'Humidity: {dht.humidity:.2f}%')
    print(f'Temperature: {dht.temperature:.2f}°C')
    return f'Humidity: {dht.humidity:.2f}%', f'Temperature: {dht.temperature:.2f}°C'

# run app
if __name__ == '__main__':
    app.run(debug=True)