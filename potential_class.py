from boundary_class import boundaries
import numpy as np
import constants as const

class potential:
    @staticmethod
    def convergence(potential_old: float, potential_new: float) -> float:
        """
        Calculate the maximum change in the potential.
        """
        difference = np.max(np.abs(potential_new - potential_old))
        return difference

    @staticmethod
    def jacobi(M: list) -> list:
        """
        Generate an array that contains the potential inside a box of size N,
        using an ansatz of 0 potential.
        """
        P = np.copy(M).reshape((const.N + 2, const.N + 2))

        difference = 1

        while difference > const.tolerance:

            old = np.copy(P)

            P[1:-1, 1:-1] = 0.25 * (
                old[1:-1, 2:] +
                old[1:-1, :-2] +
                old[2:, 1:-1] +
                old[:-2, 1:-1]
            )

            difference = potential.convergence(old, P)

        print(P)
        return P