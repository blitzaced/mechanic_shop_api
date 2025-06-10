from .schemas import service_ticket_schema, service_tickets_schema, return_service_ticket_schema, edit_service_ticket_schema
from ..mechanics.schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_Ticket, Mechanic, Part, db
from . import service_tickets_bp
from app.extensions import limiter
from app.extensions import cache
from app.utils.auth import encode_token, token_required



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



#EDIT SERVICE TICKET

#Add Mechanic from Ticket
@service_tickets_bp.route("/<int:ticket_id>/add-mechanic/<int:mechanic_id>", methods=['PUT'])
def add_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_Ticket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if ticket and mechanic:
        if mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
            db.session.commit()
            return jsonify({
                "message": f"successfully added {mechanic.name} to the ticket",
                "ticket": service_ticket_schema.dump(ticket),
                "mechanics": mechanics_schema.dump(ticket.mechanics)                
            }), 200
        return jsonify({"error": f"{mechanic.name} already assigned to ticket."}), 400
    return jsonify({'error': "Invalid ticket_id or mechanic_id."}), 400


#Remove Mechanic from Ticket
@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_Ticket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if ticket and mechanic:
        if mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
            db.session.commit()
            return jsonify({
                "message": f"Successfully removed {mechanic.name} from the ticket",
                "ticket": service_ticket_schema.dump(ticket),
                "mechanics": mechanics_schema.dump(ticket.mechanics)
            }), 200
        return jsonify({"error": f"{mechanic.name} was not assigned to this ticket."}), 400
    return jsonify({'error': "Invalid ticket_id or mechanic_id."}), 400


#----------------------------------------First attempt------------------------------------------------------------------------
#@service_tickets_bp.route("/<int:service_ticket_id>", methods=['PUT'])
#def edit_service_ticket(service_ticket_id):
#    try:
#        service_ticket_edits = edit_service_ticket_schema.load(request.json)
#    except ValidationError as e:
#        return jsonify(e.messages), 400


#    query = select(Service_Ticket).where(Service_Ticket.id == service_ticket_id)
#    service_ticket = db.session.execute(query).scalars().first()
    
#    for mechanic_id in service_ticket_edits['add_mechanic_ids']:
#        query = select(Mechanic).where(Mechanic.id == mechanic_id)
#        mechanic = db.session.execute(query).scalars().first()
        
#        if mechanic and mechanic not in service_ticket.mechanics:
#            service_ticket.mechanics.append(mechanic)
            
#    for mechanic_id in service_ticket_edits['remove_mechanic_ids']:
#        query = select(Mechanic).where(Mechanic.id == mechanic_id)
#        mechanic = db.session.execute(query).scalars().first()
        
#        if mechanic and mechanic in service_ticket.mechanics:
#            service_ticket.mechanics.remove(mechanic)    
    
#    db.session.commit()
#    return return_service_ticket_schema.jsonify(service_ticket)



#ADD PART TO TICKET

@service_tickets_bp.route('/<int:service_ticket_id>/add-part/<int:part_id>', methods=['PUT'])
def add_part_to_ticket(service_ticket_id, part_id):
    # Fetch the service ticket
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    # Fetch the part
    part = db.session.get(Part, part_id)
    if not part:
        return jsonify({"error": "Part not found."}), 404

    # Check if already added
    if part in service_ticket.parts:
        return jsonify({"message": "This part has already been added to this service ticket."}), 400

    # Add part to ticket
    service_ticket.parts.append(part)
    db.session.commit()

    return jsonify({"message": f"Part {part.name} added to ticket {service_ticket.id}."}), 200