import board
import digitalio
import adafruit_bmp280
import time
import csv

#Set up the SPI communication using the default SPI pins (MOSI, MISO, and SCLK)
spi = board.SPI()

#Creates a DigitalInOut object named cs to represent the Chip Select (CS) pin for the BMP280
cs = digitalio.DigitalInOut(board.D5)

#Take the spi and cs objects as arguments to establish the SPI communication and specify the Chip Select pin
sensor = adafruit_bmp280.Adafruit_BMP280_SPI(spi, cs)
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
print('Temperature: {} °C'.format(sensor.temperature)) 
print('Pressure: {}hPa'.format(sensor.pressure))