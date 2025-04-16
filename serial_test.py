import serial
import time
import serial.tools.list_ports

#print available ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)

arduino = serial.Serial('/dev/tty/ACM0', 115200, timeout = 1)
arduino_alt = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)

angle = 180

num_bytes = (angle.bit_length() + 7) // 8

# Convert the integer to bytes in little-endian format
byte_angle = angle.to_bytes(num_bytes, byteorder='little')

if arduino.is_open:
    print("ARDUINO OPEN")
    arduino.write(byte_angle)
    print(f"Sent angle to Arduino: {angle}")

if arduino_alt.is_open:
    print("ARDUINO OPEN")
    arduino_alt.write(byte_angle)
    print(f"Sent angle to Arduino Alt: {angle}")

time.sleep(3)
angle = 90
num_bytes = (angle.bit_length() + 7) // 8

# Convert the integer to bytes in little-endian format
byte_angle = angle.to_bytes(num_bytes, byteorder='little')

if arduino.is_open:
    print("ARDUINO OPEN")
    arduino.write(byte_angle)
    print(f"Sent angle to Arduino: {angle}")

if arduino_alt.is_open:
    print("ARDUINO OPEN")
    arduino_alt.write(byte_angle)
    print(f"Sent angle to Arduino Alt: {angle}")