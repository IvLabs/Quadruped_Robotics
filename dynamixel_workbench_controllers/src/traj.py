#! usr/bin/env python3
from math import *
from matplotlib import pyplot as plt
import sys
from ik import in_kin as kinematics
from k_engine.fk_s3r import f_kin as fk

class trajectory_generator():

    def __init__(self , vx , vy , vz , leg_height , f_hard,n,*args):
        self.vx = vx
        self.vz = vz
        self.vy = vy
        self.leg_height = leg_height
        self.f_hard = f_hard
        self.f_gate = 6
        self.n = n
        self.x0 , self.y0 = 0 , 0
        self.x1 = self.x0 +  self.vx/(2*self.f_gate) 
       
        self.y1 = self.y0 +  self.vy/(2*self.f_gate)
        self.x_shift = self.x1/2
        
        self.y_shift = self.y1/2
   
        self.cord = [ self.x0 ,self.y0, 0]
        self.flag = 1
        self.ang1_shift=args[0]

    def get_next( self):
        n_max=int(self.f_hard/(2*self.f_gate))
        if n_max<=self.n:
            r=int(self.n/n_max)
            self.n=self.n-r*n_max
            self.flag=-1*self.flag
            if( self.flag == -1 ):
                self.update_vx_vy()
            self.swap();

        time_left = ( (1/(2*self.f_gate))  - ( self.n/self.f_hard)   ) 
        if time_left > 0 :
            self.cord[0] = self.cord[0] +  ( (self.x1 - self.cord[0])/time_left)/self.f_hard 
            self.cord[1] = self.cord[1] +  ( (self.y1 - self.cord[1])/time_left    )/self.f_hard 
            self.cord[2] =   0.5*(self.flag + 1)* (self.vz/self.f_gate) * sin( (pi*self.n*2*self.f_gate)/(self.f_hard) )
            self.cord[2] = self.leg_height - self.cord[2]
            

        if(abs(time_left) <= (1/self.f_hard) ):
            self.flag = self.flag * -1 
            if( self.flag == -1 ):
                self.update_vx_vy()
            self.swap();
            self.n = 0 
        else  :
            self.n += 1
        

        return self.cord[0]-self.x_shift , self.cord[1]-self.y_shift , self.cord[2] ;
        # return self.cord

    def swap(self):
        self.x1 , self.y1 , self.x0 , self.y0 = self.x0 , self.y0 , self.x1 , self.y1

    def update_vx_vy(self):

        self.x1 = self.x0 +  self.vx/(2*self.f_gate) 
        self.y1 = self.y0 +  self.vy/(2*self.f_gate)


    def anglist(self):

        

        x_cor ,y_cor , z_cor = [] , [] , []
        x_f ,y_f , z_f = [] , [] , []

        leg_kin = kinematics()
        leg_fk=fk()

        ang1 , ang2 , ang3 = [] , [] , []

        for _ in range(100):
            x, y, z = self.get_next()
           
    
            x_cor.append(x)
            y_cor.append(y)
            z_cor.append(z)
            print(x_cor)

            p,q,r = leg_kin.ik(x,y,z)
            x_f,y_f,z_f=leg_fk.fk(p,q,r)
            x_f.append(x)
            y_f.append(y)
            z_f.append(z)

            ang1.append(self.ang1_shift)
            ang2.append(q)
            ang3.append(-1*r)
     

        import matplotlib.pyplot as p    
        plt.title("x vs z")
        plt.plot(x_cor , z_cor)
        plt.show() 
        plt.title("xf vs zf")
        plt.plot(x_cor , z_cor)
        plt.show()

        
        plt.title("x cordinate")
        plt.plot(x_cor )
        plt.show()
        fig, axs = plt.subplots(3, 2)
        axs[0, 0].plot(ang1)
        axs[0, 0].set_title('angle 1')
        axs[0, 1].plot(ang2)
        axs[0, 1].set_title('angle 2')
        axs[1, 0].plot(ang3)
        axs[1, 0].set_title('angle 3')
        axs[1, 1].plot(x_cor,z_cor)
        axs[1, 1].set_title('x,z')
        axs[2, 0].plot(z_cor)
        axs[2, 0].set_title('z')
        axs[2, 1].plot(x_cor)
        axs[2, 1].set_title('x')
        plt.show()
        return ang1,ang2,ang3

leg1=trajectory_generator(0.7,0,0.1,0.13,50,4,0)

leg1.anglist()
      

    # print( max(ang3),max(ang2))