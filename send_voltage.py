from pymavlink import mavutil
import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115, P0
from adafruit_ads1x15.analog_in import AnalogIn

master = mavutil.mavlink_connection("tcp:127.0.0.1:5761")

# Setup I2C and ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)
ads.gain = 1  # ±4.096V input range


# Voltage divider resistors
R1 = 15600  # 10k ohm
R2 = 5600  # 5.6k ohm
divider_ratio = (R1 + R2) / R2  # = ~2.786

# Read from channel A0
chan = AnalogIn(ads, P0)

master.wait_heartbeat()
print(f"Heartbeat from system (system {master.target_system} component {master.target_component})")

while True:
    measured_voltage = chan.voltage  # Voltage at A0
    battery_voltage = measured_voltage * divider_ratio

    print(
        f"ADC: {chan.value} | A0 Voltage: {measured_voltage:.2f} V | Battery: {battery_voltage:.2f} V"
    )

    voltage_mv = int(battery_voltage * 1000)
    master.mav.battery_status_send(
        id=1,
        battery_function=0, # all
        type=3, # lipo
        temperature=0,
        voltages=[voltage_mv] + [0] * 9,
        current_battery=-1,
        current_consumed=-1,
        energy_consumed=-1,
        battery_remaining=-1,
    )
    time.sleep(1)
