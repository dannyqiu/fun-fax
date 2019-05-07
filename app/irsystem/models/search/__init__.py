import os
import re

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
    "created_utc",
    "num_comments",
]

OPTIONAL_COLUMNS = [
    "thumbnail",
]

BANNED_SUBREDDITS = [
    'circlejerk',
    'ShittyTodayILearned',
    'ShittyYouShouldKnow',
    'TheOnion',
    'WTF',
    'FULLCOMMUNISM',
    'circlejerkseattle',
    # non-english
    'Suomi',
    'BitcoinDK',
    'BitcoinNO',
    'brasil',
    'greece',
    'novotvorenice'
    'mkd',
    'Romania',
    'Denmark',
    'sweden',
    'ektenyheter',
    'norge',
    'ntnu',
    'newsokur',
    'Iceland',
    'todayilearned_jp',
    'JuropijanSpeling',
    'bybanen',
    'atakos',
    'italy',
    'RoCirclejerk',
]

TOKENIZATION_REGEX = re.compile(r"[a-z]+")

# Bring search models to package level
from .boolean import BooleanSearch
from .dummy import DummySearch
from .weighted_embedding import WeightedEmbeddingSearch
from .weighted_embedding_clustering import WeightedEmbeddingClusteringSearch
