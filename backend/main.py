

""" nope bout to work on some psych.
-add_initial_data.py will add the airports and flight data to the gdb
-get_airports.py will return an array of airports in the gdb
-find_path.py, get_all_valid_paths will return all valid paths and then convert_paths_to_json will convert it to a json """
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
cors = CORS(app, resources={r'/*': {'origins': '*'}})
#app.config['CORS_HEADERS'] = 'Content-Type'



@app.route("/flights", methods=['GET'])
def get_flight():
  return jsonify(fp.convert_paths_to_json(fp.get_paths(
    request.args.get("departure", default="", type=str),
    request.args.get("destination", default="", type=str),
    5
)))


@app.route("/airports", methods=['GET'])
def get_airports():
  return jsonify(get_airports_gdb().tolist())


if __name__ == '__main__':
  
  app.run(debug=True,host='0.0.0.0')


