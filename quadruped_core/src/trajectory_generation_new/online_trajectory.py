#! usr/bin/env python3
from math import *
from matplotlib import pyplot as plt
import sys
from mpl_toolkits import mplot3d




from k_engine.ik_s3r import in_kin as kinematics
 
class trajectory_generator():
 """ A class that generates the trajectory for the gait of the quadruped
 
 Attributes:
    vx:
    vz: 
    vy:
    leg_heigh: Height of the quafruped's leg.
    f_hard: frequency 
    f_gate: f_gate 
    n: 
    x0, y0: x[0] and y[0] trajectory cordinates
    x1, y1: x[1] and y[1] trajectory cordinates
    cord: trajectory coordinate (x,y,z)
    flag: flag
"""

    def __init__(self , vx , vy , vz , leg_height , f_hard, n):
        self.vx = vx
        self.vz = vz
        self.vy = vy
        self.leg_height = leg_height
        self.f_hard = f_hard
        self.f_gate = 4
        self.n = n
        self.x0 , self.y0 = 0,0
        self.x1 = self.x0 +  self.vx/(2*self.f_gate)
        self.y1 = self.y0 +  self.vy/(2*self.f_gate)
        self.cord = [ self.x0 ,self.y0, 0]
        self.flag = 1

    def get_next( self):
    """ This method return next trajectory coordinate 
 
    Returns:
      cord: Next trajectory cordinate
    """
        n_max=int(self.f_hard/(2*self.f_gate))
        if n_max<=self.n:
            r=int(self.n/n_max)
            self.n=self.n-r*n_max
            self.flag=-1*self.flag
            if( self.flag == -1 ):
                #print("yes")
                self.update_vx_vy()
            self.swap();


        time_left = ( (1/(2*self.f_gate))  - ( self.n/self.f_hard) ) 
        if time_left >= 0 :
            self.cord[0] = (self.cord[0] +  ( (self.x1 - self.cord[0])/time_left    )/self.f_hard )
            self.cord[1] = self.cord[1] +  ( (self.y1 - self.cord[1])/time_left    )/self.f_hard 
            self.cord[2] =   0.5*(self.flag + 1)* (self.vz/self.f_gate) * sin( (pi*self.n*2*self.f_gate)/(self.f_hard) )
            self.cord[2] = self.leg_height - self.cord[2]
            # self.cord[0] = self.cord[0] - self.x1/2
            # self.cord[1] = self.cord[1] - self.y1/2
            # print(self.cord[0],self.n,time_left)

        if(abs(time_left) < (1/self.f_hard) ):
            self.flag = self.flag * -1 
            if( self.flag == -1 ):
                #print("yes")
                self.update_vx_vy()
            self.swap();
            self.n = 0
        else:
            self.n += 1

        return self.cord

    def swap(self):
    """ This method swaps the x0, y0 and x1, y1. 
    """
        self.x1 , self.y1 , self.x0 , self.y0 = self.x0 , self.y0 , self.x1 , self.y1

    def update_vx_vy(self):

        self.x1 = self.x0 +  self.vx/(2*self.f_gate) 
        self.y1 = self.y0 +  self.vy/(2*self.f_gate)


if __name__ == "__main__":

    f_hard = 100
    tg = trajectory_generator( 0.1, 0, 0.1, 0.1,f_hard,0)

    x_cor ,y_cor , z_cor = [] , [] , []
    ang_1, ang_2, ang_3 = [], [], []
    x_f ,y_f , z_f = [] , [] , []   
    t=[] 
    leg = kinematics()
    
    
    for i in range(f_hard):
        x, y, z = tg.get_next()
        x_cor.append(x)
        y_cor.append(y)
        z_cor.append(z)

        # t1 ,t2, t3 = leg.ik(z,y,x)
        # ang_1.append(t1)
        # ang_2.append(t2)
        # ang_3.append(t3)
        
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(3)
    axs[0].plot(x_cor)
    axs[1].plot(z_cor) 
    axs[2].plot(x_cor,z_cor)
    plt.show()

    # fig, axs = plt.subplots(3, 2)
    # axs[0, 0].plot(ang_1)
    # axs[0, 0].set_title('angle 1')
    # axs[0, 1].plot(ang_2)
    # axs[0, 1].set_title('angle 2')
    # axs[1, 0].plot(ang_3)
    # axs[1, 0].set_title('angle 3')
    # axs[1, 1].plot(x_cor,z_cor)
    # axs[1, 1].set_title('x,z')
    # axs[2, 0].plot(z_cor)
    # axs[2, 0].set_title('z')
    # axs[2, 1].plot(x_cor)
    # axs[2, 1].set_title('x')
    # plt.show()
        
