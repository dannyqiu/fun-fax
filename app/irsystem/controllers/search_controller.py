from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from ..models.search import WeightedEmbeddingClusteringSearch
from ..models.utils import decode_numpy_array

search_model = WeightedEmbeddingClusteringSearch()

@irsystem.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', default=None)
    if query:
        category = request.args.get('category', default=None)
        sort_method = request.args.get('sort', default="relevancy")
        recency_sort = request.args.get('recency', default=None)
        results, words = search_model.search(query, category, sort_method=sort_method, recency_sort=recency_sort)
    else:
        results, words = [], []
    return http_resource2(results, "results", words, "words", True)

@irsystem.route('/more', methods=['GET'])
def see_more():
    query = request.args.get('q', default=None)
    if query:
        query_vector = decode_numpy_array(query)
        category = request.args.get('category', default=None)
        sort_method = request.args.get('sort', default="relevancy")
        recency_sort = request.args.get('recency', default=None)
        results, words = search_model.see_more(query_vector, category, sort_method=sort_method, recency_sort=recency_sort)
    else:
        results, words = [], []
    return http_resource2(results, "results", words, "words", True)

@irsystem.route('/random', methods=['GET'])
def random():
    category = request.args.get('category', default=None)
    results, words = search_model.random(category)
    return http_resource2(results, "results", words, "words", True)


from ..models.search import DummySearch
dummy_search_model = DummySearch()

@irsystem.route('/dummy', methods=['GET'])
def dummy():
    query = request.args.get('q')
    if query:
        results = dummy_search_model.search(query)
    else:
        results = []
    return http_resource(results, "results", True)
