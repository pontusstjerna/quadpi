import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115, P0
from adafruit_ads1x15.analog_in import AnalogIn

# Setup I2C and ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)
ads.gain = 1  # ±4.096V input range


# Voltage divider resistors
R1 = 15600  # 10k ohm
R2 = 5600   # 5.6k ohm
divider_ratio = (R1 + R2) / R2  # = ~2.786

# Read from channel A0
chan = AnalogIn(ads, P0)

while True:
  measured_voltage = chan.voltage  # Voltage at A0
  battery_voltage = measured_voltage * divider_ratio


  print(f"ADC: {chan.value} | A0 Voltage: {measured_voltage:.2f} V | Battery: {battery_voltage:.2f} V")
  time.sleep(2)
