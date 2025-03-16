import kagglehub
import shutil
from pathlib import Path

# Download latest version
download_path = str(Path(kagglehub.dataset_download("oktayrdeki/traffic-accidents")) / "traffic_accidents.csv")
destination_path = str(Path.cwd().parent.parent / "data" / "raw")

shutil.move(download_path, destination_path)
