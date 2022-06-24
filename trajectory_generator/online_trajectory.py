#! usr/bin/env python3
from math import *
from matplotlib import pyplot as plt
import sys


from s3r_kin import kinematics
 
class trajectory_generator():

    def __init__(self , vx , vy , vz , leg_height , f_hard):
        self.vx = vx
        self.vz = vz
        self.vy = vy
        self.leg_height = leg_height
        self.f_hard = f_hard
        self.f_gate = 2 
        self.n = 0
        self.x0 , self.y0 = 0 , 0
        self.x1 = self.x0 +  self.vx*2/self.f_gate 
        self.y1 = self.y0 +  self.vy*2/self.f_gate
        self.cord = [ self.x0 ,self.y0, 0]
        self.flag = 1

    def get_next( self):

        time_left = ( (2/self.f_gate)  - ( self.n/self.f_hard)   ) 
        if time_left > 0 :
            self.cord[0] = self.cord[0] +  ( (self.x1 - self.cord[0])/time_left    )/self.f_hard 
            self.cord[1] = self.cord[1] +  ( (self.y1 - self.cord[1])/time_left    )/self.f_hard 
            self.cord[2] =   0.5*(self.flag + 1)* (self.vz/self.f_gate) * sin( (pi*self.n*self.f_gate)/(2*self.f_hard) )
            self.cord[2] = self.leg_height - self.cord[2]
            # print( self.cord)

        if(abs(time_left) <= (1/self.f_hard) ):
            self.flag = self.flag * -1 
            if( self.flag == -1 ):
                self.update_vx_vy()
            self.swap();
            self.n = 0 
        else  :
            self.n += 1
        

        return self.cord ;

    def swap(self):
        self.x1 , self.y1 , self.x0 , self.y0 = self.x0 , self.y0 , self.x1 , self.y1

    def update_vx_vy(self):

        self.x1 = self.x0 +  self.vx*2/self.f_gate 
        self.y1 = self.y0 +  self.vy*2/self.f_gate


if __name__ == "__main__":

    tg = trajectory_generator( 0.25 , 0.25 , 0.25 , 0.4 , 100)

    x_cor ,y_cor , z_cor = [] , [] , []
    ang_1, ang_2, ang_3 = [], [], []
    x_f ,y_f , z_f = [] , [] , []    

    leg = kinematics()
    
    for _ in range(200):
        x, y, z = tg.get_next()
        x_cor.append(x)
        y_cor.append(y)
        z_cor.append(z)

        t1 ,t2, t3 = leg.ik(x,y,z)
        ang_1.append(t1)
        ang_2.append(t2)
        ang_3.append(t3)
        
        p, q, r = leg.fk(t1, t2, t3)
        
        x_f.append(p)
        y_f.append(q)
        z_f.append(r)
        
    
    # import matplotlib.pyplot as plt

    plt.title("traj x vs traj z")
    plt.plot(x_cor , z_cor)
    plt.show()
    
    plt.title("xf vs zf")
    plt.plot(x_f , z_f)
    plt.show()
    # plt.title("y vs z")

    # plt.plot(y_cor , z_cor)
    # plt.show()

    plt.title("traj x")
    plt.plot(x_cor )
    plt.show()
    
    plt.title("traj z")
    plt.plot(z_cor)
    plt.show()

    
    plt.title("theta_1")
    plt.plot(ang_1 )
    plt.show()

    plt.title("theta_2")
    plt.plot(ang_2 )
    plt.show()

    plt.title("theta_3")
    plt.plot(ang_3 )
    plt.show()
    
    plt.title("xf")
    plt.plot(x_f )
    plt.show()
    
    plt.title("zf")
    plt.plot(z_f)
    plt.show()