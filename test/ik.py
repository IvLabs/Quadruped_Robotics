import math as m

class in_kin():
    def __init__(self, link_lengths_ = [0.055,0.07,0.075]):
        self.l1, self.l2, self.l3 = link_lengths_
        self.shift = 0.0

    def ik(self,x,y,z): # ik for 3d, not in use
        if x != 0:
            theta_1 = m.atan(y/x)
        else:
            theta_1 = m.pi/2 * abs(y)/y

        x1 = self.l1*m.cos(theta_1) 
        y1 = self.l1*m.sin(theta_1)
        z1 = 0 + self.shift
        r = m.sqrt((x-x1)**2 + (y-y1)**2 + (z-z1)**2)
      
        theta_2 = m.acos((self.l2**2 + r**2 - self.l3**2)/(2*self.l2*r)) + m.atan( ( (x*m.cos(theta_1)+y*m.sin(theta_1))   )/(z-z1) )

        theta_3 = m.pi - m.acos((self.l3**2 +  self.l2**2 - r**2)/(2*self.l3* self.l2))

        return theta_1,theta_2,theta_3


if __name__ == "__main__":
    ik = in_kin()
    print(ik.ik(0.04,0,0.1)) # (0.0, 0.9979344432969673, 0.7082155856829662)
    print(ik.ik(-0.04,0,0.1)) # (0.0, 0.4817316612425373, 0.7082155856829662)

    print(ik.ik(0,0.04,0.1)) # (1.57, 0.9979344432969673, 0.7082155856829662)
    print(ik.ik(0,-0.04,0.1)) # (-1.57, 0.4817316612425373, 0.7082155856829662)
    
