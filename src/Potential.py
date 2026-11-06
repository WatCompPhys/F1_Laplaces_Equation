import numpy as np
import src.constants as const

def boundaries(distribution):
    """
    Provides boundary values based on 
    distribution selection for first timestep.
    """
    x = np.arange(const.N + 2)

    if distribution == "gaussian":
        values = np.exp(-((x - const.N/2) / (const.N/5))**2)

    elif distribution == "sinusoidal":
        values = np.sin(np.pi * x / (const.N + 1))

    elif distribution == "parabolic":
        values = 1 - ((x - const.N/2) / (const.N/2))**2

    elif distribution == "linear":
        values = x / (const.N + 1)

    elif distribution == "zeros":
        values = np.zeros(const.N + 2)
    
    return values

def apply_boundary(grid, values, first_time):
    """
    Applies boundary conditions to grid based on values provided.
    """
    phi = grid.reshape((const.N + 2, const.N + 2))

    if first_time:
        phi[0, :] = values
        phi[-1, :] = values
        phi[:, 0] = values
        phi[:, -1] = values

    else:
        # top, bottom, left, right
        phi[0, :] = values[3]
        phi[-1, :] = values[2]
        phi[:, 0] = values[1]
        phi[:, -1] = values[0]

    return grid

def get_values(distribution, grid, first_time, new_values=None) -> list:
    """
    Determines which timestep is currently running and returns grid
    """
    if first_time:
        new_grid = apply_boundary(grid, boundaries(distribution), first_time)
        first_time = False
    else:
        values = new_values
        new_grid = apply_boundary(grid, values, first_time)
    
    return new_grid, first_time


def convergence(potential_old: float, potential_new: float) -> float:
    """
    Calculate the maximum change in the potential.
    """
    difference = np.max(np.abs(potential_new - potential_old))
    return difference

def jacobi(grid: list) -> list:
    phi = np.copy(grid).reshape((const.N + 2, const.N + 2))
    new_phi = np.empty_like(phi)

    difference = 1

    while difference > const.tolerance:

        new_phi[:] = phi

        new_phi[1:-1, 1:-1] = 0.25 * (
            phi[1:-1, 2:] +
            phi[1:-1, :-2] +
            phi[2:, 1:-1] +
            phi[:-2, 1:-1]
        )

        difference = convergence(phi, new_phi)

        phi, new_phi = new_phi, phi

    print(phi)
    return phi