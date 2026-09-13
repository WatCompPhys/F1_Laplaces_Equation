import numpy as np
import matplotlib.pyplot as plt
import imageio as iio
import os

def video(p, phi, X, Y, num_frames):
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
    ax.set_title("Particle in Box Simulation", color="Black")

    ax.set_xticks(np.arange(np.min(X), np.max(X) + 1, 1))
    ax.set_yticks(np.arange(np.min(Y), np.max(Y) + 1, 1))

    particle = ax.scatter([], [], color="red", s=100)
    trail, = ax.plot([], [], linewidth=2)

    # Draw the static background once
    fig.canvas.draw()
    background = fig.canvas.copy_from_bbox(ax.bbox)

    particle.set_animated(True)
    trail.set_animated(True)

    frame_step = max(1, len(p.posn_hist_x) // num_frames)
    
    with iio.get_writer(Video_path, fps=30, codec="libx264") as writer:
        for i in range(0, len(p.posn_hist_x), frame_step):

            fig.canvas.restore_region(background)

            # Move particle
            particle.set_offsets([[p.posn_hist_x[i], p.posn_hist_y[i]]])

            # Update trail
            trail.set_data(p.posn_hist_x[:i+1], p.posn_hist_y[:i+1])

            ax.draw_artist(trail)
            ax.draw_artist(particle)

            # Convert the Matplotlib figure to a NumPy image array
            fig.canvas.blit(ax.bbox)
            frame = np.asarray(fig.canvas.buffer_rgba())
            writer.append_data(frame)

    plt.close(fig)  # close the figure to save memory