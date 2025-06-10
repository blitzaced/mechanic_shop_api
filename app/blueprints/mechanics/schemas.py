from app.extensions import ma
from app.models import Mechanic
from marshmallow import fields

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    service_tickets = fields.Nested("Service_TicketSchema", many=True, exclude=("mechanics",))
    
    class Meta:
        model = Mechanic
        
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)