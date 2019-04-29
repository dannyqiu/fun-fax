from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from ..models.search import WeightedEmbeddingClusteringSearch

search_model = WeightedEmbeddingClusteringSearch()

@irsystem.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', default=None)
    if query:
        category = request.args.get('category', default=None)
        sort_method = request.args.get('sort', default="similarity")
        recency_sort = request.args.get('recency', default=None)
        results = search_model.search(query, sort_method=sort_method, recency_sort=recency_sort)
    else:
        results = []
    return http_resource(results, "results", True)


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
