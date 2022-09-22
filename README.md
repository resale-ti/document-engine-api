# Document Engine
*Esse projeto foi desenvolvido com a finalidade de termos um motor de documento, removendo essa função que antes era responsabilidade do Carteiras.*

## Pontos importantes para se prestar atenção!
### a) Funcionamento do código
- Apresentaremos duas formas de rodar o código, tanto pelo FastAPI como pelo Celery. É de sua **obrigação**, ao dar manutenção no código, garantir que esteja funcionando para as duas formas! Então lembre-se sempre de testar tanto pelo FastAPI como pelo Celery também.

-------------------------------------------------------
## 1. Variáveis de Ambiente
Para configurar as ENVS bastar ir na raiz do projeto e criar um arquivo nomeado de `.env`. Em seguida, vá no arquivo `.env.example` pegue as variáveis e preencha.

Irei citar algumas variáveis que talvez você possa ter dificuldade em saber qual valor colocar:
```
BROKER_URL=amqp://guest:guest@document-engine-rabbitmq:5672//
FLOWER_PORT=5555
FLOWER_BASIC_AUTH=resale:rsl123
CORS_ORIGINS_AllOWED=http://localhost:2080 # Exemplo de URL (No meu caso essa URL é do Carteiras via local).
```

## 2 - Como rodar o projeto
Basicamente existem duas formas de rodar o projeto, visando a dificuldade que possuímos com a importação e a exportação no uso do Celery, foi pensado uma alternativa para que pudessemos debugar o código.

### 2.1 - FastAPI - *(Recomendado para Desenvolvedores)*
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

### 2.2 - Celery
Rodando o projeto via Celery, iremos fazer o uso do Docker. A recomendação do uso do celery serão para casos que tivermos problemas com as Tasks.

Para rodar via **[docker](https://docs.docker.com/engine/install/ubuntu/)** é interessante que você o tenha instalado, assim como o docker-compose também.

É bastante simples, basta procurar pelo arquivo docker-compose que está localizado na raiz do projeto, clicar com o botão direito e dar um compose UP.

**OBS.:** Também é possível por linha de comando, caso prefira.

<img src="https://user-images.githubusercontent.com/92036660/191129954-944f0660-401a-447f-aeb7-0f874354c8b0.png" width="300" height="600" />

## 3 - Como adicionar um novo documento
Um breve resumo sobre a estruturação do código, a partir dos exemplos existentes ficará bem mais fácil de entender como fazer.

### 3.1 - Criando a rota
As rotas da aplicação se encontram no caminho `/app/api/routers`, nessa pasta encontraremos três routers principais.
#### a) `document.py`
- Esse router faz referência a quando estamos rodando pelo Celery, que é o nosso core da aplicação em DEV e PROD, por isso a importância citada no ponto `1. a) Funcionamento do código`

#### b) `developer.py`
- Esse router faz referência a quando estamos rodando pelo `FastAPI`, deve ser entendido somente como um auxiliar para debugarmos o código. Sempre mantenha seu foco no funcionamento rodando pelo `Celery`

#### c) `task_control.py`
- Esse router faz referência a quando estamos rodando pelo `Celery`e queremos ter o controle das nossas Tasks.

Para criar uma nova rota é muito simples, basta seguir o padrão existente:
**Obs.:** Palavras entre {} são variáveis demonstrativas, o valor real será o nome do seu contrato.
```python
@router.post("/{contract_type}", status_code=status.HTTP_200_OK)
async def generate_celery(payload: {ContractSchema} , response: Response) -> dict:
    try:
        task = TaskControlServices.send_task({
            'task_name': f'{contract_type}.generate_document',
            'task_state': 'PENDING',
            'task_request': payload
        })

        return {'task': task.task_id, 'message': 'Solicitação recebida com sucesso!'}

    except Exception as err:
        return response_rollbar_handler(err, response)
```

### 3.2 - Criando as Tasks
Após a criação da rota, vamos para o próximo passo que são as criações das Task. As tasks são caracterizadas pelo seu nome, seguindo o padrão `{contract_type}.generate_document`. Elas representam o que irá rodar no `Celery` quando o endpoint da sua Task for chamado.

Par criar uma nova Task é bastante simples, basta apenas seguir o padrão:
```python
@celery_app.task(
    name='{contract_type}.generate_document',
    base=CallbackTask,
)
def generate_document(task_request: dict) -> str:
    current_task.update_state(state='STARTED', meta={'current': 0, 'total': 1})
    contract_type = "{contract_type}"
    Contract.generate_contract(contract_type=contract_type, data=task_request)
```

No momento escrevo esse Readme ainda estamos vendo a possibilidade de criar um Task genérica, para evitar poluição de código. Porém, no caso do Regulamento não é possível, pois o mesmo tem particularidades. 

### 3.3 - Configurando Celery
Após criação das tasks, agora vamos para configuração do `Celery`. É bastante simples, basta apenas cadastrar dentro do `dict` o nome da sua task.

```python
celery_app.conf.task_routes = {
    'regulamento_concorrencia.generate_document': 'document-engine-queue',
    'regulamento_concorrencia_completo.generate_document': 'document-engine-queue',
    'certificado_venda.generate_document': 'document-engine-queue'
}
```

### 3.4 - Criação de um novo `Contract`
Hoje o esqueleto do contrato está todo pronto, a estrutura pode ser encontrada dentro do path `/app/api/contract/`.
Todos os elementos destacados compões a base do nosso `Contract`.
![image](https://user-images.githubusercontent.com/92036660/191807470-046d2694-30b1-480a-ad44-c9159f045693.png)

Para começar o desenvolvimento do novo `Contract`, primeiro crie uma pasta dentro de `/app/api/contract/` com o nome do seu `Contract`.

##### 3.4.1 - Contract
Dentro da Task que criamos, perceba que existe esse Trecho de código:
```python
Contract.generate_contract(contract_type=contract_type, data=task_request)
```
Ele é responsável por chamar o `Factory` dos `Contract` e através da variável `contract_type` retornar a `Classe Builder`
do nosso `Contract`.

```python
class ContractFactory:

    @staticmethod
    def get_instance(contract_type: str, data: dict):
        contract_builder_class = None

        if contract_type == EnumContractType.REGULAMENTO_CONCORRENCIA.value:
            contract_builder_class = RegulamentoConcorrenciaBuilder(data=data)

        return contract_builder_class
```

Para adicionar o seu contrato, primeiro vá no arquivo onde se encontra o `EnumContractType`, crie uma correspondência para seu `Contract` e adicionado uma opção de `elif` no código.

#### 3.4.2 - Builder
Já dentro da pasta criada anteriormente para o seu `Contract`, agora você irá começar a desenvolver o Builder do seu Contrato.

Crie a Classe herdando de ContractBuilderBase (Atua como uma classe abstrata para todos os contratos). Herdando essa classe você será obrigado a implementar o método `build()`.

Dentro do método `build()` é onde toda mágica deve acontencer, ele é responsável por manusear tudo que é preciso para geração daquele contrato.

Exemplo:
```python
class RegulamentoConcorrenciaBuilder(ContractBuilderBase):

def build(self) -> None:
    soma = 1+1
    documents = documents_soma(soma)
    gerar_pdf(documents)
```

#### 3.4.3 - Facade
Responsável por estruturar como os dados devem ser entregues ao motor de documento.

#### 3.4.4 - Documents Factory
Parte de suma importância para que o documento seja gerado corretamente. Nesse arquivo você irá retornar uma lista contendo as instâncias dos arquivos que devem ser gerados.

Exemplo, para o modelo `MLP_002` do regulamento, esses três (MLP002Capa, MLP002Miolo, MLP002Rodape) são os documentos necessários para geração do Regulamento:
```python
if regulamento_type == "MLP_002":
    return [MLP002Capa(wallet_id, data), MLP002Miolo(wallet_id, data), MLP002Rodape(wallet_id, data)]
```

##### 3.4.4.1 - Layers
Os Layers basicamente são os arquivos em si, a ideia é que eles representam uma parte singular do documento que será construído, possuem dois tipos o Layer padrão de um tipo de Contract e um Layer que é Default. É interessante que você separe eles em dois arquivos e nomeá-los corretamente, isso pode facilitar bastante sua vida.
**Exemplo:**
![image](https://user-images.githubusercontent.com/92036660/191810167-37e7a115-d482-40cc-a2cc-6c15b3d1cc54.png)

##### 3.4.4.2 - Templates
Templates são um conjunto de Layers que agrupados irão resultar em um documento.
A partir do `build()` do template que o documento irá construir o seu file_bytes.
Devem sempre herdar da Interface `ContractBuilderInterface`

##### 3.4.4.X - Observação
É muito importante lembrar que um Layer sempre deve herdar a classe do seu `Template` e o `TIPO` de seu Documento.
Exemplo:
```python
class MLP002Capa(MLP002, HTMLDocument):

    document_name = "MLP_002 - CAPA"
    current_layer = "capa.html"


class MLP002Miolo(MLP002, PDFDocument):

    document_name = "MLP_002 - MIOLO"
    current_layer = "miolo.pdf"


class MLP002Rodape(RegulamentoConcorrenciaRodapeDefault):

    document_name = "MLP_002 - RODAPÉ"
    stylesheets = "regulamento.css"
    current_layer = []
```
Ai você me pergunta, "Wesley, por que que o Rodapé então tá herdando somente o Template e o tipo de documento não?"
Pois, na verdade esse Rodapé do Regulamento ele é mais pra um Template do que um Layer, ele é uma união de diversos Layers, entenda os `Layers` como a estrutura de um documento em si.

Olhe aonde ele instancia todos os layes para o Rodapé:
```python
class RegulamentoConcorrenciaRodapeDefault(ContractBuilderInterface):

    template_path = PATH_REGULAMENTO_FOLDER

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(RegulamentoConcorrenciaRodapeTituloDefault())

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                RegulamentoConcorrenciaRodapeImovelDefault(imovel))

        return current_layer
```
Se você perceber, `RegulamentoConcorrenciaRodapeTituloDefault` e `RegulamentoConcorrenciaRodapeImovelDefault` vão ser os nossos LAYERS oficiais.

-------

Tendo todos esses pontos em vista, agora que temos nossos **Templates** propriamente estruturados e todos os nossos dados do **Builder** do **Contract**.
Iremos para a **função** `_generate_documents` do nosso `ContractBuilderBase`.

Aqui dentro é onde ele irá **percorrer** a nossa **Lista** `[MLP002Capa(wallet_id, data), MLP002Miolo(wallet_id, data), MLP002Rodape(wallet_id, data)]`

É de extrema importância que os **builds** dos nossos **Templates** sempre retornem o `file_bytes` do nosso documento.

# ---------------------------------- ATENÇÃO! --------------------------------------
## **Nunca altere** as funções que se encontram dentro da nossa estrutura base do `Contract`, todos os dados devem ser manipulados somente no **Builder** do **Contract** que está sendo desenvolvido.

## Em outras palavras, **não altere** código nesses carinhas:
![image](https://user-images.githubusercontent.com/92036660/191813622-aa6910f5-9837-4a75-b5a5-17da4c84f989.png)
