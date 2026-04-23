from app .extensions import db 


class ParkingSpot (db .Model ):
    __tablename__ ="parking_spots"

    id =db .Column (db .Integer ,primary_key =True )
    codigo =db .Column (db .String (50 ),nullable =False )
    ocupada =db .Column (db .Boolean ,nullable =False ,default =False )
    parking_id =db .Column (db .Integer ,db .ForeignKey ("parkings.id"),nullable =False )
