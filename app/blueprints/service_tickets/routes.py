from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_Ticket, Mechanic, db
from . import service_tickets_bp



#CREATE SERVICE TICKET

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    
    try:
        service_ticket_data = service_tickets_schema.load(request.json)
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
    mechanics = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(mechanics)


#RETRIEVE SPECIFIC SERVICE TICKET

@service_tickets_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if mechanic:
        return mechanic_schema.jsonify(mechanic), 400
    return jsonify({"error": "Mechanic not found."}), 400


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
 

##REMOVE MECHANIC FROM TICKET

@service_tickets_bp.route('/<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['DELETE'])
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
