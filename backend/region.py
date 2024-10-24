# import sys
# import json
# from qgis.core import *
# from qgis.analysis import QgsNativeAlgorithms
# import os

# sys.path = ['/Applications/QGIS.app/Contents/MacOS/../Resources/python', '/Users/ruthvikkodati/Library/Application Support/QGIS/QGIS3/profiles/default/python', '/Users/ruthvikkodati/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins', '/Applications/QGIS.app/Contents/MacOS/../Resources/python/plugins', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/statsmodels-0.11.1-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/pyproj-3.2.0-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/Rtree-0.9.7-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/scipy-1.5.1-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/rasterio-1.1.5-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python39.zip', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/netCDF4-1.5.4-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/Fiona-1.8.13.post1-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/lib-dynload', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/patsy-0.5.1-py3.9.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/pandas-1.3.3-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/cftime-1.2.1-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/opencv_contrib_python-4.3.0.36-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/geopandas-0.8.1-py3.9.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/matplotlib-3.3.0-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/numba-0.50.1-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/Pillow-7.2.0-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/GDAL-3.3.2-py3.9-macosx-10.13.0-x86_64.egg', '/Applications/QGIS.app/Contents/MacOS/lib/python3.9/site-packages/numpy-1.20.1-py3.9-macosx-10.13.0-x86_64.egg', '/Users/ruthvikkodati/Library/Application Support/QGIS/QGIS3/profiles/default/python']

# QgsApplication.setPrefixPath('/Applications/QGIS.app/Contents/Resources', True)
# app = QgsApplication([], True)
# QgsApplication.initQgis()

# from processing.core.Processing import Processing

# Processing.initialize()
# import processing

import sys
import json
from qgis.core import *
from qgis.analysis import QgsNativeAlgorithms
import os

# Set the paths for Ubuntu/Docker environment
sys.path.extend([
    '/usr/share/qgis/python',
    '/usr/share/qgis/python/plugins',
    '/usr/lib/python3/dist-packages',
    '/usr/lib/python3/dist-packages/qgis',
    '/usr/share/qgis/python/qgis'
])

# Initialize QGIS application
QgsApplication.setPrefixPath('/usr', True)
app = QgsApplication([], False)  # False for headless
app.initQgis()

# Initialize processing framework
import processing
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

rent_data = {
    "Vikhroli": [[5, 9], [35, 65], [70, 110]],
    "Vile Parle": [[25, 50], [50, 70], [80, 115]],
    "Andheri West": [[9, 16], [55, 85], [160, 190]],
    "Chandivali": [[10, 20], [40, 65], [80, 105]],
    "Ghatkopar West": [[8, 13], [30, 55], [60, 80]],
    "Vandre West": [[25, 40], [50, 70], [195, 230]],
    "Ghatkopar East": [[20, 40], [25, 50], [60, 85]],
    "Kurla (SC)": [[20, 35], [40, 60], [60, 85]],
    "Mankhurd Shivaji Nagar": [[5, 25], [30, 50], [60, 85]],
    "Kalina": [[20, 35], [50, 70], [85, 110]],
    "Vandre East": [[15, 25], [60, 90], [100, 140]],
    "Sion Koliwada": [[5, 20], [25, 50], [65, 95]],
    "Dharavi (SC)": [[5, 12], [20, 45], [50, 85]],
    "Chembur": [[4, 8], [35, 65], [70, 90]],
    "Borivali": [[10, 20], [25, 45], [50, 75]],
    "Magathane": [[8, 18], [20, 45], [50, 80]],
    "Dahisar": [[10, 20], [20, 30], [40, 100]],
    "Mulund": [[17, 30], [30, 50], [60, 85]],
    "Malad West": [[5, 13], [20, 35], [52, 75]],
    "Charkop": [[9, 15], [20, 38], [40, 62]],
    "Kandivali East": [[18, 25], [27, 38], [40, 65]],
    "Jogeshwari East": [[11, 16], [40, 55], [90, 120]],
    "Dindoshi": [[22, 34], [45, 65], [80, 125]],
    "Goregaon": [[12, 22], [30, 45], [55, 90]],
    "Andheri East": [[11, 16], [30, 42], [80, 130]],
    "Versova": [[20, 35], [50, 70], [80, 110]],
    "Bhandup West": [[5, 8], [32, 45], [40, 85]],
    "Wadala": [[30, 55], [60, 90], [100, 145]],
    "Anushakti Nagar": [[15, 35], [40, 65], [75, 100]],
    "Mahim": [[30, 50], [50, 70], [85, 135]],
    "Shivadi": [[25, 40], [40, 60], [70, 95]],
    "Worli": [[18, 38], [100, 140], [160, 220]],
    "Mumbadevi": [[45, 60], [60, 80], [80, 120]],
    "Colaba": [[60, 80], [80, 150], [200, 360]],
    "Byculla": [[27, 43], [55, 85], [90, 130]],
    "Malabar Hill": [[55, 85], [95, 145], [160, 300]],
}

inital_path = "shapefiles/"


def dissolveLayer(layer):
    dissolve_config = {
        "FIELD": [],
        "INPUT": layer,
        "OUTPUT": "TEMPORARY_OUTPUT",
    }

    dissolve_layer = processing.run("native:dissolve", dissolve_config)["OUTPUT"]

    return dissolve_layer


def bufferLayer(query, distance):
    # vector_layer = QgsVectorLayer(inital_path + query + ".shp")
    # print(vector_layer.featureCount())
    buffer_config = {
        "DISSOLVE": False,
        "DISTANCE": distance,
        "END_CAP_STYLE": 0,
        "INPUT": inital_path + query + ".shp",
        "JOIN_STYLE": 0,
        "MITER_LIMIT": 2,
        "OUTPUT": "TEMPORARY_OUTPUT",
        "SEGMENTS": 5,
    }
    buffer_layer = processing.run("native:buffer", buffer_config)["OUTPUT"]

    return buffer_layer


def mergeLayers(layers):
    initial_layer = layers[0]
    for i in range(1, len(layers)):
        intersection_config = {
            "INPUT": initial_layer,
            "INPUT_FIELDS": [],
            "OUTPUT": "TEMPORARY_OUTPUT",
            "OVERLAY": layers[i],
            "OVERLAY_FIELDS": [],
            "OVERLAY_FIELDS_PREFIX": "",
        }
        initial_layer = processing.run("native:intersection", intersection_config)[
            "OUTPUT"
        ]
    return initial_layer


def getSuburbs(query):
    budget = query["budget"]
    type = query["type"]
    index = int(type[0]) - 1
    names = []
    
    minimum_budget_threshold = 4000  

    if budget < minimum_budget_threshold:
        print("Budget is too low, nothing to highlight.")
        return  # If the budget is too low, exit early
    
    for key in rent_data:
        rent_range = rent_data[key][index]
        if (rent_range[0] * 1000 <= budget and rent_range[1] * 1000 >= budget) or budget >= rent_range[1] * 1000:
                names.append(key)
    with open("shapefiles/suburbs.json", "r") as f:
        suburbs = json.load(f)
    features = []
    for feature in suburbs["features"]:
        if feature["properties"]["AC_NAME"] in names:
            features.append(feature)

    if len(features) > 0:
        suburbs["features"] = features
    else:
        print("No matching regions for the given budget.")

    with open("shapefiles/target_region.json", "w") as f:
        json.dump(suburbs, f)


def getRegion(query):
    layers = []
    for key in query:
        if key != "budget" and key != "type":
            layers.append(dissolveLayer(bufferLayer(key, query[key])))
    final_layer = dissolveLayer(mergeLayers(layers))


    clip_config = {
        "INPUT": inital_path + "target_region.json",
        "OUTPUT": "TEMPORARY_OUTPUT",
        "OVERLAY": final_layer,
    }
    region = processing.run("native:clip", clip_config)["OUTPUT"]
    output_path = os.path.abspath(os.path.join("outputs", "region.json"))
    # print("hello")
    
    # print("Writing to:", output_path)
    QgsVectorFileWriter.writeAsVectorFormat(
        region,
        output_path,
        "utf-8",
        QgsCoordinateReferenceSystem("EPSG:4326"),
        "GeoJson",
    )


# query = {
#     "banks": 0.009,
#     "restaurants": 0.0045,
# }
# getRegion(query)
