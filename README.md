# Sistema de Controle de Vagas de Estacionamento
Alunos: Allyfh Pontes, Douglas Pierry e Willemberg Lopes

API REST para gerenciar estacionamentos e suas vagas.

## 🚀 Quick Start

### Instalação

```bash
git clone https://github.com/seu-usuario/apirest.git
cd apirest
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask run
```

A API roda em `http://localhost:5000`

## 📍 Endpoints

| Método | Rota | Autenticação | Descrição |
|--------|------|--------------|-----------|
| GET | `/spots/` | Pública | Listar todas as vagas |
| POST | `/spots/` | JWT | Criar nova vaga |
| PATCH | `/spots/<id>` | JWT | Atualizar status da vaga |
| GET | `/parkings/` | Pública | Listar estacionamentos |
| POST | `/parkings/` | JWT | Criar estacionamento |
| GET | `/parkings/<id>/spots` | Pública | Listar vagas de um estacionamento |
| GET | `/users/` | Pública | Listar usuários |
| POST | `/users/` | Pública | Cadastrar usuário |
| PATCH | `/users/<id>` | JWT | Atualizar usuário |
| DELETE | `/users/<id>` | JWT | Remover usuário |
| GET | `/users/<id>/messages` | Pública | Listar mensagens do usuário |
| GET | `/messages/` | Pública | Listar mensagens |
| POST | `/messages/` | JWT | Criar mensagem |
| POST | `/login` | Pública | Autenticar e obter token JWT |

## 🔐 Autenticação

Cadastre um usuário em `POST /users/` (rota pública, é o cadastro) e faça login para obter o token:

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@exemplo.com","senha":"123456"}'
```

A resposta traz `data.access_token`. Rotas de escrita (POST/PATCH/DELETE), exceto o cadastro de usuário, exigem o header:

```
Authorization: Bearer <access_token>
```

### Exemplos

**Listar vagas:**
```bash
curl http://localhost:5000/spots/
```

**Criar vaga:**
```bash
curl -X POST http://localhost:5000/spots/ \
  -H "Content-Type: application/json" \
  -d '{"codigo":"A01","ocupada":false,"parking_id":1}'
```

**Atualizar vaga:**
```bash
curl -X PATCH http://localhost:5000/spots/1 \
  -H "Content-Type: application/json" \
  -d '{"ocupada":true}'
```

## 🗄️ Modelo ParkingSpot

```
id (int)          - ID único
codigo (string)   - Código da vaga (ex: A01)
ocupada (bool)    - Status de ocupação
parking_id (int)  - ID do estacionamento
```

## 🛠️ Tecnologias

- Flask
- SQLAlchemy
- Marshmallow
- Alembic
- Flask-JWT-Extended

## 📄 Licença

MIT
