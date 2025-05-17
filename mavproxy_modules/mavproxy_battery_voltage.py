from MAVProxy.modules.lib import mp_module
from pymavlink.dialects.v20 import ardupilotmega as mavlink2
import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115, P0
from adafruit_ads1x15.analog_in import AnalogIn
import threading


class BatteryVoltageModule(mp_module.MPModule):

    def __init__(self, mpstate):
        super(BatteryVoltageModule, self).__init__(
            mpstate, "batteryvoltage", "Send battery status via MAVLink"
        )

        # Setup I2C and ADC
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS1115(i2c)
        ads.gain = 1
        self.chan = AnalogIn(ads, P0)

        # Voltage divider
        R1 = 15600
        R2 = 5600
        self.divider_ratio = (R1 + R2) / R2

        # Start thread
        self.running = True
        self.thread = threading.Thread(target=self.loop)
        self.thread.daemon = True
        self.thread.start()

    def loop(self):
        while self.running:
            try:
                measured_voltage = self.chan.voltage
                battery_voltage = measured_voltage * self.divider_ratio
                voltage_mv = int(battery_voltage * 1000)

                print(f"Battery voltage: {voltage_mv}mV")

                self.master.mav.battery_status_send(
                   id=1,
                   battery_function=0,
                   type=mavlink2.MAV_BATTERY_TYPE_LIPO,
                   temperature=0,
                   voltages=[11000] + [0] * 9,
                   current_battery=-1,
                   current_consumed=0,
                   energy_consumed=-1,
                   battery_remaining=-1,
                )
            except Exception as e:
                print(f"[batteryvoltage] Error: {e}")

            time.sleep(1)

    def unload(self):
        self.running = False
        self.thread.join()


def init(mpstate):
    return BatteryVoltageModule(mpstate)
