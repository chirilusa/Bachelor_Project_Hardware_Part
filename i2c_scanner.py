import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
    pass

devices = i2c.scan()

for device in devices:
    print("Found device at address: 0x{:02X}".format(device))

i2c.unlock()
