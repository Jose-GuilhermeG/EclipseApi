# EclipseApi

Um antigo projeto que decidi subir e finalizar , é 
uma simples api para um loja virtual Contendo:

- sistema de autenticação jwt e oAuth
- admin
- testes automatizados
- docs com swagger
- otimização com :
    - rate limiting
    - cache com redis
    - consultas otimizadas
    - paginação eficiente
    - separação de camadas permitindo escalabilidade vertical e horizontal
- CRUD dos modelos :
    - Product
    - Category
    - Evaluations
    - Doubt
    - User
    - Purchased
    - e modelos intermediarios e secundarios

## Tecnologias
| Tecnologia | Uso |
| ---------- | --- |
| Python | Backend principal |
| Django/DRF | Framework da API|
| Redis | Cache|
| MySQL | Banco de dados|
| Docker | Deploy e ambiente isolado|
| Git/GitHub | Versionamento e colaboração|

## Como usar:
### Clonar o repositório
```bash
git clone https://github.com/Jose-GuilhermeG/EclipseApi
cd eclipseapi
```

### Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Configurar variáveis de ambiente
```bash
cp .env-example .env
```
### edite o arquivo .env com suas credenciais

### Rodar migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### Iniciar servidor
```bash
python manage.py runserver
```

### Ou se usar docker
```bash
docker-compose up --build
```

### Documentação
```bash
http://localhost:8000/docs/
```

### Testes
```bash
python manage.py test
```

### Admin
por padrão ja vem um user admin nas fixture basta dar um :
```bash
python manage.py loaddata users.json
```
entrar na url "/admin" e colocar o email : 
admin@exemple.com
e a senha : admin