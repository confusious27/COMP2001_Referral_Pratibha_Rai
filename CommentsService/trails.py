# for trails (read only)
from flask import jsonify
from config import call_sql

# there is no procedure for this so call_proc won't work
def get_all_trails():
    rows = call_sql("SELECT * FROM CW2.Trail")
    if not rows:
        return {'message': 'No trails found'}, 404
    return jsonify(rows), 200