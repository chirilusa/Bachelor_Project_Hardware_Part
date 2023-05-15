import time
from time import sleep
import csv
import board
import Adafruit_DHT
import busio
import adafruit_bmp280
import RPi.GPIO as GPIO
from adafruit_veml6070 import VEML6070

# Set up DHT22
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# Set up VEML6070 
# busio.I2C initializes an I2C object from the busio library
# board.SCL and board.SDA are constants that represent the GPIO pins on the Raspberry Pi
i2c = busio.I2C(board.SCL, board.SDA) 
uv = VEML6070(i2c)

# Set up BMP280
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

# Set up rain sensor
rain_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(rain_pin, GPIO.IN)

# Open file for writing sensor data
#filename = 'sensor_data.csv'
with open(filename, mode='w') as file:
    file.write('Timestamp,DHT22 temperature (C),DHT22 humidity (%),VEML6070 UV index,BMP280 temperature (C),BMP280 pressure (hPa),Rain\n')

while True:

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # Read DHT22 sensor
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    # Read VEML6070 sensor
    uv_intensity = uv.uv_raw
    uv_condition = uv.get_index(uv_intensity)
    uv_index = int((uv_intensity * 5) / 1024)

    # Read BMP280 sensor
    temperature_c_bmp = bmp280.temperature
    pressure_hpa = bmp280.pressure

    # Read rain sensor
    if GPIO.input(rain_pin):
         rain = 0
    else:
         rain = 1

     # Write sensor data to file
    with open(filename, mode='a') as file:
         file.write('{},{:.2f},{:.2f},{},{:.2f},{:.2f},{}\n'.format(timestamp, temperature, humidity, uv_index, temperature_c_bmp, pressure_hpa, rain))

      # Wait before taking another reading
    time.sleep(5)