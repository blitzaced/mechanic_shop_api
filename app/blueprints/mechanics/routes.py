from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, delete 
from app.models import Mechanic, db
from . import mechanics_bp
from app.extensions import limiter
from app.extensions import cache
from app.utils.util import encode_token, token_required



#CREATE MECHANIC

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().all()
    if existing_mechanic: 
        return jsonify({"error": "Email already associated with a mechanic."}), 400
    
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


#RETRIEVE ALL MECHANICS

@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics)


#RETRIEVE SPECIFIC MECHANIC

@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if mechanic:
        return mechanic_schema.jsonify(mechanic), 400
    return jsonify({"error": "Mechanic not found."}), 400


#UPDATE SPECIFIC MECHANIC

@mechanics_bp.route('/', methods=['PUT'])
@token_required
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 400
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200
 

#DELETE SPECIFIC MECHANIC

@mechanics_bp.route('/', methods=['DELETE'])
@token_required
def delete_mechanice(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 400
    
    db.session.delete(mechanic)
    db.session.commit()    
    return jsonify({"message":f'Mechanic id: {mechanic_id}, successfully deleted.'}), 200



#SORT MECHANICS BY TICKET ASSIGNMENTS

@mechanics_bp.route("/popular", methods=['GET'])
def popular_mechanics():
   query = select(Mechanic)
   mechanics = db.session.execute(query).scalars().all()
   
   
   mechanics.sort(key= lambda mechanic: len(mechanic.service_tickets), reverse=True)
   
   return mechanics_schema.jsonify(mechanics)


#MECHANICS QUERY PARAMETERS - BY NAME

@mechanics_bp.route("/search", methods=['GET'])
def search_mechanic():
    name = request.args.get("name")
    
    if not name:
        return jsonify({"error": "Missing 'name' parameter"}), 400  
    
    query = select(Mechanic).where(Mechanic.name.like(f"%{name}%"))
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics)