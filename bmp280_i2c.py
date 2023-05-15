import board
import busio
import adafruit_bmp280
import time
import csv

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

# with open('bmp280_data.csv', 'w') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Timestamp', 'Temperature (C)', 'Pressure (hPa)'])

while True:
    temperature = round(sensor.temperature, 2)
    pressure = round(sensor.pressure, 2)
    print("Temperature: " + str(temperature) + " °C")
    print("Pressure: " + str(pressure) + " hPa")

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open('bmp280_data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, temperature, pressure])
    time.sleep(2)