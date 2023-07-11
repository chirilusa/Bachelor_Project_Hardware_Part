import csv
import time
import board
import busio
import adafruit_veml6070

i2c = busio.I2C(board.SCL, board.SDA)

# Open the CSV file and write the header row
with open('uv_data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'UV Intensity', 'UV Condition', 'UV Index'])

with board.I2C() as i2c:
    uv = adafruit_veml6070.VEML6070(i2c)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    for i in range(20):
        # UV Intensity is the 16-bit value read from the sensor.
        uv_intensity = uv.uv_raw
        uv_condition = uv.get_index(uv_intensity)
        uv_index = int((uv_intensity * 5) / 1024)

        print('UV Intensity: {0}  UV Condition: {1}  UV Index: {2}'.format(uv_intensity, uv_condition, uv_index))
        time.sleep(2)

        with open('uv_data.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, uv_intensity, uv_condition, uv_index])
