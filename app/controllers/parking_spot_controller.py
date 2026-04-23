from app .extensions import db 
from app .models .parking import Parking 
from app .models .parking_spot import ParkingSpot 
from app .schemas .parking_spot_schema import ParkingSpotSchema 
from app .utils .response import error_response ,success_response 


parking_spot_schema =ParkingSpotSchema ()
parking_spots_schema =ParkingSpotSchema (many =True )


def listar_vagas ():
    vagas =ParkingSpot .query .all ()
    return success_response (parking_spots_schema .dump (vagas ))


def listar_vagas_por_estacionamento (parking_id ):
    estacionamento =Parking .query .get_or_404 (parking_id )
    vagas =estacionamento .spots 
    return success_response (parking_spots_schema .dump (vagas ))


def criar_vaga (data ):
    dados_validados =parking_spot_schema .load (data )

    Parking .query .get_or_404 (dados_validados ["parking_id"])

    nova_vaga =ParkingSpot (**dados_validados )

    db .session .add (nova_vaga )
    db .session .commit ()

    return success_response (parking_spot_schema .dump (nova_vaga ),201 )


def atualizar_status_vaga (id ,data ):
    vaga =ParkingSpot .query .get_or_404 (id )

    dados_validados =parking_spot_schema .load (data ,partial =True )
    if any (chave !="ocupada"for chave in dados_validados ):
        return error_response ("Apenas o campo 'ocupada' pode ser atualizado",400 )

    for campo ,valor in dados_validados .items ():
        setattr (vaga ,campo ,valor )

    db .session .commit ()

    return success_response (parking_spot_schema .dump (vaga ))
