# Apresentação — Autenticação JWT na API de Vagas de Estacionamento

Guia de apoio para a simulação de entrega da 2ª Unidade: explica o que foi feito, por quê, e como demonstrar cada ponto pedido pelo professor.

## 1. O que já existia vs. o que foi adicionado

O projeto já usava **Flask-SQLAlchemy** (ORM) com Blueprints, Controllers e Schemas Marshmallow — isso não mudou. O que foi adicionado nesta refatoração:

| Item | Arquivo | O que faz |
|---|---|---|
| Hash de senha | `app/models/user.py` | `set_senha()` / `check_senha()` usando `werkzeug.security` |
| Senha hasheada nos controllers | `app/controllers/user_controller.py` | `criar_usuario`/`atualizar_usuario` chamam `set_senha()` em vez de gravar texto puro |
| Rota de login | `app/controllers/auth_controller.py` + `app/routes/auth.py` | `POST /login` valida email+senha e devolve um JWT |
| Configuração do JWT | `app/extensions.py` + `app/config.py` | Instância do `JWTManager`, chave secreta e expiração do token (1h) |
| Proteção das rotas | `app/routes/*.py` | `@jwt_required()` nas rotas de escrita |
| Respostas de erro do JWT | `app/__init__.py` | Token ausente/inválido/expirado → `401` no mesmo formato do resto da API |

## 2. Como o fluxo funciona (para explicar ao professor)

```
1. Cliente cadastra um usuário  -->  POST /users/                (rota pública)
2. Cliente faz login            -->  POST /login                 (rota pública)
                                      recebe { "access_token": "..." }
3. Cliente acessa um recurso    -->  GET /spots/                  (rota pública, sem header)
4. Cliente tenta escrever       -->  POST /spots/  (sem header)   -->  401 "Token de acesso ausente"
5. Cliente escreve com token    -->  POST /spots/
                                      Header: Authorization: Bearer <access_token>
                                      -->  201 Created
```

A senha nunca é devolvida em nenhuma resposta (campo `load_only=True` no schema + hash irreversível no banco).

## 3. Mapeamento direto com os critérios de avaliação

| Critério | Pontos | Onde está / como comprovar |
|---|---|---|
| Recursos modelados com ORM | 10 | `app/models/*.py` — `User`, `Message`, `Parking`, `ParkingSpot` são classes `db.Model` (Flask-SQLAlchemy). Já existia antes da refatoração. |
| Modelo de usuário integrado ao ORM | 10 | `app/models/user.py` — `User(db.Model)` com `set_senha`/`check_senha` como comportamento do próprio model, não só colunas. |
| Rota para criar usuário | 10 | `POST /users/` em `app/routes/users.py` → `criar_usuario()` em `app/controllers/user_controller.py`. |
| Senha armazenada de forma criptografada | 10 | `generate_password_hash()` (Werkzeug/PBKDF2) em `User.set_senha()`, chamado na criação **e** na atualização de usuário. Mostrar no banco (`instance/app.db`) que o campo `senha` nunca é texto puro. |
| Rota `/login` retorna JWT | 20 | `POST /login` em `app/routes/auth.py` → `login()` em `app/controllers/auth_controller.py` → `create_access_token()` do Flask-JWT-Extended. |
| Rotas protegidas conforme JWT | 20 | `@jwt_required()` em: `PATCH`/`DELETE /users/<id>`, `POST /messages/`, `POST /parkings/`, `POST`/`PATCH /spots/`. GETs continuam livres. |
| Simulação Postman (login + GET público + POST protegido) | 20 | Roteiro pronto na seção 4 abaixo. |

**Total coberto: 100 pontos.**

## 4. Roteiro de demonstração ao vivo (Postman ou curl)

Suba o servidor antes de chamar o professor:
```bash
source .venv/Scripts/activate   # ou .venv\Scripts\activate no cmd/PowerShell
flask db upgrade
flask run
```

**Passo 1 — Cadastrar um usuário (rota pública):**
```
POST http://localhost:5000/users/
Content-Type: application/json

{"nome": "Usuario Demo", "email": "demo@exemplo.com", "senha": "123456"}
```
→ `201`. Mostre que a resposta **não** tem o campo `senha`.

**Passo 2 — Login:**
```
POST http://localhost:5000/login
Content-Type: application/json

{"email": "demo@exemplo.com", "senha": "123456"}
```
→ `200` com `data.access_token`. Copie o token (no Postman, salve como variável).

**Passo 3 — GET público (sem header nenhum):**
```
GET http://localhost:5000/spots/
```
→ `200`. Mostra que a leitura é livre para qualquer um.

**Passo 4 — POST protegido SEM token (deve falhar):**
```
POST http://localhost:5000/parkings/
Content-Type: application/json

{"nome": "Estacionamento Centro", "endereco": "Rua Principal, 100"}
```
→ `401` `{"success": false, "message": "Token de acesso ausente"}`.

**Passo 5 — POST protegido COM token (deve funcionar):**
```
POST http://localhost:5000/parkings/
Content-Type: application/json
Authorization: Bearer <access_token do passo 2>

{"nome": "Estacionamento Centro", "endereco": "Rua Principal, 100"}
```
→ `201`. Anote o `id` retornado.

**Passo 6 (opcional, "efeito bônus") — criar uma vaga usando o `parking_id` do passo 5, e depois repetir com o token adulterado (um caractere a mais) para mostrar o `401 "Token invalido"`.**

> Atenção: se reaproveitar um usuário criado **antes** desta refatoração, o login vai falhar (senha antiga estava em texto puro). Cadastre sempre um usuário novo para a demo.

## 5. Perguntas que o professor pode fazer (e respostas prontas)

**"Por que `POST /users/` (criar usuário) não está protegido, se é uma rota de escrita?"**
> É a rota de cadastro/registro. Um usuário novo ainda não tem token — exigir JWT aqui criaria um problema de "ovo e galinha" (não dá para logar sem existir, e não dá para se cadastrar sem token). É o mesmo padrão usado em qualquer API com login: cadastro e login são as duas portas públicas de entrada, tudo depois delas é protegido.

**"Por que usaram `werkzeug.security` e não `bcrypt`?"**
> O Werkzeug já é dependência do próprio Flask — zero bibliotecas novas para instalar. `generate_password_hash`/`check_password_hash` usam um algoritmo seguro (scrypt/PBKDF2 conforme a versão) com salt automático, o suficiente para o que a atividade pede.

**"Onde fica a lógica de verificar a senha?"**
> Dentro do próprio model `User` (`set_senha`/`check_senha`), não duplicada nos controllers. Tanto o cadastro/atualização de usuário quanto o login chamam esses dois métodos — um único lugar de verdade para hash e verificação.

**"O que acontece se o token expirar ou for inválido?"**
> `app/__init__.py` registra três handlers do Flask-JWT-Extended (`unauthorized_loader`, `invalid_token_loader`, `expired_token_loader`) que devolvem `401` no mesmo formato `{"success": false, "message": ...}` usado no resto da API — token ausente, token malformado/adulterado e token expirado geram mensagens diferentes.

**"Por que as rotas GET continuam sem proteção?"**
> A atividade pede exatamente isso: leitura pública, escrita (criar/editar/apagar) protegida. Faz sentido também do ponto de vista de produto — qualquer um pode consultar vagas disponíveis, só quem está autenticado pode alterar dados.

## 6. Comandos de preparação do ambiente (para o clone/simulação)

```bash
git clone <repo>
cd POS
python -m venv .venv
source .venv/Scripts/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask db upgrade
flask run
```
A API sobe em `http://localhost:5000`.
