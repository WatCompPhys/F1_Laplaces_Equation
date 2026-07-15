import numpy as np

N = 10
tolerance = 0.0001

class boundaries:
    def __init__(self, distribution):
        self.grid = np.zeros((N+2)*(N+2))

        if distribution == "uniform":
            self.values = np.random.uniform(0, N, N+2)

        elif distribution == "normal":
            self.values = np.random.normal(0, N, N+2)

        elif distribution == "zeros":
            self.values = np.zeros(N+2)

        else:
            raise ValueError("Unknown distribution")
        
        self.apply_boundary()
        self.first_time = True

    def apply_boundary(self):
        # top and bottom
        for i in range(N+2):
            self.grid[i] = self.values[i]
            self.grid[N*(N+2)+i] = self.values[i]

        # left and right
        for i in range(N+2):
            self.grid[i*(N+2)] = self.values[i]
            self.grid[i*(N+2)+N] = self.values[i]

    def get_values(self, new_values=None):
        if self.first_time:
            self.first_time = False
            return self.grid
        else:
            self.values = new_values
            return self.grid