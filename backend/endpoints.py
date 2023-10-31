import os
import json
import time
import random
import datetime
import psycopg2
import sqlalchemy
import requests
from sqlalchemy import or_ , String, and_
from sqlalchemy import update, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_utils import database_exists, create_database

from dataclasses import dataclass
from flask import Flask, request, send_from_directory, current_app, url_for
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint

from convert import manage_conversion
from util import load_saved_datasheeet

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Datasheets Backend"
    }
)
app.register_blueprint(swaggerui_blueprint)

ma = Marshmallow(app)
cors = CORS(app)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['BACKUP_DIRECTORY'] = './'

Base = declarative_base()

@app.route('/static/<path:filename>')
def send_static(filename):
    return send_from_directory(directory="/static", path=filename)


def prepare_error_response(message):
    return {'status_code': 500, 'message': message}


def prepare_success_response(message=None, data=None):
    return {'status_code': 200, 'message': message, 'data': data}


def create_database_connection():
    db_user = os.getenv("POSTGRES_DB_USER", 'postgres')
    db_pass =  os.getenv("POSTGRES_DB_PASS", 'postgres')
    db_host = os.getenv("POSTGRES_HOST", 'localhost')
    db_port = os.getenv("POSTGRES_PORT", 5432)
    db_name = os.getenv("POSTGRES_DB_NAME", 'kitt4sme-digital-datasheet-database')
    db_use_ssl = os.getenv("POSTGRES_USE_SSL")
    app.logger.debug(str(db_user)+","+str(db_pass)+","+str(db_host)+","+str(db_port)+","+str(db_name)+","+str(db_use_ssl))
    engine = sqlalchemy.create_engine(
        "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            db_user,
            db_pass,
            db_host,
            db_port,
            db_name
        )
    )

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine)
    session = sqlalchemy.orm.sessionmaker()
    session.configure(bind=engine)
    session = session()
    return session

def validate_marketplace(datasheet):
    retval = False
    # If datasheet hasn't been validated or too much time has passed since last validation
    app.logger.debug("validation status: "+ str(datasheet.validation))
    if (datasheet.validation_ts == None):
        datasheet.validation_ts = 0
    print("datasheet: "+str(datasheet.datasheet))
    if (datasheet.validation == -1 or datasheet.validation_ts < time.time()-int(os.environ["VALIDATION_TIMEOUT"])*3600):
        validate_api = os.environ["VALIDATION_URL"]+datasheet.datasheet["datasheet"]["information"]["component_uuid"]
        print(validate_api)
        ret = requests.get(validate_api)
        session = create_database_connection()
        if (ret.status_code != 200):
            query = (update(Datasheets).where(Datasheets.id == datasheet.id).values(validation=0, validation_ts=time.time()))
        else:
            query = (update(Datasheets).where(Datasheets.id == datasheet.id).values(validation=1, validation_ts=time.time()))
            retval = True
        session.execute(query)
        session.commit()
    else:
        if (datasheet.validation == 1 ):
            retval = True
    print("validation result: "+str(retval))
    return retval

"""
    Start of Backup API
"""
@app.route('/backup-datasheets', methods=['GET'])
@cross_origin()
def backup_datasheets():
    session = create_database_connection()
    datasheets = session.query(Datasheets).all()

    backup_dir = current_app.config['BACKUP_DIRECTORY']
    backup_filename = f"datasheets_backup_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

    backup_path = os.path.join(backup_dir, backup_filename)

    datasheet_schema = DatasheetsSchema()
    with open(backup_path, 'w') as backup_file:
        for datasheet in datasheets:
            json.dump(datasheet_schema.dump(datasheet), backup_file)
            backup_file.write('\n')

    backup_url = url_for('download_backup', filename=backup_filename, _external=True)

    return prepare_success_response('Backup created.', {'backup_url': backup_url})



@app.route('/download-backup/<path:filename>', methods=['GET'])
@cross_origin()
def download_backup(filename):
    backup_dir = current_app.config['BACKUP_DIRECTORY']
    print("file path ", filename )
    return send_from_directory(directory=backup_dir, path=filename)


@app.route('/backup-files', methods=['GET'])
@cross_origin()
def get_backup_files():
    backup_dir = current_app.config['BACKUP_DIRECTORY']
    backup_files = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))]
    backup_urls = [url_for('download_backup', filename=f, _external=True) for f in backup_files]

    return prepare_success_response('List of backup files.', {'backup_files': backup_files, 'backup_urls': backup_urls})


"""
    End of Backup API
"""

"""
Query, Extract, and Convert Datasheets from Numberic representation to Human Readable
"""
@app.route('/datasheets-numberic-to-human-readable', methods=['GET'])
@cross_origin()
def convert_datasheet():
    try:
        session = create_database_connection()
        result = session.query(Datasheets).all()
        print(len(result))
        for datasheet in result:
            manage_conversion([datasheet.datasheet])
        return prepare_success_response()
    except psycopg2.Error:
        return prepare_error_response('Failed to convert.')

"""
    Start of Datasheets API
"""


@dataclass
class Datasheets(Base, SerializerMixin):
    __tablename__ = 'datasheets'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    keycloak_id = sqlalchemy.Column(sqlalchemy.String(length=100))
    datasheet = sqlalchemy.Column(sqlalchemy.JSON())
    validation = sqlalchemy.Column(sqlalchemy.Integer)
    validation_ts = sqlalchemy.Column(sqlalchemy.BigInteger)


class DatasheetsSchema(ma.Schema):
    class Meta:
        fields = ("id", "keycloak_id", "datasheet", "validation", "validation_ts")

datasheet_schema = DatasheetsSchema()
datasheet_schema = DatasheetsSchema(many=True)

@app.route('/datasheets-delete/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_datasheet(id):
    session = create_database_connection()
    datasheet = session.query(Datasheets).get(id)
    if not datasheet:
        return prepare_error_response('Datasheet not found.')
    try:
        session.delete(datasheet)
        session.commit()
        return prepare_success_response('Datasheet removed.')
    except psycopg2.Error:
        session.rollback()
        return prepare_error_response('Failed to delete.')

def parse_words(text):
    ignore_array = ["","a", "in", "into", "to","with"]
    ret = []
    if (len(text) > 0):
        words = text.split(" ")
        for word in words:
            if word in ignore_array:
                print("ignoring word: "+word)
            else:
                ret.append(word.lower())
    return ret

def get_property_words(selected_checkboxes, schema):
    ret = []
    for checkbox in selected_checkboxes:
        box_element = checkbox.split(".")
        issues = schema["module_property"]["properties"][box_element[1]]["items"]["properties"]["issue"]["oneOf"]
        index = int(box_element[2].split("_")[1])
        print(issues)
        words = parse_words(issues[index-1]["title"])
        for word in words:
            if word not in ret:
                ret.append(word)
    return ret

@app.route("/datasheets-search", methods=['POST'])
@cross_origin()
def return_all_datasheets():
    try:
        with open("content.json", 'r') as file:
            schema = json.load(file)
        session = create_database_connection()
        payload = request.json
        print("TEST")
        selected_checkboxes = payload.get('selectedCheckboxes')
        filter_text = payload.get('filter')
        print("checkboxes:")
        print(selected_checkboxes)
        print("filter_text:")
        print(filter_text)
        search_words = parse_words(filter_text)
        search_words.extend(get_property_words(selected_checkboxes, schema))
        return_sheets = []
        query = session.query(Datasheets)
        search_words = parse_words(filter_text)
        print("search_words:")
        print(search_words)

        result = query.all()    
        datahseets = datasheet_schema.dump(result)
        #print(datahseets)
        keywords = []
        for datasheet in datahseets:
            found = True
            print("datasheet:")
            #print(datasheet)
            information = datasheet["datasheet"]["information"]
            print(information)
            keywords.extend(parse_words(information["component_accronym"]))
            keywords.extend(parse_words(information["component_name"]))
            keywords.extend(parse_words(information["provider"]))
            print(keywords)
            # context elements
            context = datasheet["datasheet"]["context"]
            #print("context:")
            #print(context)
            keywords.extend(parse_words(context["description"]))

            if (context["productiveaxis"]["ai_hri"]):
                keywords.extend(parse_words(schema["productiveaxis"]["properties"]["ai_hri"]["title"]))
            if (context["productiveaxis"]["ai_quality"]):
                keywords.extend(parse_words(schema["productiveaxis"]["properties"]["ai_quality"]["title"]))
            if (context["productiveaxis"]["ai_manualactivity"]):
                keywords.extend(parse_words(schema["productiveaxis"]["properties"]["ai_manualactivity"]["title"]))
            if (context["category"]["reasoning"]):  
                keywords.extend(parse_words(schema["category"]["properties"]["reasoning"]["title"]))
            if (context["category"]["decisionmaker"]):
                keywords.extend(parse_words(schema["category"]["properties"]["decisionmaker"]["title"]))
            #print("keywords after context")
            #print(keywords)
            module_properties = datasheet["datasheet"]["module_properties"]
            
            if (len(search_words) > 0):
                matches = 0 
                for word in search_words:
                    if word in keywords:
                        matches = matches + 1
                if (matches == 0):
                    found = False

            # module_properties elements
            properties = len(selected_checkboxes)
            for checkbox in selected_checkboxes:
                box_element = checkbox.split(".")
                for issue in module_properties[box_element[1]]:
                    index = int(box_element[2].split("_")[1])
                    if (int(issue["issue"]) == index):
                        properties = properties - 1

            if (found and properties <= 0):
                print("append datasheet")
                print(datasheet)
                return_sheets.append(datasheet)
    except KeyError:
        print("Error fetching datasheets")
        return prepare_error_response('Failed to search.')      
    return prepare_success_response(data=return_sheets)

"""
Return all datasheets
"""
@app.route('/datasheets', methods=['GET'])
@cross_origin()
def get_datasheets():
    try:
        session = create_database_connection()
        result = session.query(Datasheets).all()
        results = []
        print(str(len(result))+" args: "+str(request.args))
        for datasheet in result:
            if(request.args.get('validate') == '1'):
                if (validate_marketplace(datasheet)):
                    results.append(datasheet.datasheet)
            else:
                results.append(datasheet.datasheet)
        print(results)
        return prepare_success_response(data=results)
    except psycopg2.Error:
        return prepare_error_response('Failed to retrieve datasheets from DB')

@app.route("/datasheets", methods=['POST'])
@cross_origin()
def insert_new_datasheet():
    try:
        data = request.get_json()
        keycloak_id = data['keycloak_id']
        session = create_database_connection()
        insert_data = Datasheets(keycloak_id=keycloak_id, datasheet=data)
        session.add(insert_data)
        session.commit()
        return prepare_success_response(message="Successfully created a new datasheet")
    except psycopg2.Error:
        return prepare_error_response('Failed to submit datasheet.')


@app.route("/datasheets", methods=['PUT'])
@cross_origin()
def update_existing_datasheet():
    try:
        data = request.get_json()
        datasheet_id = data['datasheet_id']
        session = create_database_connection()
        query = (update(Datasheets).where(Datasheets.id == datasheet_id).values(datasheet=data))
        session.execute(query)
        session.commit()
        return prepare_success_response(message="Successfully updated the datasheet")
    except psycopg2.Error:
        return prepare_error_response('Failed to submit datasheet.')

"""
    End of Datasheet API
"""

"""
    Start of Customer API
"""


@dataclass
class Customers(Base, SerializerMixin):
    __tablename__ = 'customers'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    keycloak_id = sqlalchemy.Column(sqlalchemy.String(length=100))


class CustomersSchema(ma.Schema):
    class Meta:
        fields = ("id", "keycloak_id")


customer_schema = CustomersSchema()
customer_schema = CustomersSchema(many=True)


@app.route("/customer", methods=['GET'])
@cross_origin()
def return_all_customers():
    try:
        session = create_database_connection()
        results = session.query(Customers).all()
        return prepare_success_response(data=customer_schema.dump(results))
    except psycopg2.Error:
        return prepare_error_response('Failed to return customers.')


@app.route("/customer", methods=['POST'])
@cross_origin()
def insert_new_customer():
    try:
        data = request.get_json()
        keycloak_id = data['keycloak_id']
        session = create_database_connection()
        customer = Customers(keycloak_id=keycloak_id)
        session.add(customer)
        session.commit()
        return prepare_success_response(message="Successfully created a new customer")
    except psycopg2.Error:
        return prepare_error_response('Failed.')


"""
    End of Customer API
"""
if __name__ == '__main__':
    app.run(
        debug=os.getenv("DEBUG", False),
        host='0.0.0.0',
        port="5001"
    )
