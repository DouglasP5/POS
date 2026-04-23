from flask import Blueprint ,jsonify ,request 

from app .controllers .parking_spot_controller import (
criar_vaga ,
listar_vagas ,
atualizar_status_vaga ,
)


spots_bp =Blueprint ("spots",__name__ )


@spots_bp .route ("/",methods =["GET"])
def get_spots ():
    response ,status =listar_vagas ()
    return jsonify (response ),status 


@spots_bp .route ("/",methods =["POST"])
def post_spot ():
    data =request .get_json ()
    response ,status =criar_vaga (data )
    return jsonify (response ),status 


@spots_bp .route ("/<int:id>",methods =["PATCH"])
def patch_spot (id ):
    data =request .get_json ()
    response ,status =atualizar_status_vaga (id ,data )
    return jsonify (response ),status 
