import numpy as np
import matplotlib.pyplot as plt
import imageio as iio
import csv, os

def video(filename: str):
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
    
    fig, ax = plt.subplots(figsize=(8, 8), dpi=100, projection="3d")
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.axis('off')
    ax.set_xlim(-6,6)
    ax.set_ylim(-6,6)
    ax.set_zlim(-6,6)
    ax.set_title("Particle in Box Simulation", color="white")

    particle = ax.scatter([], [], color="red", s=300)

    with iio.get_writer(Video_path, fps=60, codec="libx264") as writer:
        with open(filename, 'r') as myfile:
            myfile = csv.DictReader(myfile)
            for row in myfile:

                x, y = float(row['x']), float(row['y'])

                particle.set_offsets([[x, y]])

                # Convert the Matplotlib figure to a NumPy image array
                fig.canvas.draw()
                frame = np.asarray(fig.canvas.buffer_rgba())
                writer.append_data(frame)

    plt.close(fig)  # close the figure to save memory