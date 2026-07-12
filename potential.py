import numpy as np
import constants as const

def convergence(potential_old: float, potential_new: float) -> float:
    """
    Calculate the maximum change in the potential.
    """
    difference = np.max(np.abs(potential_new - potential_old))
    return difference

def jacobi() -> list:
    """
    Generate an array that contains the potential inside a box of size N,
    using an ansatz of 0 potential.
    """

    # Create a copy of the initial potential distribution (ansatz)
    P = np.copy(const.ansatz)
    
    # Iterate until the potential field converges within the desired tolerance
    difference = 1
    while difference > const.tolerance:

        # Store the previous iteration of the potential field for Jacobi updates
        old = np.copy(P)

        # x-coordinate loop
        m = 1
        while m < const.N:

            # y-coordinate loop
            n = 1
            while n < const.N:

                # Convert 2D grid coordinates (m,n) into a 1D array index
                index = m*(const.N+1)+n

                # Apply finite difference approximation of Laplace's equation
                P[index] = 0.25*(
                    old[index+1]+
                    old[index-1]+
                    old[index+(const.N+1)]+
                    old[index-(const.N+1)]
                )

                n += 1

            m += 1
        difference = convergence(old, P)
    
    print(P)
    return P

jacobi()