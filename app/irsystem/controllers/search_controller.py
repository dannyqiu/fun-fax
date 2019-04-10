from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Fun Fax"
net_id = "Arshi Bhatnagar (ab2248), Danny Qiu (dq29), Rebecca Jiang (rwj52), Nehal Rawat (nr338), Ryan Davila (rmd252)"

@irsystem.route('/search', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


@irsystem.route('/', methods=['GET'])
def index():
    return render_template('index.html')
