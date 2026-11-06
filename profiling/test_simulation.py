import time
import numpy as np
import src.constants as const
import src.Potential as Potential
from src.particle_class import particle
from src.video import video
from src.step_potential_switching import step_switching

# Simulation parameters
const.N = 50
const.tolerance = 1e-4

L = 10.0
x = 5.0
y = 5.0
x_0 = 7.0
y_0 = 5.0

particle_mass = 1.0
particle_charge = 1.0
num_frames = 300

distribution = "gaussian"

start_time = time.perf_counter()

# Boundary Conditions
grid = np.zeros((const.N+2)*(const.N+2))
grid, first_time = Potential.get_values(
    distribution, grid, first_time=True
)

# Solve Laplace equation
phi = Potential.jacobi(grid)
phi_history = [phi.copy()]

# Coordinate system
X = np.linspace(0, L, const.N + 2)
Y = np.linspace(0, L, const.N + 2)

dL = X[1] - X[0]

# Create particle
p = particle(
    mass=particle_mass,
    charge=particle_charge,
    init_pos=[x, y]
)

# Particle simulation
dt = 0.01
max_steps = 10000
steps = 0

disp_x = x - x_0
disp_y = y - y_0

while (not p.exit_box
       and (abs(disp_x) > .25 or abs(disp_y) > .25)
       and steps < max_steps):

    new_values = step_switching(x, y, x_0, y_0)
    grid, first_time = Potential.get_values(
        distribution, grid, first_time, new_values
    )

    phi = Potential.jacobi(grid)
    phi_history.append(phi.copy())

    p.update_pos(phi, dL, dt, X, Y)

    x = p.position[0]
    y = p.position[1]

    disp_x = x - x_0
    disp_y = y - y_0

    steps += 1

print("Number of particle positions:", len(p.posn_hist_x))

# Generate video
video(p, phi_history, X, Y, num_frames)

elapsed_time = time.perf_counter() - start_time
print(f"Executed in: {elapsed_time:.4f} seconds")