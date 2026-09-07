from potential import jacobi
import numpy as np
import matplotlib.pyplot as plt
import imageio as iio
import os

def video(p, phi, X, Y):
    """
    Take CSV data and generate plots at time t (frames),
    and compile them into a video
    """
    # Get directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Combine directory with filename
    Video_path = os.path.join(script_dir, "particle.mp4")

    if os.path.exists(Video_path):
        os.remove(Video_path)
        print(f"File '{Video_path}' deleted successfully.")
    else:
        print(f"File '{Video_path}' does not exist.")
    
    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)

    heatmap = ax.imshow(
        phi,
        extent=[
            np.min(X),
            np.max(X),
            np.min(Y),
            np.max(Y)
        ],
        origin="lower",
        cmap="magma"
    )

    fig.colorbar(heatmap, ax=ax, label="Potential")

    ax.set_facecolor('black')
    ax.set_xlim(np.min(X), np.max(X))
    ax.set_ylim(np.min(Y), np.max(Y))
    ax.set_aspect("equal")
    ax.set_title("Particle in Box Simulation", color="white")

    particle = ax.scatter([], [], color="red", s=100)
    trail, = ax.plot([], [], linewidth=2)

    with iio.get_writer(Video_path, fps=30, codec="libx264") as writer:
        for i in range(len(p.posn_hist_x)):

            x = p.posn_hist_x[i]
            y = p.posn_hist_y[i]

            # Move particle
            particle.set_offsets([[x, y]])

            # Update trail
            trail.set_data(
                p.posn_hist_x[:i+1],
                p.posn_hist_y[:i+1])          

            # Convert the Matplotlib figure to a NumPy image array
            fig.canvas.draw()
            frame = np.asarray(fig.canvas.buffer_rgba())
            writer.append_data(frame)

    plt.close(fig)  # close the figure to save memory