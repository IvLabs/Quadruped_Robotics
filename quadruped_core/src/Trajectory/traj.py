#! usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../..')
# print(os.path.dirname(os.path.abspath(__file__)) + '/../../..')
from math import *
from matplotlib import pyplot as plt
from quadruped_core.src.Kinematics.ik import in_kin as kinematics


class trajectory_generator():

    def __init__(self, vx, vy, vz, leg_height, f_hard, n, ang_shift,*args):
        self.vx = vx
        self.vz = vz
        self.vy = vy
        self.leg_height = leg_height
        self.f_hard = f_hard
        self.f_gate = 6
        self.n = n
        self.x0, self.y0 = 0, 0
        self.x1 = self.x0 + self.vx/(2*self.f_gate)
        self.x_shift = self.x1/2

        self.cord = [self.x0, 0]
        self.flag = 1
        self.ang_shift = ang_shift
        if vx != 0 :
            self.ang1_shift = ang_shift + atan(abs(vy)/abs(vx))
        else:
            self.ang1_shift = ang_shift + pi/2
        self.vx = sqrt(vx**2 + vy**2)
        self.leg_kin = kinematics()

        n_max = int(self.f_hard/(2*self.f_gate))
        if n_max <= self.n:
            r = int(self.n/n_max)
            self.n = self.n-r*n_max
            if(r%2 != 0):
                self.flag = self.flag * -1
                self.cord[0]=self.vx/(2*self.f_gate)
                self.update_vx_vy()
                self.swap()


    def get_next(self):
   
        time_left = ((1/(2*self.f_gate)) - (self.n/self.f_hard))
        if time_left > 0:
            self.cord[0] = self.cord[0] + \
                ((self.x1 - self.cord[0])/time_left)/self.f_hard
            self.cord[1] = 0.5*(self.flag + 1) * (self.vz/self.f_gate) * \
                sin((pi*self.n*2*self.f_gate)/(self.f_hard))
            self.cord[1] = self.leg_height - self.cord[1]

        if(abs(time_left) <= (1/self.f_hard)):
            self.flag = self.flag * -1
            if(self.flag == -1):
                self.update_vx_vy()
            self.swap()
            self.n = 0
        else:
            self.n += 1
        return self.cord[0]-self.x_shift, self.cord[1]
        # return self.cord

    def swap(self):
        self.x1, self.x0 = self.x0,  self.x1

    def update_vx_vy(self):
        self.x1 = self.x0 + self.vx/(2*self.f_gate)

    def change_vx_vy(self,vx,vy):
        if vx != 0 :
            self.ang1_shift = self.ang_shift + atan(abs(vy)/abs(vx))
        else:
            self.ang1_shift = self.ang_shift + pi/2
        self.vx = sqrt(vx**2 + vy**2)

    def anglist(self,key):
        x, z = self.get_next()
        q, r = self.leg_kin.ik(x,z,key)

        return self.ang1_shift, q,r

if __name__== "__main__":
    leg1 = trajectory_generator(0.4, 0, 0.1, 0.11, 50, 4, 0)

    x_ , z_ = [], []
    for i in range(100):
        x, z = leg1.get_next()
        x_.append(x)
        z_.append(z)
    plt.plot(x_,z_)
    plt.show()

    q_ , r_ = [], []
    for i in range(100):
        ang1, q, r = leg1.anglist(1)
        q_.append(q)
        r_.append(r)
    plt.plot(q_)
    plt.show()
    plt.plot(r_)
    plt.show()

