import time
import numpy as np
import streamlit as st
import constants as const
import Potential
from particle_class import particle
from video import video
from step_potential_switching import step_switching

st.title("Particle in Box Simulation")

# Simulation parameters

const.N = st.slider(
    "Grid size (N)",
    min_value=10,
    max_value=500,
    value=50,
    step=10
)

const.tolerance = st.number_input(
    "Jacobi tolerance",
    min_value=1e-10,
    max_value=1e-2,
    value=1e-7,
    format="%.1e"
)

L = st.number_input(
    "Box size (L)",
    min_value=1.0,
    max_value=100.0,
    value=10.0,
    step=1.0
)

x = st.number_input(
    "Particle x position",
    min_value=0.0,
    max_value=float(L),
    value=float(L / 2)
)

y = st.number_input(
    "Particle y position",
    min_value=0.0,
    max_value=float(L),
    value=float(L / 2)
)

x_0 = st.number_input(
    "Particle x position destination",
    min_value=0.0,
    max_value=float(L),
    value=float(L / 2)
)

y_0 = st.number_input(
    "Particle y position destination",
    min_value=0.0,
    max_value=float(L),
    value=float(L / 2)
)


particle_mass = st.number_input(
    "Particle mass",
    min_value=0.1,
    value=1.0
)

particle_charge = st.number_input(
    "Particle charge",
    value=1.0
)

# Video Parameter

num_frames = st.slider(
    "Number of video frames",
    min_value=50,
    max_value=1000,
    value=300,
    step=50
)

# Boundary conditions

distribution = st.selectbox(
    "Boundary distribution",
    ["gaussian", "sinusoidal", "parabolic", "linear", "zeros"]
)

if st.button("Run Simulation"):
    # Start the timer
    start_time = time.perf_counter()
    with st.spinner("Running simulation..."):

        #Boundary Conditions
        grid = np.zeros((const.N+2)*(const.N+2))
        grid, first_time = Potential.get_values(distribution, grid, first_time=True)

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
               and steps < max_steps
        ):

            new_values = step_switching(x, y, x_0, y_0)
            grid, first_time = Potential.get_values(distribution, grid, first_time, new_values)

            phi = Potential.jacobi(grid)
            phi_history.append(phi.copy())

            p.update_pos(
                phi,
                dL,
                dt,
                X,
                Y
            )

            x = p.position[0]
            y = p.position[1]
            
            disp_x = x - x_0
            disp_y = y - y_0

            steps += 1

        print("Number of particle positions:", len(p.posn_hist_x))
        print("Starting video...")
        # Generate video
        video(
            p,
            phi_history,
            X,
            Y,
            num_frames
        )
        print("Video finished")
    st.success("Simulation complete!")

    # Display video
    st.video("particle.mp4")

    # Stop the timer
    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    print(f"Executed in: {elapsed_time:.4f} seconds")