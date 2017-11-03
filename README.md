# tdt4113-gr39-pr6

## Communication Protocol
In this section, we specify the different inputs and outputs from the sensobs and motobs.
### Sensobs:
- IR_Proximity Sensob:
-- get_value() returns a tuple with (left_value, right_value). Both left_value and right_value are boolean (True or False)
- Path_Choice Sensob (Camera):
-- Specify format for camera data being transmitted to the behaviour here

### Motor recommendations:
The motor reccomendations being transferred to the motobs is on the following format:
* (Mode, rotation_degrees, [speed])
Here, Mode is either rotate (R) or drive (D). 
Rotation_degrees is positive for counterclockwise rotation and negative for clockwise rotation. It is measured in degrees
In drive mode, a third parameter speed is given. This is positive for forward driving and negative for reverse.
The speed is in percent of max-speed and is a number between -1 and 1.
