from app.extensions import ma
from app.models import Part

class PartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Part
        
part_schema = PartSchema()
parts_schema = PartSchema(many=True)