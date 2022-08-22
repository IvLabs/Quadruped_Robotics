import math as m

class in_kin():
    def __init__(self, link_lengths_ = [0.055,0.07,0.043]):
        self.l1, self.l2, self.l3 = link_lengths_

    def ik(self,p,r,key):
        x, z = p,r
        r = m.sqrt((x)**2  + (z)**2)
        theta_2 = m.acos((self.l2**2 + r**2 - self.l3**2)/(2*self.l2*r))+m.atan(x/z)
        theta_3 = -(m.pi - m.acos((self.l3**2 +  self.l2**2 - r**2)/(2*self.l3* self.l2)))
        if(key==0):
            theta_2 = -m.acos((self.l2**2 + r**2 - self.l3**2)/(2*self.l2*r))+m.atan(x/z)
            theta_3 = (m.pi - m.acos((self.l3**2 +  self.l2**2 - r**2)/(2*self.l3* self.l2)))
        return theta_2,theta_3



        


if __name__ == "__main__":
    ik = in_kin()
    print(ik.ik(0,0.14))
    
    
