# EclipseApi

Um antigo projeto que decidi subir e finalizar , é
uma simples api para um loja virtual Contendo:

- sistema de autenticação jwt e oAuth
- admin
- testes automatizados
- docs com swagger
- criação de objetos falsos automatizado
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
- Micro serviço de envio de email

## Tecnologias
| Tecnologia | Uso |
| ---------- | --- |
| Python | Backend principal |
| Django/DRF | Framework da API|
| Redis | Cache|
| MySQL | Banco de dados |
| Nginx | Servidor de arquivos estaticos |
| Docker | Deploy e ambiente isolado|
| Git/GitHub | Versionamento e colaboração|
| kafka | sistema de comunicação de serviços |
| kafka-ui | gerenciamento e monitoramento do kafka |

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
| Variável | Serve para |
| -------- | ----- |
|SECRET_KEY| Chave usada para criptografia |
|DEBUG | modo de depuração|
|DATABASE_NAME | nome da tabela no DB|
|DATABASE_HOST | host do DB|
|DATABASE_PASSWORD | senha para acessar o DB|
|DATABASE_USER |usuario do DB|
|DATABASE_PORT | porta do DB|
|REDIS_URL |url para o redis |
|REDIS_PASSWORD | senha para o redis |
|REDIS_USE_PASSWORD | diz se é necessario usar senha no redis|

### Rodar migrações
```bash
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

### Fake Objects
por padrão não vem nenhum objeto (produto , duvida , avaliação e etc) para ser usado , é necessario cadastrar manualmente
mas para criar objetos de forma automatizada ha um modulo chamada fake_objects, basta rodar:
```bash
python ./fake_objects/<tipo_de_objeto>.py/
```
o "tipo_de_objeto" pode-se ser <b>Products</b> ou <b>Users</b> , sendo que <b>Product</b> gera os produtos , duvidas e avaliações mas é necessario ter o admin no banco junto as migrações
e <b>Users</b> ainda não foi implementado

## Como Contribuir:
Ha um arquivo apenas para ajudar nisso: [Contribuir](./CONTRIBUTING.md)

## Documentação
### Endpoints:
```bash
http://localhost:8000/docs/
```

\ [services](./docs/services.md) : documentação dos services
