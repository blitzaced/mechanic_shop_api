from app.extensions import ma
from app.models import Service_Ticket
import re
from marshmallow import fields

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested("MechanicSchema", many=True)
    customers = fields.Nested("CustonerScehma")
    class Meta:
        model = Service_Ticket
        include_fk = True
        fields = ("id", "VIN", "service_date", "service_desc", "customer_id")
        
class EditService_TicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(),required=True)
    remove_mechanic_ids = fields.List(fields.Int(),required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")
        
service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)
return_service_ticket_schema = Service_TicketSchema(exclude=["customer_id"])
edit_service_ticket_schema = EditService_TicketSchema()