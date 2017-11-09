# tdt4113-gr39-pr6

## Communication Protocol
In this section, we specify the different inputs and outputs from the sensobs and motobs.
### Sensobs:
* IR_Proximity Sensob:  
  * get_value() returns a tuple with (left_value, right_value). Both left_value and right_value are boolean (True or False)
* Path_Choice Sensob (Camera): 
  * Specify format for camera data being transmitted to the behaviour here

### Motor recommendations:
The motor reccomendations being transferred to the motobs is on the following format:
* (Mode, rotation_degrees)  
  * Here, Mode is either rotate (DriveMode.ROTATE) or drive (DriveMode.DRIVE). 
Rotation_degrees is positive for counterclockwise rotation and negative for clockwise rotation. It is measured in degrees
