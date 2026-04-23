from app .extensions import db 


class Parking (db .Model ):
    __tablename__ ="parkings"

    id =db .Column (db .Integer ,primary_key =True )
    nome =db .Column (db .String (120 ),nullable =False )
    endereco =db .Column (db .String (255 ),nullable =False )

    spots =db .relationship (
    "ParkingSpot",
    backref ="parking",
    lazy =True ,
    cascade ="all, delete-orphan",
    )
