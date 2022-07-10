#!/usr/bin/env python3
import sys
sys.path.insert(0,r'/home/yaswanth/catkin_ws/src/dynamixel-workbench/dynamixel_workbench_controllers/src/test')


from numpy.core.numeric import True_

import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
#from actionlib.simple_action_client SimpleActionCli
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory,JointTrajectoryPoint
from std_msgs.msg import Header
import numpy as np
from traj import trajectory_generator
from math import pi
leg1= trajectory_generator( 0.9, 0, 0.1, 0.13, 50,0,0)
leg2= trajectory_generator( 0.9, 0, 0.1, 0.13, 50,2,-0.436)
leg3= trajectory_generator( 0.9, 0, 0.1, 0.13, 50,2,-0.349)
leg4= trajectory_generator( 0.9, 0, 0.1, 0.13, 50,0,1.39)
l1ang_1,l1ang_2,l1ang_3=leg1.anglist()
l2ang_1,l2ang_2,l2ang_3=leg2.anglist()
l3ang_1,l3ang_2,l3ang_3=leg3.anglist()
l4ang_1,l4ang_2,l4ang_3=leg4.anglist()


def create_traj_msg():
            
        joints_str = JointTrajectory()
        joints_str.header = Header()
        joints_str.header.stamp = rospy.Time.now()
        # joints_str.joint_names = ["pan4","pan5","pan6"]
        joints_str.joint_names = ["pan1","pan2","pan3","pan4","pan5","pan6","pan7","pan8","pan9","pan10","pan11","pan12"]
        #joint_data = (pi/180)*np.array([ [30,60] , [30,60] , [30,60]   ])"l1ang_1,l1ang_2,l1ang_3,l2ang_1,l2ang_2,l2ang_3,
        # joint_data =np.array([l1ang_1,l1ang_2,l1ang_3]),,"pan9",,l4ang_1,l4ang_2,l4ang_3l3ang_,
        joint_data =np.array([l1ang_1,l1ang_2,l1ang_3,l2ang_1,l2ang_2,l2ang_3,l3ang_1,l3ang_2,l3ang_3,l4ang_1,l4ang_2,l4ang_3])
        point = JointTrajectoryPoint()
        for i in range(len(joint_data[0, :])):
            point= JointTrajectoryPoint(positions= joint_data[:,i], 
                                                     time_from_start= rospy.Duration(0.05*i))                                       
            joints_str.points.append(point)
        return joints_str

def pubsh(arg):   
    joints_st = create_traj_msg()   
    pub = rospy.Publisher('/dynamixel_workbench/joint_trajectory',JointTrajectory,queue_size=1)  
    time = rospy.get_time()
    pub.publish(joints_st)        
    
def listener():
   rospy.Subscriber("/dynamixel_workbench/joint_states",JointState , pubsh)
    

if __name__ == '__main__':
    try :
        rospy.init_node("jointmove",anonymous=True)   
        listener()      
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
