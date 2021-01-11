import configparser
import datetime

from bson import ObjectId
from flask import Flask, render_template, request
from pymongo import MongoClient

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


@app.route('/addtodb', methods=['POST'])
def addToDb():
    data = request.form
    date = datetime.datetime.now()

    component_to_add = {"name": data['Name'], "location": data['Location'], "footprint": data['Footprint'],
                        "amount": data['Amount'], "datasheet": data['Datasheet'], "entry_date": date, "updated_date": date,
                        "comment": data['Comment']}
    x = components_col.insert_one(component_to_add)
    return addComponentPage(True)


@app.route('/addcomponent')
def addComponentPage(isAdded = None):
    return render_template('add.html', config=config, component_headers=component_headers, added=isAdded)


@app.route('/remove', methods=['POST'])
def removeItem():
    data = request.form
    x = components_col.remove(ObjectId(data['id']))
    return index()


@app.route('/update', methods=['POST'])
def updateItem():
    data = request.form
    date = datetime.datetime.now()
    x = components_col.find_one_and_update({'_id': ObjectId(data['id'])},
                              {"$set": {
                                  "name": data['name'],
                                  "location": data['location'],
                                  "footprint": data['footprint'],
                                  "amount": data['amount'],
                                  "datasheet": data['datasheet'],
                                  "entry_date": data['entry_date'],
                                  "updated_date": date,
                                  "comment": data['comment']
                              }})
    return index()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5555, debug=False)
