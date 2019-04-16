from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from ..models.search import BooleanSearch

search_model = BooleanSearch()

@irsystem.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if query:
        results = search_model.search(query)
    else:
        results = []
    return http_resource(results, "results", True)
