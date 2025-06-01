from app.extensions import ma
from app.models import Service_Ticket

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket
        
service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)