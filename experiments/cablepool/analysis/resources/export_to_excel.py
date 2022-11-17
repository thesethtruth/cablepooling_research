import pandas as pd
from pathlib import Path

FOLDER = Path(__file__).parent

for dataset in FOLDER.glob("*nal.pkl"):

    df = pd.read_pickle(dataset).to_excel(dataset.stem + ".xlsx")
