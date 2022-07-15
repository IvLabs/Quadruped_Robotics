#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory,JointTrajectoryPoint
from std_msgs.msg import Header
import numpy as np
from quadruped import quadruped

class run_quadruped:

    def __init__(self,loop_points ):
        self.pub = rospy.Publisher('/dynamixel_workbench/joint_trajectory',JointTrajectory,queue_size=100)  
        self.sub = rospy.Subscriber("/dynamixel_workbench/joint_states",JointState , self.subCallBack)
        self.loop_points = loop_points

    def create_traj_msg(self):
            
        joints_str = JointTrajectory()
        joints_str.header = Header()
        joints_str.header.stamp = rospy.Time.now()
        joints_str.joint_names = ["pan1","pan2","pan3","pan4","pan5","pan6","pan7","pan8","pan9","pan10","pan11","pan12"]
        joint_data =np.array(self.loop_points).T
        point = JointTrajectoryPoint()
        for i in range(len(joint_data[0,:])):
            point= JointTrajectoryPoint(positions= joint_data[:,i], 
              time_from_start= rospy.Duration(0.0101*i))                                   
            joints_str.points.append(point)
        return joints_str
    
    def subCallBack(self, arg):
         joint_str = self.create_traj_msg()
         rq.pub.publish(joint_str)
    

if __name__ == "__main__":
    
    try :
        rospy.init_node("run_quad",anonymous=True) 
        rospy.Rate(50)
        quad = quadruped("trot", 0.04, 0, 0.04)
        loop_points = quad.get_loop_points(0.04, 0)
        rq = run_quadruped(loop_points)
        rospy.spin()
    except rospy.ROSInterruptException:
        print("error")
        pass
   
    
