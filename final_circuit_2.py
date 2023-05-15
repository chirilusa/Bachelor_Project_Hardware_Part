import time
import csv
import board
import Adafruit_DHT
import busio
import digitalio
import adafruit_bmp280
import RPi.GPIO as GPIO
from adafruit_veml6070 import VEML6070


# Set up DHT22
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4


def read_dht22_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return round(temperature, 2), round(humidity, 2)
    else:
        return None, None


# Set up VEML6070
i2c = busio.I2C(board.SCL, board.SDA)
uv = VEML6070(i2c)


def read_veml6070_sensor():
    uv_intensity = uv.uv_raw
    uv_condition = uv.get_index(uv_intensity)
    uv_index = int((uv_intensity * 5) / 1024)
    return uv_index


# Set up BMP280
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
sensor = adafruit_bmp280.Adafruit_BMP280_SPI(spi, cs)

def read_bmp280_sensor():
    temperature_c_bmp = sensor.temperature
    pressure_hpa = sensor.pressure
    return round(temperature_c_bmp, 2), round(pressure_hpa, 2)


# Set up rain sensor
rain_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(rain_pin, GPIO.IN)


def read_rain_sensor():
    if GPIO.input(rain_pin):
        return 0
    else:
        return 1


def write_data_to_csv(filename, timestamp, temperature, humidity, uv_index, temperature_c_bmp, pressure_hpa, rain):
    with open(filename, mode='a') as file:
        file.write('{},{:.2f},{:.2f},{},{:.2f},{:.2f},{}\n'.format(timestamp, temperature, humidity, uv_index, temperature_c_bmp, pressure_hpa, rain))


def clear_csv_file(filename):
    with open(filename, mode='w') as file:
        file.write('Timestamp,DHT22 temperature (C),DHT22 humidity (%),VEML6070 UV index,BMP280 temperature (C),BMP280 pressure (hPa),Rain\n')


def main():
    filename = 'sensor_data.csv'
    clear_csv_file(filename)
    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        # Citire senzor DHT22 
        temperature, humidity = read_dht22_sensor()

        # Citire senzor VEML6070 
        uv_index = read_veml6070_sensor()

        # Citire senzor BMP280 
        temperature_c_bmp, pressure_hpa = read_bmp280_sensor()

        # Citire senzor de ploaie 
        rain = read_rain_sensor()

        # Scrierea informațiilor în fișier
        write_data_to_csv(filename, timestamp, temperature, humidity, uv_index, temperature_c_bmp, pressure_hpa, rain)

        print("Temp={:.2f}*C  Humidity={:.2f}% UV Index={} BMP Temp={:.2f} BMP Press={:.2f} Rain={}".format(temperature, humidity, uv_index, temperature_c_bmp, pressure_hpa, rain))

        # Wait before taking another reading
        time.sleep(5)


if __name__ == '__main__':
    main()
