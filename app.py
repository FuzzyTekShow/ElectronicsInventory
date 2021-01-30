import configparser
import datetime
import os

from bson import ObjectId
from flask import Flask, render_template, request, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename

################
version = "0.1"
################

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
config.set('systemSettings', 'version', version)

client = MongoClient('mongodb://localhost:27017/')
db = client["electronics_inventory"]
components_col = db["components"]

component_headers = ("Name", "Location", "Footprint", "Amount",
                     "Datasheet", "Entry Date", "Updated Date", "Comment")


def get_component_data():
    table_components = []

    for component in components_col.find():
        component['entry_date'] = component['entry_date'].strftime(config['userSettings']['dateFormat'])
        component['updated_date'] = component['updated_date'].strftime(config['userSettings']['dateFormat'])
        table_components.append(list(component.values()))

    return table_components


@app.route('/')
def index():
    return render_template('index.html', config=config, table_headers=component_headers, table_components=get_component_data())


@app.route('/error/<string:e>')
def error(e):
    return render_template('error.html', error=e)


@app.route('/add', methods=['POST'])
def add():
    try:
        data = request.form
        date = datetime.datetime.now()
        datasheet = ""

        # If there is no uploaded file
        if request.files.get('datasheetUpload').filename == None:
            datasheet = data['datasheetLink']
        else: # Otherwise try to save it
            file = request.files.get('datasheetUpload')
            fileDiskLocation = save_datasheet(file)
            # Check that it's valid
            if fileDiskLocation == "{}/{}".format(config['userSettings']['datasheetDIR'], file.filename):
                datasheet = file.filename
            else: # If all is well, return the location on the disk
                return str(fileDiskLocation)

        component_to_add = {"name": data['name'], "location": data['location'], "footprint": data['footprint'],
                            "amount": data['amount'], "datasheet": datasheet, "entry_date": date, "updated_date": date,
                            "comment": data['comment']}
        result = components_col.insert_one(component_to_add)
        return str(result.acknowledged)
    except Exception as e:
        return str(e)


@app.route('/remove', methods=['POST'])
def remove():
    try:
        data = request.form
        result = components_col.delete_one(ObjectId(data['id']))
        return result
    except Exception as e:
        return str(e)


@app.route('/update', methods=['POST'])
def update():
    try:
        data = request.form
        date = datetime.datetime.now()

        result = components_col.find_one_and_update({'_id': ObjectId(data['id'])},
                              {"$set": {
                                  "name": data['name'],
                                  "location": data['location'],
                                  "footprint": data['footprint'],
                                  "amount": data['amount'],
                                  "datasheet": data['datasheet'],
                                  "updated_date": date,
                                  "comment": data['comment']
                              }})
        if result is not None:
            return "True"
    except Exception as e:
        return str(e)


def save_datasheet(file):
    try:
        filename = secure_filename(file.filename)
        saveDIR = config['userSettings']['datasheetDIR']

        # If file exists, return an error
        if (os.path.exists(saveDIR + "/" + filename)):
            raise FileExistsError("A datasheet with than file name already exists.")

        file.save(os.path.join(saveDIR, filename))
        return saveDIR + "/" + filename
    except Exception as e:
     return str(e)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5555, debug=False)
