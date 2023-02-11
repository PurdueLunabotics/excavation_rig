#!/usr/bin/env python3

import rospy
import time

from std_msgs.msg import Float64
import RPi.GPIO as GPIO

# topics
act_topic = 'actuation'
exc_topic = 'excavation'

exc_ctrl = 0
act_ctrl = 0

def act_cb(msg):
    global act_ctrl
    act_ctrl = msg.data

def exc_cb(msg):
    global exc_ctrl
    exc_ctrl = msg.data

class Motor:
    def __init__(self,pwm_p,dir_p):
        self.dir_p = dir_p
        self.pwm_p = pwm_p

        GPIO.setup(self.dir_p, GPIO.OUT)
        GPIO.setup(self.pwm_p, GPIO.OUT)

        self.pwm_h = GPIO.PWM(self.pwm_p, 10000)
        self.pwm_h.start(0)

        self.speed = 0

    def set_speed(self,speed): #speed goes from -100 to 100
        if(speed == self.speed):
            return
        direction = False if speed > 0 else True
        speed = abs(speed)
        GPIO.output(self.dir_p,direction)
        self.pwm_h.ChangeDutyCycle(speed)
        self.speed = speed

    def cleanup(self):
        self.pwm_h.stop()

if __name__ == '__main__':

    rospy.init_node('rig_current_fb_node')
    act_sub = rospy.Subscriber(f'ctrl/{act_topic}', Float64,act_cb)
    exc_sub = rospy.Subscriber(f'ctrl/{exc_topic}', Float64,exc_cb)

    GPIO.setmode(GPIO.BOARD)

    m_act = Motor(33,35)
    m_exc = Motor(31,29)

    def shutdown_hook():
        print('shutting down')
        m_act.cleanup()
        m_exc.cleanup()

    rospy.on_shutdown(shutdown_hook)

    print('initialized motors')
    r = rospy.Rate(50) # 50hz
    while not rospy.is_shutdown():
        m_act.set_speed(act_ctrl)
        m_exc.set_speed(exc_ctrl)
        r.sleep()
