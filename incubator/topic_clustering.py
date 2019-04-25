from collections import defaultdict
import pandas as pd
from . import TOPICS_CSV


class Topics:
	def __init__(self):
		self.subreddits_to_categories = self.subreddits()
		self._topics = self.categories_to_subreddits()
		self.categories_to_topics = self.categories(self._topics)


	def subreddits(self):
		data = pd.read_csv(TOPICS_CSV).dropna()
		d = {}
		for index, row in data.iterrows():
			if row[0] in d:
				d[row[0]].append(row[1])
			else:
				d[row[0]] = [row[1]]
		return d
	def categories(self,t):
		d = {}
		for key in t:
			for val in t[key]:
				if val in d:
					d[val].append(key)
				else:
					d[val] = [key]
		return d

	def categories_to_subreddits(self):
		d = {"general content": ["gifs", "people", "reaction", "science", "nature", "images",
		"interesting", "asian", "photoshop", "redditors", "wallpapers", "videos"],
		"discussion" : ["general", "advice", "ama", "games", "questions", "occupation", "sex/gender", "stories",
		"customer service", "revenge", "scary/weird", "support"],
		"educational" : ["general education", "facts", "educational question", "explain like...", "anthroplogy",
		"art", "cs", "econ", "enviornment", "history", "language", "law", "math", "medicine", "psychology", "science",
		"astronomy", "biology", "chemistry", "physics"],
		"entertainment" : ["general entertainment", "anime", "books/writing", "comics", "celebs", "cosplay", "games",
		"genres", "internet", "movies", "music","tv"], "hobbies": ["hobbies", "aquariums", "art", "writing", "automotives",
		"design", "guns", "jobs", "music", "outdoors", "hiking", "photography", "planes", "tech", "cs", "tools", "travel"], 
		"lifestyle": ["general lifestyle", "gender", "home", "general communities", "diet", "lgbt", "parenting", "alcohol",
		"drugs", "general health", "mental health", "physical", "excercise", "lifting", "running", "weight"],
		"fashion": ["makeup", "hair", "tattoos", "fashion", "shoes"],
		"food": ["food", "cooking", "diet", "drinks", "recipes"],
		"religion": ["religion", "philosophy"],
		"relationships": ["relationships", "family", "sex", "self-improvement"],
		"technology": ["technology", "3D Printing", "business-tech", "android", "apple", "gadgets", "hardware", "kodi",
		"google", "linux", "microsoft", "data", "digital currency", "programming", "sound"],
		"humor": ["general humor", "jokes", "memes", "irl"],
		"animals": ["animals"],
		"other": ["conspiracy", "cringe", "called out", "neckbeard", "cute", "eww", "angering", "edgy", "judgy", "scary",
		"creepy", "imaginary", "scary", "free", "men", "women", "geography", "meta", "apps", "drama", "negative",
		"positive", "subreddits", "mind blowing", "nature", "nostalgia", "parodies", "fettish", "bad", "unexpected",
		"appealing"],
		"news": ["politics", "news", "right wing", "capitalism", "left wing"]}
		return d