import os

from app import app

DATA_DIR = os.path.abspath(os.path.join(app.instance_path, "..", "data"))
FUN_FACT_TITLE_CSV = os.path.abspath(os.path.join(DATA_DIR, "fun_fact_title.csv"))
TIL_TITLE_CSV = os.path.abspath(os.path.join(DATA_DIR, "til_title.csv"))
YSK_TITLE_CSV = os.path.abspath(os.path.join(DATA_DIR, "ysk_title.csv"))

REQUIRED_COLUMNS = [
    "title",
    "subreddit",
    "permalink",
    "score",
]

# Bring search models to package level
from .boolean import BooleanSearch
from .dummy import DummySearch
from .weighted_embedding import WeightedEmbeddingSearch
