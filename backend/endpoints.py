import os
import json
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

from convert import manage_conversion
from util import load_saved_datasheeet

app = Flask(__name__)
ma = Marshmallow(app)
cors = CORS(app)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['BACKUP_DIRECTORY'] = './'

Base = declarative_base()


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
    validate_api = os.environ["VALIDATION_URL"]+datasheet["component_uuid"]
    ret = requests.get(validate_api)
    if (ret.status_code != 200):
        return False
    return True

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


class DatasheetsSchema(ma.Schema):
    class Meta:
        fields = ("id", "keycloak_id", "datasheet")

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
    
@app.route("/datasheets-search", methods=['POST'])
@cross_origin()
def return_all_datasheets():
    try:
        session = create_database_connection()
        payload = request.json
        selected_checkboxes = payload.get('selectedCheckboxes')
        filter_text = payload.get('filter')

        query = session.query(Datasheets)

        filter_conditions = []

        for key in selected_checkboxes:
            json_key = key.replace('.', '->')
            json_key = json_key.split('->')
            value = json_key[2].split('_')
            filter_conditions.append(
                text(f"datasheet -> '{json_key[0]}' -> '{json_key[1]}' -> 0 ->> '{value[0]}' IS NOT NULL")
            )

        if filter_text:
            filter_conditions.append(text(f'datasheet::text ILIKE \'%{filter_text}%\''))


        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

        result = query.all()         
        
        if not result:  # If the result is empty, return all datasheets
            result = session.query(Datasheets).all()   

       
        for datasheet in result:
            datasheet_ids = load_saved_datasheeet([datasheet.datasheet], filter_text)
            if not datasheet_ids:
                pass
            else:
                matching_datasheets = session.query(Datasheets).filter_by(id=datasheet.id)
                result = matching_datasheets

        return prepare_success_response(data=datasheet_schema.dump(result))
    except psycopg2.Error:
        return prepare_error_response('Failed to search.')


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
        print(len(result))
        for datasheet in result:
            if(request.args.get("validate") == 1):
                if (validate_marketplace(datasheet)):
                    results.append(datsheet)
        return prepare_success_response(message=json.dumps(results))
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
