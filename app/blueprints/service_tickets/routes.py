from .schemas import service_ticket_schema, service_tickets_schema, return_service_ticket_schema, edit_service_ticket_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_Ticket, Mechanic, db
from . import service_tickets_bp
from app.extensions import limiter
from app.extensions import cache
from app.utils.util import encode_token, token_required



#CREATE SERVICE TICKET

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = Service_Ticket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201


#RETRIEVE ALL SERVICE TICKETS

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(Service_Ticket)
    service_tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(service_tickets)


#RETRIEVE SPECIFIC SERVICE TICKET

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    
    if service_ticket:
        return service_ticket_schema.jsonify(service_ticket), 400
    return jsonify({"error": "Service ticket not found."}), 400


#ASSIGN MECHANIC TO TICKET


@service_tickets_bp.route('/<int:service_ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic_to_ticket(service_ticket_id, mechanic_id):
    # Fetch the service ticket
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    # Fetch the mechanic
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    # Check if already assigned
    if mechanic in service_ticket.mechanics:
        return jsonify({"message": "Mechanic is already assigned to this service ticket."}), 200

    # Assign mechanic to ticket
    service_ticket.mechanics.append(mechanic)
    db.session.commit()

    return jsonify({"message": f"Mechanic {mechanic.name} assigned to ticket {service_ticket.id}."}), 200
 

#REMOVE MECHANIC FROM TICKET

@service_tickets_bp.route('/<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['DELETE'])
@token_required
def remove_mechanic_from_ticket(service_ticket_id, mechanic_id):
    # Fetch the service ticket
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    # Fetch the mechanic
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    # Check if the mechanic is assigned to the ticket
    if mechanic not in service_ticket.mechanics:
        return jsonify({"message": "Mechanic is not assigned to this service ticket."}), 400

    # Remove the mechanic
    service_ticket.mechanics.remove(mechanic)
    db.session.commit()

    return jsonify({"message": f"Mechanic {mechanic.name} removed from service ticket {service_ticket.id}."}), 200


#EDIT SERVICE TICKET

@service_tickets_bp.route("/<int:service_ticket_id>", methods=['PUT'])
def edit_service_ticket(service_ticket_id):
    try:
        service_ticket_edits = edit_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400


    query = select(Service_Ticket).where(Service_Ticket.id == service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()
    
    for mechanic_id in service_ticket_edits['add_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        
        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)
            
    for mechanic_id in service_ticket_edits['remove_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        
        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)    
    
    db.session.commit()
    return return_service_ticket_schema.jsonify(service_ticket)

