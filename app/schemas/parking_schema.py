from app .extensions import ma 
from app .models .parking import Parking 


class ParkingSchema (ma .SQLAlchemySchema ):
    class Meta :
        model =Parking 

    id =ma .auto_field (dump_only =True )
    nome =ma .auto_field (required =True )
    endereco =ma .auto_field (required =True )
