import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from quadruped_core.src.Trajectory.traj import trajectory_generator
pi = np.pi


class quadruped:

    def __init__(self, gate_type: str, vx, vy, vz):

        if gate_type == "trot":
            phase_angs = [0, pi/2, pi/2, 0]
        else:
            phase_angs = [0, pi, pi, 0]

        self.vx, self.vy, self.vz = vx, vy, vz
        self.f_hard = 100
        self.leg_height = 0.1
        self.n_sift = self.get_n_shift(phase_angs)
        self.ang_shift = [0, 0, 0, 0]

        
        
        leg_traj = []
        for i in range(4):
            leg = trajectory_generator(vx=self.vx, vy=self.vy, vz=self.vz, leg_height=self.leg_height,
                                     f_hard=self.f_hard, n=self.n_sift[i], ang_shift=self.ang_shift[i])
            leg_traj.append(leg)
        self.leg_traj = leg_traj

    def get_n_shift(self, phase_angs):
        n_shift = [0, 0, 0, 0]
        for i in range(4):
            n_shift[i] = int(phase_angs[i]/(2*pi*self.f_hard))
        return n_shift

    def get_loop_points(self, vx, vy):
        self.vx, self.vy = vx, vy
        loop_points = []
        for i in range(4):
            self.leg_traj[i].change_vx_vy(vx, vy)
        
        for i in range(self.f_hard):
            points = []
            for j in range(4):
                points.extend(self.leg_traj[j].anglist())
            loop_points.append(points)
        return loop_points  

if __name__=="__main__":
    quad = quadruped("trot", 0.04, 0, 0.04)
    loop_points = quad.get_loop_points(0.04, 0)
    print(np.shape( np.array(loop_points)))
