import numpy as np 
import matplotlib.pyplot as plt

class particle:
    def __init__(self, mass = 1, charge = 1, init_pos = [0.0, 0.0]):
        self.mass = mass 
        self.charge = charge 
        self.position = np.array(init_pos) #[x,y]
        self.posn_hist_x = []
        self.posn_hist_y = []
        self.velocity = np.array([0.0, 0.0]) #[vx, vy]
        self.exit_box = False

    def get_accels(self, phi,  dL, dt,  X, Y):
        """
        phi is the potential field, dL is the grid spacing and dt is the timestep. 
        X and Y are 1D arrays of the axes 

        Going along a row varies x and column varies y for phi and electric fields
        This means for any field, the indexing is [y_index, x_index]
        """
        electric_field_x, electric_field_y = np.zeros_like(phi),  np.zeros_like(phi)
        electric_field_x[1:-1, 1:-1] = -(phi[1:-1, 2:] - phi[1:-1, :-2])/(dL*2)
        electric_field_y[1:-1, 1:-1] = -(phi[2:, 1:-1] - phi[:-2, 1:-1])/(dL*2)

        accel_field_x = electric_field_x * self.charge/self.mass
        accel_field_y = electric_field_y * self.charge/self.mass

        x_index = np.abs(self.position[0] - X).argmin()
        y_index = np.abs(self.position[1] - Y).argmin()

        accel = np.array([accel_field_x[ y_index,x_index], accel_field_y[y_index, x_index]])

        return accel

    def update_pos(self, phi, dL, dt, X, Y):
        if self.position[0] >= np.max(X) or self.position[1] >= np.max(Y) or self.position[0] <= np.min(X) or self.position[1] <= np.min(Y):
            self.velocity = np.array([0, 0])
            print("Particle has reached the end of the plates.")
            self.exit_box = True
            return None 

        cur_accel = self.get_accels(phi, dL, dt, X, Y)
        self.position += self.velocity * dt + 1/2 * cur_accel * dt**2
        new_accel = self.get_accels(phi, dL, dt, X, Y)
        self.velocity += 1/2 * (cur_accel + new_accel) * dt

        self.posn_hist_x.append(self.position[0])
        self.posn_hist_y.append(self.position[1])

    def plot_path(self, phi = None, X = None, Y = None):
        if phi is not None and X is not None and Y is not None:
            col = plt.imshow(phi, extent = [np.min(X), np.max(X),np.min(Y), np.max(Y) ], origin = "lower", cmap = "magma")
            plt.colorbar(label="Potential")

        plt.plot(self.posn_hist_x, self.posn_hist_y, label = "Particle Path")
        plt.plot(self.posn_hist_x[0], self.posn_hist_y[0], "o", color = "r", label = "Particle Start")
        plt.plot(self.posn_hist_x[-1], self.posn_hist_y[-1], "o", color = "b", label = "Particle End")

        plt.legend()
        plt.show()


            



