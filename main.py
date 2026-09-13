import os
import numpy as np
import streamlit as st
import constants as const
from boundary_class import boundaries
from potential_class import potential
from particle_class import particle
from video import video

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

particle_x = st.number_input(
    "Particle x position",
    min_value=0.0,
    max_value=float(L),
    value=float(L / 2)
)

particle_y = st.number_input(
    "Particle y position",
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

    with st.spinner("Running simulation..."):

        #Boundary Conditions
        boundary = boundaries(distribution)
        M = boundary.get_values()

        # Solve Laplace equation
        phi = potential.jacobi(M)

        # Coordinate system
        X = np.linspace(0, L, const.N + 2)
        Y = np.linspace(0, L, const.N + 2)

        dL = X[1] - X[0]

        # Create particle
        p = particle(
            mass=particle_mass,
            charge=particle_charge,
            init_pos=[particle_x, particle_y]
        )

        # Particle simulation
        dt = 0.01

        while not p.exit_box:

            p.update_pos(
                phi,
                dL,
                dt,
                X,
                Y
            )


        print("Number of particle positions:", len(p.posn_hist_x))
        print("Starting video...")
        # Generate video
        video(
            p,
            phi,
            X,
            Y,
            num_frames
        )
        print("Video finished")
    st.success("Simulation complete!")

    # Display video
    st.video("particle.mp4")