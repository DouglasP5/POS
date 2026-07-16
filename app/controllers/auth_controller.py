from flask_jwt_extended import create_access_token

from app.models.user import User
from app.utils.response import error_response, success_response


def login(data):
    email = data.get("email") if data else None
    senha = data.get("senha") if data else None

    if not email or not senha:
        return error_response("Email e senha sao obrigatorios", 400)

    usuario = User.query.filter_by(email=email).first()

    if not usuario or not usuario.check_senha(senha):
        return error_response("Email ou senha invalidos", 401)

    access_token = create_access_token(identity=str(usuario.id))

    return success_response({"access_token": access_token})
