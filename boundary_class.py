import numpy as np
import constants as const

class boundaries:
    """
    Applies boundary conditions to a grid based on 
    distribution selection for first timestep.
    And input values on subsequent timestep
    """
    def __init__(self, distribution: str) -> None:
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

        self.first_time = True
        self.apply_boundary()

    def apply_boundary(self) -> None:
        """
        Applies boundary conditions to grid based on values provided.
        """
        if self.first_time:
            # bottom and top
            for i in range(const.N + 2):
                self.grid[i] = self.values[i]
                self.grid[(const.N + 1) * (const.N + 2) + i] = self.values[i]

            # left and right
            for i in range(const.N + 2):
                self.grid[i * (const.N + 2)] = self.values[i]
                self.grid[i * (const.N + 2) + (const.N + 1)] = self.values[i]

        else:
            # top
            for i in range(const.N + 2):
                self.grid[(const.N + 1) * (const.N + 2) + i] = self.new_values[2]
            # bottom
            for i in range(const.N + 2):
                self.grid[i] = self.new_values[3]

            # right
            for i in range(const.N + 2):
                self.grid[i * (const.N + 2) + (const.N + 1)] = self.new_values[0]
            # left
            for i in range(const.N + 2):
                self.grid[i * (const.N + 2)] = self.new_values[1]

    def get_values(self, new_values=None) -> list:
        """
        Determines which timestep is currently running and returns grid
        """
        if self.first_time:
            self.first_time = False
            return self.grid
        else:
            self.new_values = new_values
            self.apply_boundary()
            return self.grid