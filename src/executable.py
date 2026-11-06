import subprocess
import sys
import os

def launch_streamlit_app(app_path):
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", app_path])


script_dir = os.path.dirname(os.path.abspath(__file__))
app_file = os.path.join(script_dir, "main.py")

launch_streamlit_app(app_file)