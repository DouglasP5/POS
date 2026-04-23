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
python app.py
```

A API roda em `http://localhost:5000`

## 📍 Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/spots/` | Listar todas as vagas |
| POST | `/spots/` | Criar nova vaga |
| PATCH | `/spots/<id>` | Atualizar status da vaga |

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

## 📄 Licença

MIT
