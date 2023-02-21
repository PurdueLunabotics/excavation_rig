# excavation_rig
Purdue Lunabotics Excavation Rig ROS package

Runs on Raspberry PI connected to:
- H-bridge motor controller controlled via PWM
- ADS1115 current feedback sensors connected to + channel of each motor (in series) and interfaced via I2C

Nodes:
- `current_fb_node`
   - Publishers:
     - `current/voltage`: voltage measured by ADC
     - `current/raw`: raw value from ADC [0,65536]
- `motor_control_node`
   - Subscribers:
     - `ctrl/actuation`: speed control [-100,100]
     - `ctrl/excavation`: speed control [-100,100]
- `xbox_control`
   - Subscribers:
     - `joy`: from `joy` ros package
   - Publishers:
     - `ctrl/actuation`: speed control [-100,100]
     - `ctrl/excavation`: speed control [-100,100]
