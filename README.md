# api-document-generator

API desenvolvida com FastAPI, MYSQL e Docker.

## Instalação

- Primeiro passo é ter instalado o [Docker](https://www.docker.com/). Com ele iremos iniciar a aplicação e base de 
dados do projeto.
- criar virtualenv na versão 3.6.9 do python e ativar `source venv/bin/activate`
- instalar libs que estão no requirements.txt `pip install -r requirements.txt`
  
## Como usar

```
# Adicione as configurações abaixo no docker-compose.yml
  app:
    environment:
      ACCESS_KEY: "Sua access key na AWS para acesso a S3 Bucket"
      SECRET_KEY: "Sua secret key na AWS para acesso a S3 Bucket"

# Utilize o comando abaixo para iniciar o projeto.
docker-compose up -d --build --force-recreate

# Após iniciar o projeto estará disponível na URL abaixo.
http://localhost:8000/

# Para iniciar um consumidor acesse o container da aplicação e execute o comando abaixo.
docker exec -it app bash

celery -A app.api.document.tasks worker -l info -Q proposal-document-queue -c 1
celery -A app.api.document.tasks worker -l info -Q real-estate-document-queue -c 1
```

## Documentação

Para ter acesso a documentação, basta utilizar o endereço abaixo, após ter iniciado os passos anteriores.

```
http://localhost:8002/docs/
```

## Utilitários

Para ter acesso a admin do MySQL, utilize o endereço abaixo.

```
http://127.0.0.1:8080/

usuário: root
senha: password
```

Para ter acesso a admin do RabbitMQ, utilize o endereço abaixo.

```
http://127.0.0.1:15672/

usuário: guest
senha: guest
```

## Para testar os testes unitários

```
PYTHONPATH=/home/lucastribioli/Documentos/project/python/pagimovel-import-api python -m pytest

```
### Arquivo para executar os testes no VSCODE

Adicione esse arquivo no arquivo launch.json

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "${workspaceFolder}/app",
            "env": {
               "PYTHONPATH":"${workspaceFolder}" 
            }
        }
    ]
}
```