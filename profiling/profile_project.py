
import cProfile
import pstats
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PROFILE = ROOT / "profiling" / "profile.prof"
REPORT = ROOT / "profiling" / "profile_report.txt"

cProfile.run(
    "runpy.run_path(str(ROOT / 'profiling' / 'test_simulation.py'), run_name='__main__')",
    str(PROFILE)
)

# Generate report containing only project functions
with open(REPORT, "w") as file:
    stats = pstats.Stats(str(PROFILE), stream=file)

    project_functions = {
        key: value
        for key, value in stats.stats.items()
        if str(ROOT / "src") in str(Path(key[0]).resolve())
    }

    stats.stats = project_functions

    stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats()

print(f"Profiling complete!\nReport saved to: {REPORT}")
