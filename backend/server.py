import sys
from region import getRegion, getSuburbs
import os

# sys.path.append("C:\\Users\\HP\\miniconda3\\lib\\site-packages")

from flask import Flask, request, make_response, send_from_directory
import json
from flask_cors import CORS

app = Flask(__name__, static_folder='frontend-build')
CORS(app, resources={r"/*": {"origins": "*"}})  # Configure CORS for all routes

# Serve React App for root URL
@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (JS, CSS, images, etc.)
@app.route('/<path:path>')
def serve_static_files(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, 'index.html')

@app.route("/getRegion", methods=["POST", "OPTIONS"])
def getQueryRegion():
    if request.method == "OPTIONS":  # Handle preflight request
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    
    data = dict(request.form)
    # print(data)
    new_data = {}
    for key in data:
        if key == "type":
            new_data[key.lower()] = data[key]
        elif key == "budget":
            new_data[key.lower()] = int(data[key])
        else:
            new_data[key.lower()] = float(data[key]) * 0.009

    getSuburbs(new_data)

    if len(new_data) == 2:
        # Check if the file exists
        target_region_path = "shapefiles/target_region.json"
        if os.path.exists(target_region_path):
            # print(f"Reading from {target_region_path}")
            with open(target_region_path, "r") as f:
                content = f.read()
                # print("File content:", content)  # Debug print
                try:
                    region = json.loads(content)  # Safely load the file contents
                except json.JSONDecodeError as e:
                    return make_response(f"Error decoding JSON: {str(e)}", 500)
        else:
            return make_response("target_region.json not found", 404)
    else:
        getRegion(new_data)
        region_file_path = "outputs/region.json"
        if os.path.exists(region_file_path):
            # print(f"Reading from {region_file_path}")
            with open(region_file_path, "r") as f:
                content = f.read()
                # print("File content:", content)  # Debug print
                try:
                    region = json.loads(content)  # Safely load the file contents
                except json.JSONDecodeError as e:
                    return make_response(f"Error decoding JSON: {str(e)}", 500)
        else:
            return make_response("region.json not found", 404)

    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.data = json.dumps({"region": region})
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
