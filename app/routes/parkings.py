from flask import Blueprint ,jsonify ,request 

from app .controllers .parking_controller import criar_estacionamento ,listar_estacionamentos 
from app .controllers .parking_spot_controller import listar_vagas_por_estacionamento 


parkings_bp =Blueprint ("parkings",__name__ )


@parkings_bp .route ("/",methods =["GET"])
def get_parkings ():
    response ,status =listar_estacionamentos ()
    return jsonify (response ),status 


@parkings_bp .route ("/",methods =["POST"])
def post_parking ():
    data =request .get_json ()
    response ,status =criar_estacionamento (data )
    return jsonify (response ),status 


@parkings_bp .route ("/<int:parking_id>/spots",methods =["GET"])
def get_parking_spots (parking_id ):
    response ,status =listar_vagas_por_estacionamento (parking_id )
    return jsonify (response ),status 
