from pathlib import Path
from zipfile import ZipFile
import io
import requests

URL = "https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce"
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

if __name__ == "__main__":
    RAW.mkdir(parents=True, exist_ok=True)
    response = requests.get(URL, timeout=120)
    response.raise_for_status()
    with ZipFile(io.BytesIO(response.content)) as archive:
        for member in archive.infolist():
            if member.filename.endswith(".csv"):
                target = RAW / Path(member.filename).name
                target.write_bytes(archive.read(member))
                print(f"raw: {target.name}")
