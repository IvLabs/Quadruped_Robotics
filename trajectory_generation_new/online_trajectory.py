#! usr/bin/env python3
from math import *
from matplotlib import pyplot as plt
import sys
from mpl_toolkits import mplot3d




from k_engine.s3r_kin import kinematics
 
class trajectory_generator():

    # def __init__(self , vx , vy , vz , leg_height , f_hard):
    #     self.vx = vx
    #     self.vz = vz
    #     self.vy = vy
    #     self.leg_height = leg_height
    #     self.f_hard = f_hard
    #     self.f_gate = 2
    #     self.n =   0
    #     self.x0 , self.y0 = 0,0
    #     self.x1 = self.x0 +  self.vx*2/self.f_gate 
    #     self.y1 = self.y0 +  self.vy*2/self.f_gate
    #     self.cord = [ self.x0 ,self.y0, 0]
    #     self.flag = 1

    # def get_next( self):

    #     time_left = ( (2/self.f_gate)  - ( self.n/self.f_hard) ) 
    #     if time_left > 0 :
    #         self.cord[0] = self.cord[0] +  ( (self.x1 - self.cord[0])/time_left    )/self.f_hard 
    #         self.cord[1] = self.cord[1] +  ( (self.y1 - self.cord[1])/time_left    )/self.f_hard 
    #         self.cord[2] =   0.5*(self.flag + 1)* (self.vz/self.f_gate) * sin( (pi*self.n*self.f_gate)/(2*self.f_hard) )
    #         self.cord[2] = self.leg_height - self.cord[2]
    #         # print( self.cord)

    #     if(abs(time_left) <= (1/self.f_hard) ):
    #         self.flag = self.flag * -1 
    #         if( self.flag == -1 ):
    #             self.update_vx_vy()
    #         self.swap();
    #         self.n = 0 
    #     else  :
    #         self.n += 1

    def __init__(self , vx , vy , vz , leg_height , f_hard, n):
        self.vx = vx
        self.vz = vz
        self.vy = vy
        self.leg_height = leg_height
        self.f_hard = f_hard
        self.f_gate = 6
        self.n = n
        self.x0 , self.y0 = 0,0
        self.x1 = self.x0 +  self.vx/(2*self.f_gate)
        self.y1 = self.y0 +  self.vy/(2*self.f_gate)
        self.cord = [ self.x0 ,self.y0, 0]
        self.flag = 1

    def get_next( self):
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
        if time_left > 0 :
            self.cord[0] = (self.cord[0] +  ( (self.x1 - self.cord[0])/time_left    )/self.f_hard )
            self.cord[1] = self.cord[1] +  ( (self.y1 - self.cord[1])/time_left    )/self.f_hard 
            self.cord[2] =   0.5*(self.flag + 1)* (self.vz/self.f_gate) * sin( (pi*self.n*2*self.f_gate)/(self.f_hard) )
            self.cord[2] = self.leg_height - self.cord[2]

            # print(self.cord[0],self.n,time_left)

        if(abs(time_left) <= (1/self.f_hard) ):
            self.flag = self.flag * -1 
            if( self.flag == -1 ):
                #print("yes")
                self.update_vx_vy()
            self.swap();
            self.n = 0
        else:
            self.n += 1

        return self.cord ;

    def swap(self):
        self.x1 , self.y1 , self.x0 , self.y0 = self.x0 , self.y0 , self.x1 , self.y1

    def update_vx_vy(self):

        self.x1 = self.x0 +  self.vx/(2*self.f_gate) 
        self.y1 = self.y0 +  self.vy/(2*self.f_gate)


if __name__ == "__main__":

    tg = trajectory_generator( 0.1, 0, 0.1, 0.175,50,0)

    x_cor ,y_cor , z_cor = [] , [] , []
    ang_1, ang_2, ang_3 = [], [], []
    x_f ,y_f , z_f = [] , [] , []   
    t=[] 
    #l1ang_1,l1ang_2,l1ang_3,l2ang_1,l2ang_2,l2ang_3,l3ang_1,l3ang_2,l3ang_3, l4ang_1,l4ang_2,l4ang_3= [],[],[],[],[],[],[],[],[],[],[],[]
    leg = kinematics()
    
    
    for i in range(100):
        x, y, z = tg.get_next()
        x_cor.append(x)
        y_cor.append(y)
        z_cor.append(z)
        x=x-(0.1/(4*6))
        print(x)
        t1 ,t2, t3 = leg.ik(z,y,x)
        ang_1.append(t1)
        ang_2.append(t2)
        ang_3.append(t3)
        
        p, q, r = leg.fk(t1,t2, t3)
        
        x_f.append(p)
        y_f.append(q)
        z_f.append(r)
        
    # for i in range(50):
    #         t1 ,t2, t3 = leg.ik(x_cor[i], y_cor[i], z_cor[i])
    #         l1ang_1.append(t1)
    #         l1ang_2.append(t2)
    #         l1ang_3.append(t3)
            
    #         t1 ,t2, t3 = leg.ik(x_cor[i+25], y_cor[i+25], z_cor[i+25])
    #         l2ang_1.append(t1)
    #         l2ang_2.append(t2)
    #         l2ang_3.append(t3)

    #         t1 ,t2, t3 = leg.ik(x_cor[i+13], y_cor[i+13], z_cor[i+13])
    #         l3ang_1.append(t1)
    #         l3ang_2.append(t2)
    #         l3ang_3.append(t3)

    #         t1 ,t2, t3 = leg.ik(x_cor[i+37], y_cor[i+37], z_cor[i+37])
    #         l4ang_1.append(t1)
    #         l4ang_2.append(t2)
    #         l4ang_3.append(t3)
        # t1 ,t2, t3 = leg.ik(x,y,z)
        # ang_1.append(t1)
        # ang_2.append(t2)
        # ang_3.append(t3)
        
       
    # for i in range(50):
    #     p, q, r = leg.fk(l4ang_1[i], l4ang_2[i], l4ang_3[i] )
        
    #     x_f.append(p)
    #     y_f.append(q)
    #     z_f.append(r)
    #     t1 ,t2, t3 = leg.ik(x,y,z)
    #     l1ang_1.append(t1)
    #     l1ang_2.append(t2)
    #     l1ang_3.append(t3)
    # for i in range(100):
    #     t1 ,t2, t3 = leg.ik(x,y,z)
    #     l1ang_1.append(t1)
    #     l1ang_2.append(t2)
    #     l1ang_3.append(t3)

    # for i in range(25,125):
    #     t1 ,t2, t3 = leg.ik(x,y,z)
    #     l2ang_1.append(t1)
    #     l2ang_2.append(t2)
    #     l2ang_3.append(t3)

    # for i in range(50,150):
    #     t1 ,t2, t3 = leg.ik(x,y,z)
    #     l3ang_1.append(t1)
    #     l3ang_2.append(t2)
    #     l3ang_3.append(t3)

    # for i in range(75,175):
    #     t1 ,t2, t3 = leg.ik(x,y,z)
    #     l4ang_1.append(t1)
    #     l4ang_2.append(t2)
    #     l4ang_3.append(t3)



    # ax = plt.axes(projection='3d')
    # ax.plot3D(x_cor, y_cor, z_cor)  
    # plt.show()

    # ax = plt.axes(projection='3d')
    # ax.plot3D(x_f, y_f, z_f)  
    # plt.show()
    # print(ang_2)
    # import matplotlib.pyplot as plt

    # plt.title("traj x vs traj z l1")
    # plt.plot(x_cor[:100] )
    # plt.show()

    # plt.title("traj x vs traj z l2")
    # plt.plot(x_cor[25:125] )
    # plt.show()

    # plt.title("traj x vs traj z l3")
    # plt.plot(x_cor[50:150] )
    # plt.show()

    # plt.title("traj x vs traj z  l4")
    # plt.plot(x_cor[75:175] )
    # plt.show()

    # plt.title("xcor ")
    # plt.plot(x_cor)
    # plt.show()
    # # plt.title("y vs z")

    # # # plt.plot(y_cor , z_cor)
    # # # plt.show()

    # plt.title("traj x")
    # plt.plot(z_cor )
    # plt.show()
    
    # plt.title("traj z")
    # plt.plot(z_cor)
    # plt.show()

    
    # plt.title("theta_1")
    # plt.plot(ang_1 )
    # plt.show()

    # plt.title("theta_2")
    # plt.plot(ang_2 )
    # plt.show()

    # plt.title("theta_3")
    # plt.plot(ang_3 )
    # plt.show()
    
    plt.title("xf")
    plt.plot(z_f,x_f)
    plt.show()
    
    # plt.title("xvsz")
    # plt.plot(z_cor)
    # plt.show()
    
