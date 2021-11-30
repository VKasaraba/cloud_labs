import os
from flask import Flask, request
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.inspection import inspect
import base64
import ast

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app)

class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class Supermarket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supermarket_name = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(90), nullable=False)

    def serialize(self):
        supermarket = Serializer.serialize(self)
        return supermarket

    def serialize(self):
        d = Serializer.serialize(self)
        return d

    def __str__(self):
        return f'Supermarket {self.id} {self.supermarket_name} on {self.address}'

    def __repr__(self):
        return self.__str__()

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supermarket_id = db.Column(db.Integer, nullable=False)
    section_name = db.Column(db.String(45), nullable=False)

    def serialize(self):
        supermarket = Supermarket.query.get(self.supermarket_id).serialize()
        section = Serializer.serialize(self)
        return {**section, **supermarket}

    def __str__(self):
        return f'Section {self.id} {self.section_name} corresponding to supermarket {self.supermarket_id}'

    def __repr__(self):
        return self.__str__()

class AdvertisementPanel(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, nullable=False)
    producer_name = db.Column(db.String(90), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    material_name = db.Column(db.String(90), nullable=False)

    def serialize(self):
        d = Serializer.serialize(self)
        return d

    def __str__(self):
        return f'Panel {self.id} of {self.producer_name} corresponding to section {self.section_id}'

    def __repr__(self):
        return self.__str__()

class Sensor(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    sensor_type = db.Column(db.String(90), nullable=False)
    report_time = db.Column(db.String(90), nullable=False)
    people_walked = db.Column(db.Integer, nullable=False)
    avg_time_near_panel = db.Column(db.Integer, nullable=False)

    def serialize(self):
        sensor = Serializer.serialize(self)
        return sensor

    def __str__(self):
        return f'Sensor {self.id}'

    def __repr__(self):
        return self.__str__()

@app.route('/panels', methods=['GET', 'POST'])
def panels():
    if request.method == 'GET':
        print('IN GET')
        data = AdvertisementPanel.query.all()
        print(json.dumps(AdvertisementPanel.serialize_list(data)))
        return json.dumps(AdvertisementPanel.serialize_list(data))
    elif request.method == 'POST':
        data = request.json
        print('IN POST, json data: ', data)
        session = db.session
        section_id = data.get('section_id')
        producer_name = data.get('producer_name')
        height = data.get('height')
        width = data.get('width')
        material_name = data.get('material_name')
        new_panel = AdvertisementPanel(section_id=section_id, producer_name=producer_name, height=height, width=width, material_name=material_name)
        session.add(new_panel)
        session.commit()
        return data

@app.route('/panels/<int:panel_id>', methods=['GET', 'DELETE', 'PUT'])
def get_panel(panel_id):
    panel = AdvertisementPanel.query.get(panel_id)
    print(request.method, panel.id)
    if request.method == 'GET':
        return json.dumps(panel.serialize())
    if request.method == 'DELETE':
        db.session.delete(panel)
        db.session.commit()
        return {}
    if request.method == 'PUT':
        data = request.json
        print('IN UPDATE, json data: ', data)
        session = db.session
        panel.section_id = data.get('section_id', panel.section_id)
        panel.producer_name = data.get('producer_name', panel.producer_name)
        panel.height = data.get('height', panel.height)
        panel.width = data.get('width', panel.width)
        panel.material_name = data.get('material_name', panel.material_name)
        session.commit()
        return data

@app.route('/section/<int:section_id>', methods=['GET'])
def get_section(section_id):
    section = Section.query.get(section_id)
    if request.method == 'GET':
        return json.dumps(section.serialize())

@app.route('/sensors', methods=['GET'])
def get_sensors():
    data = Sensor.query.all()
    if request.method == 'GET':
        return json.dumps(Sensor.serialize_list(data))

@app.route('/sensors/<int:sensor_id>', methods=['PUT'])
def put_to_sensor(sensor_id):
    sensor = Sensor.query.get(sensor_id)
    if request.method == 'PUT':
        data = request.json
        print('in put_to_sensor, data: ', data)
        print('id: ', sensor_id)
        if not data.get('apiKey') == 'iovds8we47y48qq3uvjfdi8su':
            return {}
        session = db.session
        sensor.report_time = data.get('report_time', sensor.report_time)
        sensor.people_walked = data.get('people_walked', sensor.people_walked)
        sensor.avg_time_near_panel = data.get('avg_time_near_panel', sensor.avg_time_near_panel)
        session.commit()
        return data

@app.route('/sensors', methods=['POST'])
def post_to_mqtt_sensor():
    sensor = Sensor()
    data_json = request.json
    data_encoded = data_json.get('message').get('data')
    data_bytes = base64.b64decode(data_encoded)
    data = ast.literal_eval(data_bytes.decode('utf-8'))
    session = db.session
    sensor_id = data.get('id')
    sensor = Sensor.query.get(sensor_id)
    sensor.report_time = data.get('report_time', sensor.report_time)
    sensor.people_walked = data.get('people_walked', sensor.people_walked)
    sensor.avg_time_near_panel = data.get('avg_time_near_panel', sensor.avg_time_near_panel)
    session.commit()
    return data

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

