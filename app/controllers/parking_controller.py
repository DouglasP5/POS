from app .extensions import db 
from app .models .parking import Parking 
from app .schemas .parking_schema import ParkingSchema 
from app .utils .response import success_response 


parking_schema =ParkingSchema ()
parkings_schema =ParkingSchema (many =True )


def listar_estacionamentos ():
    estacionamentos =Parking .query .all ()
    return success_response (parkings_schema .dump (estacionamentos ))


def criar_estacionamento (data ):
    dados_validados =parking_schema .load (data )

    novo_estacionamento =Parking (**dados_validados )

    db .session .add (novo_estacionamento )
    db .session .commit ()

    return success_response (parking_schema .dump (novo_estacionamento ),201 )
