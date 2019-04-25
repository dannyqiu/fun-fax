#!/bin/sh

python3 -m spacy download en_core_web_lg

python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

