from flask import Flask, request, make_response, jsonify
import dbhelpers, apihelpers, dbcreds

app = Flask(__name__)

@app.post("/api/post")
def post_post():
    error = apihelpers.check_endpoint_info(request.json, ["username", "content", "image_url"])
    if(error != None):
        return make_response(jsonify(error), 400)
    
    results = dbhelpers.run_procedure('call insert_post(?,?,?)', 
                            [request.json.get("username"),request.json.get("content"),request.json.get("image_url")])
    
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response("Sorry, there has been an error", 500)
    
@app.get("/api/post")
def get_posts():
    results = dbhelpers.run_procedure('call get_posts()', [])
    
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response("Sorry, there has been an error", 500)

if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Development Mode")
    app.run(debug=True)