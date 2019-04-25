from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from ..models.search import WeightedEmbeddingSearch

search_model = WeightedEmbeddingSearch()

@irsystem.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if query:
        results = search_model.search(query)
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
