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
| POST | `/login` | Pública | Autenticar e obter token JWT |
| GET | `/users/` | Pública | Listar usuários |
| POST | `/users/` | Pública | Cadastrar usuário |
| PATCH | `/users/<id>` | JWT | Atualizar usuário |
| DELETE | `/users/<id>` | JWT | Remover usuário |
| GET | `/users/<id>/messages` | Pública | Listar mensagens do usuário |
| GET | `/messages/` | Pública | Listar mensagens |
| POST | `/messages/` | JWT | Criar mensagem |
| GET | `/parkings/` | Pública | Listar estacionamentos |
| POST | `/parkings/` | JWT | Criar estacionamento |
| GET | `/parkings/<id>/spots` | Pública | Listar vagas de um estacionamento |
| GET | `/spots/` | Pública | Listar todas as vagas |
| POST | `/spots/` | JWT | Criar nova vaga |
| PATCH | `/spots/<id>` | JWT | Atualizar status da vaga |

## 📮 Configurando o Postman

1. Crie uma **Collection** (ex: `POS API`) e um **Environment** (ex: `Local`) com a variável:
   - `base_url` = `http://localhost:5000`
2. Em todas as requisições abaixo, use `{{base_url}}` no lugar da URL fixa.
3. Na requisição de **Login**, abra a aba **Scripts → Post-response** (versões antigas: aba **Tests**) e cole:
   ```javascript
   const json = pm.response.json();
   pm.environment.set("token", json.data.access_token);
   ```
   Isso salva o token automaticamente numa variável de ambiente `token` a cada login.
4. Nas requisições marcadas como **Auth: Bearer Token**, vá na aba **Authorization** da requisição, escolha o tipo **Bearer Token** e informe `{{token}}`.
5. Toda requisição com corpo precisa do header `Content-Type: application/json` e do body no modo **raw / JSON**.

---

## 🔑 Autenticação

### Login
| Campo | Valor |
|---|---|
| Método | `POST` |
| URL | `{{base_url}}/login` |
| Auth | No Auth |
| Headers | `Content-Type: application/json` |

Body (raw, JSON):
```json
{
  "email": "demo@exemplo.com",
  "senha": "123456"
}
```

Resposta `200`:
```json
{
  "success": true,
  "data": {
    "access_token": "<jwt>"
  }
}
```

Resposta `401` (credenciais inválidas):
```json
{ "success": false, "message": "Email ou senha invalidos" }
```

---

## 👤 Usuários

### Listar usuários
| Campo | Valor |
|---|---|
| Método | `GET` |
| URL | `{{base_url}}/users/` |
| Auth | No Auth |

### Cadastrar usuário
| Campo | Valor |
|---|---|
| Método | `POST` |
| URL | `{{base_url}}/users/` |
| Auth | No Auth |
| Headers | `Content-Type: application/json` |

Body (raw, JSON):
```json
{
  "nome": "Demo",
  "email": "demo@exemplo.com",
  "senha": "123456",
  "admin": false
}
```
`nome` e `email` são obrigatórios, `email` precisa ser um e-mail válido, `senha` é obrigatória com mínimo de 6 caracteres, `admin` é opcional (bool, default `false`).

Resposta `201`:
```json
{
  "success": true,
  "data": { "id": 1, "nome": "Demo", "email": "demo@exemplo.com", "admin": false }
}
```

Resposta `400` (ex: senha curta):
```json
{ "success": false, "errors": { "senha": ["Shorter than minimum length 6."] } }
```

### Atualizar usuário
| Campo | Valor |
|---|---|
| Método | `PATCH` |
| URL | `{{base_url}}/users/<id>` (ex: `{{base_url}}/users/1`) |
| Auth | Bearer Token → `{{token}}` |
| Headers | `Content-Type: application/json` |

Body (raw, JSON) — todos os campos são opcionais, envie só o que quiser alterar:
```json
{
  "nome": "Novo Nome",
  "senha": "novaSenha123"
}
```

Resposta `200`: mesmo formato do cadastro, com os campos atualizados.

### Remover usuário
| Campo | Valor |
|---|---|
| Método | `DELETE` |
| URL | `{{base_url}}/users/<id>` |
| Auth | Bearer Token → `{{token}}` |

Resposta `204`: sem corpo.

### Listar mensagens de um usuário
| Campo | Valor |
|---|---|
| Método | `GET` |
| URL | `{{base_url}}/users/<user_id>/messages` |
| Auth | No Auth |

---

## 💬 Mensagens

### Listar mensagens
| Campo | Valor |
|---|---|
| Método | `GET` |
| URL | `{{base_url}}/messages/` |
| Auth | No Auth |

### Criar mensagem
| Campo | Valor |
|---|---|
| Método | `POST` |
| URL | `{{base_url}}/messages/` |
| Auth | Bearer Token → `{{token}}` |
| Headers | `Content-Type: application/json` |

Body (raw, JSON):
```json
{
  "content": "Mensagem de teste",
  "user_id": 1
}
```

Resposta `201`:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "content": "Mensagem de teste",
    "user_id": 1,
    "created_at": "2026-07-16T12:00:00",
    "user": { "id": 1, "nome": "Demo" }
  }
}
```

Resposta `404` (usuário inexistente):
```json
{ "success": false, "message": "Recurso nao encontrado" }
```

---

## 🅿️ Estacionamentos

### Listar estacionamentos
| Campo | Valor |
|---|---|
| Método | `GET` |
| URL | `{{base_url}}/parkings/` |
| Auth | No Auth |

### Criar estacionamento
| Campo | Valor |
|---|---|
| Método | `POST` |
| URL | `{{base_url}}/parkings/` |
| Auth | Bearer Token → `{{token}}` |
| Headers | `Content-Type: application/json` |

Body (raw, JSON):
```json
{
  "nome": "Estacionamento Central",
  "endereco": "Rua Principal, 100"
}
```

Resposta `201`:
```json
{
  "success": true,
  "data": { "id": 1, "nome": "Estacionamento Central", "endereco": "Rua Principal, 100" }
}
```

### Listar vagas de um estacionamento
| Campo | Valor |
|---|---|
| Método | `GET` |
| URL | `{{base_url}}/parkings/<parking_id>/spots` |
| Auth | No Auth |

---

## 🚗 Vagas

### Listar vagas
| Campo | Valor |
|---|---|
| Método | `GET` |
| URL | `{{base_url}}/spots/` |
| Auth | No Auth |

### Criar vaga
| Campo | Valor |
|---|---|
| Método | `POST` |
| URL | `{{base_url}}/spots/` |
| Auth | Bearer Token → `{{token}}` |
| Headers | `Content-Type: application/json` |

Body (raw, JSON):
```json
{
  "codigo": "A01",
  "ocupada": false,
  "parking_id": 1
}
```

Resposta `201`:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "codigo": "A01",
    "ocupada": false,
    "parking_id": 1,
    "parking": { "id": 1, "nome": "Estacionamento Central" }
  }
}
```

### Atualizar status da vaga
| Campo | Valor |
|---|---|
| Método | `PATCH` |
| URL | `{{base_url}}/spots/<id>` |
| Auth | Bearer Token → `{{token}}` |
| Headers | `Content-Type: application/json` |

Body (raw, JSON) — **somente** o campo `ocupada` pode ser enviado:
```json
{
  "ocupada": true
}
```

Resposta `400` (se enviar outro campo, ex: `codigo`):
```json
{ "success": false, "message": "Apenas o campo 'ocupada' pode ser atualizado" }
```

---

## 📦 Modelos de dados

```
User
  id (int, gerado)        nome (string)         email (string, único)
  senha (string, ≥6, write-only)                admin (bool, default false)

Message
  id (int, gerado)        content (string)      user_id (int, FK -> User)
  created_at (datetime, gerado)

Parking
  id (int, gerado)        nome (string)         endereco (string)

ParkingSpot
  id (int, gerado)        codigo (string)        ocupada (bool)
  parking_id (int, FK -> Parking)
```

## 🛠️ Tecnologias

- Flask
- SQLAlchemy
- Marshmallow
- Alembic
- Flask-JWT-Extended

## 📄 Licença

MIT
