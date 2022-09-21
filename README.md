# Document Engine
*Esse projeto foi desenvolvido com a finalidade de termos um motor de documento, removendo essa função que antes era responsabilidade do Carteiras.*

## Variáveis de Ambiente
Para configurar as ENVS bastar ir na raiz do projeto e criar um arquivo nomeado de `.env`. Em seguida, vá no arquivo `.env.example` pegue as variáveis e preencha.

Irei citar algumas variáveis que talvez você possa ter dificuldade em saber qual valor colocar:
```
BROKER_URL=amqp://guest:guest@document-engine-rabbitmq:5672//
FLOWER_PORT=5555
FLOWER_BASIC_AUTH=resale:rsl123
CORS_ORIGINS_AllOWED=http://localhost:2080 # Exemplo de URL (No meu caso essa URL é do Carteiras via local).
```

## Como rodar o projeto
Basicamente existem duas formas de rodar o projeto, visando a dificuldade que possuímos com a importação e a exportação no uso do Celery, foi pensado uma alternativa para que pudessemos debugar o código.

### 1 - FastAPI - *(Recomendado para Desenvolvedores)*
Rodando o projeto via FastAPI você terá a possibilidade de colocar breakpoints pelo código enquanto está rodando. Esta forma não faz uso do Docker, você estará rodando diretamente pelo [uvicorn](https://www.uvicorn.org/).

Primeiramente, Configure seu **launch.json** do vscode com o seguinte JSON:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Arquivo Atual",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "${fileDirname}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

Após launch configurado, basta procurar pelo arquivo `main.py` que se encontra na pasta **/app** e pressionar o **RUN** do launch.json

#### Se você conferir no final do arquivo **main.py** temos esse trecho de código:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost",
                port=8004, debug=True, reload=True)
```

Ou seja, nosso projeto estará rodando na **porta 8004**, com o **host** sendo **localhost**, o **debug** estará <span style="color: green;">ativo</span>. e o **reload=True** significa que qualquer mudança que ocorrer no código a API irá identificar e fazer um "reload", em outras palavras, você não vai precisar ficar desligando e ligando a API para que suas mudanças sejam efetivadas.

Outro detalhe, nesse mesmo arquivo do `main.py` é a inclusão da rota somente para **STAGE local**.
```python
# Router somente para desenvolvimento local, por aqui usamos somente FAST-API - conseguimos debugar.
if (os.environ.get("STAGE")).upper() == "LOCAL":
    app.include_router(developer.router, prefix='/local', tags=['Developer'])
```

### 2 - Celery
Rodando o projeto via Celery, iremos fazer o uso do Docker. A recomendação do uso do celery serão para casos que tivermos problemas com as Tasks.

Para rodar via **[docker](https://docs.docker.com/engine/install/ubuntu/)** é interessante que você o tenha instalado, assim como o docker-compose também.

É bastante simples, basta procurar pelo arquivo docker-compose que está localizado na raiz do projeto, clicar com o botão direito e dar um compose UP.

**OBS.:** Também é possível por linha de comando, caso prefira.

<img src="https://user-images.githubusercontent.com/92036660/191129954-944f0660-401a-447f-aeb7-0f874354c8b0.png" width="300" height="600" />

## ATENÇÃO
Um ponto a se prestar atenção é que a porta em que o Docker está configurada é diferente da que se você for rodar localmente pelo FastAPI, então caso vá alternar entre os dois preste atenção nesse detalhe, pode economizar um bom tempo tentando achar onde está o problema 😂
