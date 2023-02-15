#!/usr/bin/env python3
import rospy
import numpy as np
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64


def constrain(joy_in):
    return np.int8(min(joy_in * 128,127))

class ManualController:
    def __init__(self):
        self._joy_sub = rospy.Subscriber('joy', Joy, self.joy_cb);
        self._exc_ctrl_pub = rospy.Publisher('ctrl/excavation', Float64, queue_size=1);
        self._act_ctrl_pub = rospy.Publisher('ctrl/actuation', Float64, queue_size=1);
        self._exc_ctrl_msg = Float64()
        self._act_ctrl_msg = Float64()

    def joy_cb(self, joy):
        if joy.buttons[1]: # 'B' button
            self.stop()
            rospy.loginfo("STOPPED")
        else:
            # Joysticks
            self._exc_ctrl_msg.data = joy.axes[1] * 100
            self._act_ctrl_msg.data = joy.axes[4] * 100

    def loop(self):
        self._exc_ctrl_pub.publish(self._exc_ctrl_msg)
        self._act_ctrl_pub.publish(self._act_ctrl_msg)

    def stop(self):
        self._exc_ctrl_msg.data = 0
        self._act_ctrl_msg.data = 0

if __name__ == '__main__':
    rospy.init_node('manual_controller_node')

    man_ctrl = ManualController()
    r = rospy.Rate(20)

    def shutdown_hook():
        print('stopping manual control')
        man_ctrl.stop()

    rospy.on_shutdown(shutdown_hook)

    while not rospy.is_shutdown():
        man_ctrl.loop()
        r.sleep()
