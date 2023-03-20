import os
import psycopg2
import sqlalchemy
from sqlalchemy import or_ , String, and_
from sqlalchemy import update, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_utils import database_exists, create_database

from dataclasses import dataclass
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)
cors = CORS(app)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'
Base = declarative_base()


def prepare_error_response(message):
    return {'status_code': 500, 'message': message}


def prepare_success_response(message=None, data=None):
    return {'status_code': 200, 'message': message, 'data': data}


def create_database_connection():
    db_user = os.getenv("POSTGRES_DB_USER")
    db_pass =  os.getenv("POSTGRES_DB_PASS")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB_NAME")
    db_use_ssl = os.getenv("POSTGRES_USE_SSL")

    # engine = sqlalchemy.create_engine(
    #     "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    #         db_user,
    #         db_pass,
    #         db_host,
    #         db_port,
    #         db_name
    #     )
    # )

    POSTGRESQL_USER='postgres'
    POSTGRESQL_PASSWORD='postgres'
    POSTGRESQL_DATABASE='kitt4sme-digital-datasheet-database'
    POSTGRESQL_HOST='localhost'
    POSTGRESQL_PORT=5432
    engine = sqlalchemy.create_engine(
        "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            'posgres',
            'posgres',
            'localhost',
            5432,
            'kitt4sme-digital-datasheet-database'
        )
    )
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine)
    session = sqlalchemy.orm.sessionmaker()
    session.configure(bind=engine)
    session = session()
    return session


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

        print(query)
        result = query.all()
        print(result)

        return prepare_success_response(data=datasheet_schema.dump(result))
    except psycopg2.Error:
        return prepare_error_response('Failed to search.')

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
        host='0.0.0.0'
    )
