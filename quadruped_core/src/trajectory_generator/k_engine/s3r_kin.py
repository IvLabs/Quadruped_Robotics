# -*- coding: utf-8 -*-

import math as m

class kinematics():

    def __init__(self, link_lengths_ = [0.88,0.88,0.84]):
        self.l1, self.l2, self.l3 = link_lengths_
        
        
    # forward kinematics calculations    
    def fk(self, t1, t2, t3):

        l2c2 = self.l2*m.cos(t2)
        l3c23 = self.l3*m.cos(t2+t3)
        l2s2 = self.l2*m.sin(t2) 
        l3s23 = self.l3*m.sin(t2+t3)
        
        x = (self.l1 + l2c2 + l3c23)*m.cos(t1)
        y = (self.l1 + l2c2 + l3c23)*m.sin(t1)
        z= l2s2 + l3s23
        
        return x,y,z
    
    # inverse kinematics calculations
    def ik(self,p,q,r):

        x, y, z = p,q,r

        # Having the link l1 along x-axis would mean y=0
        y = 0
        
        theta_1 = m.atan2(y,x)

        x1 = x/m.cos(theta_1) - self.l1
        z1 = z
        
        r_2 = x1**2 + z1**2
        
        a = r_2 - (self.l2**2 + self.l3**2)
        # n=2*self.l2*self.l3

        c = a/(2*self.l2*self.l3)

        theta_3 = m.acos(c)

        l3c3 = self.l3*m.cos(theta_3)
        l3s3 = self.l3*m.sin(theta_3)
        
        beta = m.atan2(l3s3, self.l2 + l3c3)
        gamma = m.atan2(z1, x1)
        
        theta_2 = gamma - beta

        return theta_1,theta_2,theta_3
