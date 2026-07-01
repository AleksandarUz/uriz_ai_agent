import os
import pandas as pd


def load_user_stories(file_path: str) -> list[dict]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Fajl ne postoji: {file_path}")

    df = pd.read_csv(file_path)

    required_columns = ["id", "title", "description", "priority", "status"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Nedostaje kolona u CSV fajlu: {column}")

    df = df.fillna("")

    return df.to_dict(orient="records")