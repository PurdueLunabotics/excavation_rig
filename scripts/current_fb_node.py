#!/usr/bin/env python3

import rospy
import time

from std_msgs.msg import Float64

import ADS1x15

# topics
act_topic = 'actuation'
exc_topic = 'excavation'

exc_ads_id = 2
act_ads_id = 3 

# initialize ADS1115 on I2C bus 1 with default address 0x48
addr = 0x48 # bus address

if __name__ == '__main__':

    rospy.init_node('rig_current_fb_node')

    ADS = ADS1x15.ADS1115(1, addr)
    ADS.setGain(0)
    f = ADS.toVoltage()

    act_raw_pub = rospy.Publisher(f'current/{act_topic}/raw',Float64,queue_size=10)
    act_vol_pub = rospy.Publisher(f'current/{act_topic}/voltage',Float64,queue_size=10)

    exc_raw_pub = rospy.Publisher(f'current/{exc_topic}/raw',Float64,queue_size=10)
    exc_vol_pub = rospy.Publisher(f'current/{exc_topic}/voltage',Float64,queue_size=10)

    r = rospy.Rate(50) # 50hz
    while not rospy.is_shutdown():
        exc_adc_val = ADS.readADC(exc_ads_id)
        act_adc_val = ADS.readADC(act_ads_id)

        exc_raw_pub.publish(exc_adc_val)
        exc_vol_pub.publish(exc_adc_val * f)

        act_raw_pub.publish(act_adc_val)
        act_vol_pub.publish(act_adc_val * f)

        r.sleep()
