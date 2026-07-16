from flask import Flask
from marshmallow import ValidationError
from werkzeug .exceptions import NotFound

from .config import Config
from .extensions import db ,jwt ,ma ,migrate
from .routes .auth import auth_bp
from .routes .messages import messages_bp
from .routes .parkings import parkings_bp
from .routes .spots import spots_bp
from .routes .users import users_bp


def create_app ():
    app =Flask (__name__ )

    app .config .from_object (Config )

    db .init_app (app )
    migrate .init_app (app ,db )
    ma .init_app (app )
    jwt .init_app (app )

    from .models import message ,parking ,parking_spot ,user

    app .register_blueprint (auth_bp )
    app .register_blueprint (messages_bp ,url_prefix ="/messages")
    app .register_blueprint (users_bp ,url_prefix ="/users")
    app .register_blueprint (parkings_bp ,url_prefix ="/parkings")
    app .register_blueprint (spots_bp ,url_prefix ="/spots")

    @app .errorhandler (ValidationError )
    def handle_validation_error (err ):
        return {"success":False ,"errors":err .messages },400

    @app .errorhandler (NotFound )
    def handle_not_found (err ):
        return {"success":False ,"message":"Recurso nao encontrado"},404

    @app .errorhandler (404 )
    def handle_404 (err ):
        return {"success":False ,"message":"Rota nao encontrada"},404

    @jwt .unauthorized_loader
    def handle_missing_token (reason ):
        return {"success":False ,"message":"Token de acesso ausente"},401

    @jwt .invalid_token_loader
    def handle_invalid_token (reason ):
        return {"success":False ,"message":"Token invalido"},401

    @jwt .expired_token_loader
    def handle_expired_token (jwt_header ,jwt_payload ):
        return {"success":False ,"message":"Token expirado"},401

    return app
