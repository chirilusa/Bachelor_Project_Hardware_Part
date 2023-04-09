import csv
import time
from time import sleep
import Adafruit_DHT

# Define the sensor and pin
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# Open the CSV file and write the header row
with open('dht22_data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Temperature (C)', 'Humidity (%)'])

# Read data from the sensor and append to CSV file every 10 seconds

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")

    with open('dht22_data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, round(temperature,2), round(humidity,2)])
    sleep(2)