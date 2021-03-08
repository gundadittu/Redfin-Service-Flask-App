from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import json 
import werkzeug

from . import query_handler 

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/query-sf-listings', methods=['GET'])
@cross_origin()
def query_sf_listings():
     street_address_arg = request.args.get('street_address')
     street_addr_query = str(street_address_arg) if street_address_arg else None
     valid_street_addr_query = street_addr_query and isinstance(street_addr_query, str)

     results = []
     if valid_street_addr_query: 
         results = query_handler.get_sf_listings_by_street_address(street_addr_query)
     else: 
         results = query_handler.get_all_sf_listings()

     return jsonify({ "error": None, "results": results})

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
     return jsonify({ "error": "Invalid request", "results": None}), 400