# from cmath import acos
import math as m

class in_kin():
    def __init__(self, link_lengths_ = [0.88,0.88,0.84]):
        self.l1, self.l2, self.l3 = link_lengths_
        

    def ik(self,p,q,r):
        x, y, z = p,q,r

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

