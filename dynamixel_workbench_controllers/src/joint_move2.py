#!/usr/bin/env python3

import sys

import numpy as np
from math import pi
import rospy
from sensor_msgs.msg import JointState
from actionlib.simple_action_client import SimpleActionClient 
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from rospy.topics import Message
from trajectory_msgs.msg import JointTrajectory,JointTrajectoryPoint

from std_msgs.msg import Header



class run_dynamixel:
    def __init__(self):
        
        self.joints_str = JointTrajectory()
        self.joints_str.header = Header()
        self.joints_str.header.stamp = rospy.Time.now()
        self.joints_str.joint_names = ["pan2"]
        self.point = JointTrajectoryPoint()
        l3 = np.array([
                                  [0,0.78]
               
                                   ])
        for indx in range(len(l3[0, :])):
            point= JointTrajectoryPoint(positions= l3[:, indx],
                                        time_from_start= rospy.Duration(0 + 10*indx))
            self.joints_str.points.append(point)
       
    def pub_position(self,arg):
        pub = rospy.Publisher('/dynamixel_workbench/joint_trajectory',JointTrajectory,queue_size=1)
        pub.publish(self.joints_str)
        # rospy.loginfo("command invaito: %s", self.joints_str)
    
    def listener(self):
        rospy.Subscriber('/dynamixel_workbench/joint_states',JointState,self.pub_position)


if __name__ == '__main__':
    try:
        rospy.init_node('pub_to_motor')
        r1 = run_dynamixel()
        r1.listener()
        rospy.spin()
    except:
        rospy.ROSInterruptException
        pass
