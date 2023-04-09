import time
import board
import adafruit_dht
import busio
import adafruit_veml6070
import adafruit_bmp280
import RPi.GPIO as GPIO

# Set up DHT22
dht_pin = 4
dht_device = adafruit_dht.DHT22(dht_pin)

# Set up VEML6070 
# busio.I2C initializes an I2C object from the busio library
# board.SCL and board.SDA are constants that represent the GPIO pins on the Raspberry Pi
i2c = busio.I2C(board.SCL, board.SDA) 
uv = adafruit_veml6070.VEML6070(i2c)

# Set up BMP280
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Set up rain sensor
rain_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(rain_pin, GPIO.IN)

# Open file for writing sensor data
filename = 'sensor_data.csv'
with open(filename, mode='w') as file:
    file.write('Timestamp,DHT22 temperature (C),DHT22 humidity (%),VEML6070 UV index,BMP280 temperature (C),BMP280 pressure (hPa),Rain\n')

while True:
    try:
        # Read DHT22 sensor
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity

        # Read VEML6070 sensor
        uv_index = uv.uv_index

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
            file.write('{},{:.2f},{:.2f},{},{:.2f},{:.2f},{}\n'.format(time.time(), temperature_c, humidity, uv_index, temperature_c_bmp, pressure_hpa, rain))

        # Wait before taking another reading
        time.sleep(5)

    # except RuntimeError as e:
    #     # Errors happen fairly often, DHT's are hard to read, just keep going
    #     print('Error reading DHT22: ', e.args[0])
    #     time.sleep(5)
    #     continue
    # except Exception as e:
    #     # Other errors happen less often, make sure to clean up
    #     print('Error: ', e)
    #     GPIO.cleanup()
    #     break
