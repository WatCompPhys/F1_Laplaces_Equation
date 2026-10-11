import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as iio
import os


def video(p: object, phi_history: list, X: list, Y: list, num_frames: int):
    """
    Animate the particle and evolving electric potential.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(script_dir, "particle.mp4")

    if os.path.exists(video_path):
        os.remove(video_path)

    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)

    heatmap = ax.imshow(
        phi_history[0],
        extent=[
            np.min(X),
            np.max(X),
            np.min(Y),
            np.max(Y)
        ],
        origin="lower",
        cmap="magma",
        aspect="equal"
    )

    fig.colorbar(heatmap, ax=ax, label="Potential")

    ax.set_facecolor("black")
    ax.set_xlim(np.min(X), np.max(X))
    ax.set_ylim(np.min(Y), np.max(Y))
    ax.set_aspect("equal")
    ax.set_title("Particle in Box Simulation")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.set_xticks(np.arange(np.min(X), np.max(X) + 1, 1))
    ax.set_yticks(np.arange(np.min(Y), np.max(Y) + 1, 1))

    particle_plot = ax.scatter([], [], color="red", s=50, zorder=3)
    trail, = ax.plot([], [], color="cyan", linewidth=1.5, zorder=2)

    total_steps = min(
        len(p.posn_hist_x),
        len(p.posn_hist_y),
        len(phi_history)
    )

    if total_steps == 0:
        plt.close(fig)
        raise ValueError("No particle positions or potential snapshots were recorded.")

    frame_indices = np.linspace(
        0,
        total_steps - 1,
        min(num_frames, total_steps),
        dtype=int
    )

    with iio.get_writer(
        video_path,
        fps=30,
        codec="libx264"
    ) as writer:

        for i in frame_indices:
            # Update the electric potential
            heatmap.set_data(phi_history[i])

            # Update particle position
            particle_plot.set_offsets([
                [p.posn_hist_x[i], p.posn_hist_y[i]]
            ])

            # Update particle trail
            trail.set_data(
                p.posn_hist_x[:i + 1],
                p.posn_hist_y[:i + 1]
            )

            fig.canvas.draw()

            frame = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
            writer.append_data(frame)

    plt.close(fig)

    print(f"Video saved to: {video_path}")