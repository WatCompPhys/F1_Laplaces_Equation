from particle_class import particle
from potential_class import potential
from video import video
import numpy as np 
import constants
import time

#TEST 1: LAPLACIAN-FREE OF COMPUTED POTENTIAL FIELD 

def laplacian_free_test(L, num_cells, atol = 1e-3): #keep atol = 1e-3 or less
    start_time = time.time()
    print(f"Laplacian-Free Test initialted at t = {start_time}")
    X, Y = np.linspace(0, L, num_cells), np.linspace(0, L, num_cells)
    dL = X[1] - X[0]
    XX, YY  = np.meshgrid(X, Y)
    phi = np.zeros_like(XX)

    #you can change these boundaries to wtv but make sure to test quite a few and make sure that it works for all
    # Bottom = -np.sin(2 * np.pi/L * X) + 1/10
    # Top = np.sin(2 * np.pi/L * X)+ 1/10
    # Left = -np.sin(2 * np.pi/L * Y)+ 1/10
    # Right = np.sin(2 * np.pi/L * Y)+ 1/10
    
    # Constant
    # Bottom = np.ones_like(X) * 1
    # Top = np.ones_like(X) * 1
    # Left = np.ones_like(Y) * 1
    # Right = np.ones_like(Y) * 1

    # Quadratic
    # Bottom = X**2
    # Top = (L - X)**2
    # Left = Y**2
    # Right = (L - Y)**2

    # Exponential
    # Bottom = np.exp(X / L)
    # Top = np.exp((L - X) / L)
    # Left = np.exp(Y / L)
    # Right = np.exp((L - Y) / L)

    # Sine + Cosine
    # Bottom = np.sin(2 * np.pi * X / L) + np.cos(4 * np.pi * X / L)
    # Top = np.sin(2 * np.pi * X / L) - np.cos(4 * np.pi * X / L)

    # Left = np.sin(2 * np.pi * Y / L) + np.cos(4 * np.pi * Y / L)
    # Right = np.sin(2 * np.pi * Y / L) - np.cos(4 * np.pi * Y / L)

    # Gaussian
    # Bottom = np.exp(-((X - L/2) / (L/5))**2)
    # Top = np.exp(-((X - L/2) / (L/5))**2)

    # Left = np.exp(-((Y - L/2) / (L/5))**2)
    # Right = np.exp(-((Y - L/2) / (L/5))**2)

    # Random
    # Bottom = np.random.uniform(-1, 1, num_cells)
    # Top = np.random.uniform(-1, 1, num_cells)
    # Left = np.random.uniform(-1, 1, num_cells)
    # Right = np.random.uniform(-1, 1, num_cells)

    # Almost Discountinous
    Bottom = np.where(X < L/2, 1, -1)
    Top = np.where(X < L/2, -1, 1)

    Left = np.where(Y < L/2, 1, -1)
    Right = np.where(Y < L/2, -1, 1)

    phi[:, 0] = Left
    phi[:, -1] = Right
    phi[0, :] = Top 
    phi[-1, :] = Bottom

    phi = potential.jacobi(phi.flatten())
    laplace_phi = 1/(dL**2) * (phi[2:, 1:-1] + phi[:-2, 1:-1] + phi[1:-1, 2:] + phi[1:-1, :-2] - 4 * phi[1:-1, 1:-1]) #judge the interior points

    finish_time = time.time()
    print(f"Laplacian-Free Test concluded at t = {finish_time}")

    print(30 * "\n"+f"*************** LAPLACIAN-FREE TEST RESULTS ***************")
    print(f"\nPASS? = {np.allclose(laplace_phi, np.zeros_like(laplace_phi), atol = atol)} \nTEST DESCRIPTION: Evaluates whether phi is Laplacian-free to within a specfied numerical tolerance  (atol = {atol})\n")
    print(f"ANALYSIS: \nMax deviation from zero for laplacian(phi) = {np.max(np.abs(laplace_phi - np.zeros_like(laplace_phi)))}\nMean deviation from zero for laplacian(phi) = {np.mean(np.abs(laplace_phi - np.zeros_like(laplace_phi)))}")
    print(f"PERFORMANCE: Runtime = {(finish_time - start_time):.1f} sec ()")


    return None

# laplacian_free_test(10, constants.N + 2)


#DEMONSTRATION 1: Static field, moving particle, plot

def test_loop_1(L, num_cells, tmax, dt):
    X, Y = np.linspace(0, L, num_cells), np.linspace(0, L, num_cells)
    dL = X[1] - X[0]
    XX, YY  = np.meshgrid(X, Y)
    phi = np.zeros_like(XX)

    B = -np.sin(2 * np.pi/L * X) + 1/10
    T = np.sin(2 * np.pi/L * X)+ 1/10
    Left = -np.sin(2 * np.pi/L * Y)+ 1/10
    R = np.sin(2 * np.pi/L * Y)+ 1/10

    phi[:, 0] = Left
    phi[:, -1] = R 
    phi[0, :] = T 
    phi[-1, :] = B

    phi = potential.jacobi(phi.flatten())

    test_particle = particle(1.0, 1.0, [2.8, 0.1]) # [X[len(X)//2],Y[len(Y)//3]]

    laplace_phi = 1/(dL**2) * (phi[2:, 1:-1] + phi[:-2, 1:-1] + phi[1:-1, 2:] + phi[1:-1, :-2] - 4 * phi[1:-1, 1:-1]) #judge the interior points
    t = 0 
    while t < tmax and not test_particle.exit_box:
        print(30 * "\n" + f"t = {t} out of {tmax} (dt = {dt})")
        test_particle.update_pos(phi, dL, dt, X, Y)
        t += dt 

    print(f"TEST: phi is laplacian-free | PASS = {np.allclose(laplace_phi, np.zeros_like(laplace_phi), rtol = 1e-3, atol = 1e-6)}")
    test_particle.plot_path(phi, X, Y)


#test_loop_1(10, constants.N + 2, 128, 1/10)


#DEMONSTRATION 2: Static field, moving particle, video

def test_loop_2(L, num_cells, tmax, dt):
    X, Y = np.linspace(0, L, num_cells), np.linspace(0, L, num_cells)
    dL = X[1] - X[0]
    XX, YY  = np.meshgrid(X, Y)
    phi = np.zeros_like(XX)

    # Bottom = np.exp(X / L)
    # Top = np.exp((L - X) / L)
    # Left = np.exp(Y / L)
    # Right = np.exp((L - Y) / L)

    Bottom = np.sin(2 * np.pi * X / L) + np.cos(4 * np.pi * X / L)
    Top = np.sin(2 * np.pi * X / L) - np.cos(4 * np.pi * X / L)

    Left = np.sin(2 * np.pi * Y / L) + np.cos(4 * np.pi * Y / L)
    Right = np.sin(2 * np.pi * Y / L) - np.cos(4 * np.pi * Y / L)

    phi[:, 0] = Left
    phi[:, -1] = Right
    phi[0, :] = Top
    phi[-1, :] = Bottom

    phi = potential.jacobi(phi.flatten())

    test_particle = particle(1.0, 1.0, [2.4, 0.1]) # [X[len(X)//2],Y[len(Y)//3]]

    laplace_phi = 1/(dL**2) * (phi[2:, 1:-1] + phi[:-2, 1:-1] + phi[1:-1, 2:] + phi[1:-1, :-2] - 4 * phi[1:-1, 1:-1]) #judge the interior points
    t = 0 
    while t < tmax and not test_particle.exit_box:
        print(30 * "\n" + f"t = {t} out of {tmax} (dt = {dt})")
        test_particle.update_pos(phi, dL, dt, X, Y)
        t += dt

    video(test_particle, phi, X, Y)

test_loop_2(10, constants.N + 2, 128, 1/10)