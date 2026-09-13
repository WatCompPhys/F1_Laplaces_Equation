import numpy as np
import constants as const

class boundaries:
    def __init__(self, distribution):
        self.grid = np.zeros((const.N+2)*(const.N+2))

        x = np.arange(const.N + 2)

        if distribution == "gaussian":
            self.values = np.exp(-((x - const.N/2) / (const.N/5))**2)

        elif distribution == "sinusoidal":
            self.values = np.sin(np.pi * x / (const.N + 1))

        elif distribution == "parabolic":
            self.values = 1 - ((x - const.N/2) / (const.N/2))**2

        elif distribution == "linear":
            self.values = x / (const.N + 1)

        elif distribution == "zeros":
            self.values = np.zeros(const.N + 2)
        
        self.apply_boundary()
        self.first_time = True

    def apply_boundary(self):
        # top and bottom
        for i in range(const.N + 2):
            self.grid[i] = self.values[i]
            self.grid[(const.N + 1) * (const.N + 2) + i] = self.values[i]

        # left and right
        for i in range(const.N + 2):
            self.grid[i * (const.N + 2)] = self.values[i]
            self.grid[i * (const.N + 2) + (const.N + 1)] = self.values[i]

    def get_values(self, new_values=None):
        if self.first_time:
            self.first_time = False
            return self.grid
        else:
            self.values = new_values
            self.apply_boundary()
            return self.grid