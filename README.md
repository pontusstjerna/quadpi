# QuadPi

This is a small repo for my completely autonomous drone running ArduPilot using a compantion raspberry pi zero computer.

## Current setup

- FC: Sparky2 (old as hell)
- Motors: MR2205-2750KV RACER EDITION
- Esc: BL_Heli Multistar 4-in-1
- Props: 3-blade 5045
- Frame: Modified version of this with added GPS and Rpi zero case: https://makerworld.com/en/models/411258-3d-printable-5-inch-drone-frame

Tech stack is very simple. FC runs ArduCopter with a Raspberry Pi Zero 2 running Mavproxy connected with serial. No RC involved at all.

For voltage reading, I have soldered a voltage divider directly to my LiPo input (using 3S 11.1v) that is connected to an ADS1115 ADC to read battery voltage. This is then sent through Mavproxy to my FC since Sparky2 doesn't have any integrated ADC.
