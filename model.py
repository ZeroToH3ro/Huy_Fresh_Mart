import sys
sys.path.append('/usr/lib/python3/dist-packages')
from picamera2 import Picamera2, Preview
import time
import cv2
from ultralytics import YOLO
import RPi.GPIO as GPIO
import serial
import requests
from requests.exceptions import RequestException, Timeout
from pyzbar import pyzbar
import numpy as np

# Initialize YOLO model
model = YOLO("/home/huy/GDP/DOANTOTNGHIEP_2/code/Code RasPi4/Raspberry pi/runs/detect/train/weights/best.pt")

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Disable warnings

# Define GPIO pins
button_capture_pin = 17
button_barcode_pin = 22
button_send_pin = 27
switch_pin = 22
led1_pin = 12
led2_pin = 16
led3_pin = 26
buzzer_pin = 5

# Setup GPIO pins
GPIO.setup(button_capture_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_send_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_barcode_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led1_pin, GPIO.OUT)
GPIO.setup(led2_pin, GPIO.OUT)
GPIO.setup(led3_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Initialize camera
camera = Picamera2()
camera_config = camera.create_still_configuration(
    main={"size": (2592, 1944)},
    lores={"size": (640, 480)}
)
camera.configure(camera_config)
camera.start()
time.sleep(2)  # Give camera time to warm up

# Initialize variables
last_result = None
button_pressed = False
product_id = None
loadcell_value = None
COLOR = False

try:
    while True:
        # Capture image button
        if GPIO.input(button_capture_pin) == GPIO.HIGH:
            print("Button 1 on.")
            GPIO.output(led1_pin, GPIO.HIGH)

            # Capture and save image
            camera.capture_file("capture.jpg")
            image = cv2.imread("capture.jpg")

            # YOLO detection
            results = model.predict(source=image, save=True)

            if results:
                highest_confidence = -1
                for result in results:
                    boxes = result.boxes
                    if boxes:
                        for box in boxes:
                            conf = box.conf[0]
                            if conf > highest_confidence:
                                highest_confidence = conf
                                product_id = int(box.cls[0])

                if product_id is not None:
                    print(f"Label: {product_id}, Confidence: {highest_confidence:.2f}")
                    try:
                        ser = serial.Serial('/dev/serial0', 9600)
                        loadcell_value = ser.readline().decode('utf-8').strip()
                        ser.close()
                        print(f"Loadcell value: {loadcell_value}")
                    except serial.SerialException as e:
                        print(f"Serial port error: {e}")

            GPIO.output(led1_pin, GPIO.LOW)
            GPIO.output(led2_pin, GPIO.LOW)
            time.sleep(0.5)

        # Barcode reading button
        button_state = GPIO.input(button_barcode_pin)
        if button_state == GPIO.LOW:
            if not button_pressed:
                print("Button 2 on.")
                GPIO.output(led3_pin, GPIO.HIGH)
                button_pressed = True

                # Capture and process frame for barcode
                frame = camera.capture_array()
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                barcodes = pyzbar.decode(gray_frame)

                for barcode in barcodes:
                    loadcell_value = 1
                    barcodeData = barcode.data.decode("utf-8")
                    product_id = barcodeData
                    print(f"Barcode: {product_id}")

                    if product_id:
                        GPIO.output(buzzer_pin, GPIO.HIGH)
                        time.sleep(0.5)
                        GPIO.output(buzzer_pin, GPIO.LOW)

                        # Send HTTP request
                        try:
                            api_url = f"http://127.0.0.1:8000/api?id={product_id}&loadcellValue={loadcell_value}"
                            response = requests.get(api_url)
                        except RequestException as e:
                            print(f"API request error: {e}")

                time.sleep(3)
        else:
            if button_pressed:
                print("Button 2 released.")
                GPIO.output(led3_pin, GPIO.LOW)
                GPIO.output(led1_pin, GPIO.LOW)
                button_pressed = False

        # Send data button
        if GPIO.input(button_send_pin) == GPIO.LOW:
            print("Sending data...")
            if product_id is not None and loadcell_value is not None:
                GPIO.output(buzzer_pin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(buzzer_pin, GPIO.LOW)

                try:
                    api_url = f"http://127.0.0.1:8000/api?id={product_id}&loadcellValue={loadcell_value}"
                    response = requests.get(api_url)
                    product_id = None
                    print("Data sent successfully")
                except RequestException as e:
                    print(f"API request error: {e}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram terminated by user")
finally:
    # Cleanup
    GPIO.cleanup()
    camera.stop()
    print("Cleanup completed")