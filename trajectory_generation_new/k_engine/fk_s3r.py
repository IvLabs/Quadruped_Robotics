# -*- coding: utf-8 -*-

import math as m

class f_kin():
    
    def __init__(self, link_lengths_ = [0.055,0.07,0.075]):
        self.l1, self.l2, self.l3 = link_lengths_
        
    def fk(self, t1, t2, t3):
        
        l2c2 = self.l2*m.cos(t2)
        l3c23 = self.l3*m.cos(t2+t3)
        l2s2 = self.l2*m.sin(t2) 
        l3s23 = self.l3*m.sin(t2+t3)
        
        x = (self.l1 + l2c2 + l3c23)*m.cos(t1)
        y = (self.l1 + l2c2 + l3c23)*m.sin(t1)
        z= l2s2 + l3s23
        
        return x,y,z