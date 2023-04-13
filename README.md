# Engenharia de Dados
Repositorio destinado a pratica de conceitos basicos e principais ferramentas de engenharia de dados. Neste repositorio temos um projeto onde usaremos EC2 e RDS da AWS, Airflow e Metabase, todos integrados entre si para que possamos acompanhar a jornada dos dados desde a ingestao ate a visualizacao do dados na cloud.

## Requisitos
- Conta AWS
- Instancia EC2 (se sua instancia for free tier, nao tera como rodar o airflow pois necessita de 4gb de ram)
- Instancia RDS free tier
- Conhecimentos em Python
- Conhecimentos em SQL

## Projeto
O projeto consiste em:
- Criar e configurar uma instancia EC2 Linux (servidor)
- Criar e configurar um RDS (Banco de dados Relacional em Nuvem)
- Subir um container com Airflow (Orquestrador de Pipelines de dados)
- Subir um container com Metabase (Ferramenta de DataViz)
- Implementar dois pipelines de dados de ETL de uma API para o RDS utilizando o Airflow e Visualizando os dados no Metabase.

Para isso existe um passo a passo que deve ser seguido:
- Criar um EC2
- Criar um RDS
- Fazer o passo a passo da secao Workflow do Projeto neste arquivo
- Fazer o passo a passo da secao Primeiro Acesso EC2
- Fazer o passo a passo da secao Docker neste arquivo
- Fazer o passo a passo da secao Airflow neste arquivo
- Fazer o passo a passo da secao Metabase neste arquivo

## Workflow do Projeto
Antes de iniciarmos o projeto precisamos seguir alguns passos:
- Criar uma conta na AWS
- Criar uma instancia EC2 t2.large com Ubuntu 22.04 LTS
- Criar uma instancia RDS PostgreSQL v14.6 free tier(db.t3.micro) e Publicamente Acessivel (qualquer ip da internet pode acessar o banco de dados)

### Intancia EC2
Com tudo isso criado, va ate sua instancia EC2 e na Aba "Seguranca", clique em "Grupos de Seguranca" que te levara para outra pagina Web. Faca os seguintes passos:
- Em "Regras de Entrada" clique no botao superior esquerdo "Editar Regras de entrada"
- Adicione uma nova regra de entrada
  - Tipo = TCP Personalizado
  - Intervalo de portas = 8080
  - Origem = Qualquer Local IPV4
- Agora adicione mais 2 regras de entrada, da mesma forma porem para as portas 5432 e 3000
- Clique em "Salvar Regras" para aplicar as mudancas

### Intancia RDS
Com tudo isso criado, va ate sua instancia RDS e na Aba "Segurança e conexão", clique em "Grupos de Seguranca" que te levara para outra pagina Web. Faca os seguintes passos:
- Em "Regras de Entrada" clique no botao superior esquerdo "Editar Regras de entrada"
- Adicione uma nova regra de entrada
  - Tipo = TCP Personalizado
  - Intervalo de portas = 5432
  - Origem = Qualquer Local IPV4
- Clique em "Salvar Regras" para aplicar as mudancas

## Primeiro Acesso EC2
Para acessar pela primeira vez sua instancia EC2 use alguma ferramenta para conectar ao servidor via ssh, como a extesao **Remote SSH** do VS Code ou o programa Putty. Lembre-se que para ambos os casos voce deve colocar o arquivo .pem na pasta C:/Users/<seu_user>/.ssh. 

Para utilizar o Remote SSH e necessario criar um arquivo JSON com as infos daquele servidor, para isso, utilize o exemplo abaixo.
```
Host <Nome_do_seu_servidor>
    User ubuntu
    HostName <IPv4 publico AWS>
    IdentityFile <Caminho para arquivo .pem>
```

Caso esteja com dificuldade para acessar via SSH, existe uma opcao de acesso diretamente da AWS. Para isso:
- Va ate a instancia EC2 criada
- Selecione a instancia desejada
- Havera um botao na tela superior direita escrito "Conectar"
- Mantenha as informacoes padrao e clique no botao amarelo "Conectar"

Ao acessar o terminal da instancia EC2 rode estes comando a seguir:
```
sudo apt update -y
sudo apt-get upgrade -y
sudo apt install python3-pip sqlite3 python3.10-venv -y
sudo apt-get install libpq-dev -y
pip install apache-airflow
```

## Docker 
Docker e um orquestrador de containers que roda sobre o linux. Para fazer o Download na sua instancia EC2, ser necessario rodar o arquivo bash da pasta "Usefull_Files/docker_install.sh.
```
cd Usefull_Files/
chmod +x docker_install.sh
./docker_install.sh
sudo apt install docker-compose
```

Com isso o Docker e o Docker-compose serao instalados no seu servidor EC2.
## Airflow
Esta pasta contem tudo que e necessario para subir um container no seu servidor com a aplicacao Airflow. Ha tambem algumas DAGs basicas do projeto como: 
- DAG para criar uma tabela no banco de dados ou fazer uma consulta diretamente no banco de dados
- DAG com um processo de ETL onde apresenta uma requisicao API, transformacao dos dados e carga no banco de dados RDS na AWS

Para subir o container airflow e necessario ter instalado o Docker e o Docker Compose!!!

Os comandos para subir um container sao:
```
cd /<path_para_pasta_airflow_no_servidor>/
docker-compose up -d 
```

Os comandos para derrubar um container sao:
```
cd /<path_para_pasta_airflow_no_servidor>/
docker-compose down
```

Para acessar a UI da sua aplicacao airflow sera necessario: 
- No seu navegador, ir a sua instancia EC2 criada anteriormente
- Achar a Aba "Detalhes" na sua instancia EC2 (Pagina Web)
- Copiar a informacao "DNS IPv4 público"
- Abrir nova aba no seu navegador
- Digitar: <DNS IPv4 público>:8080, onde "DNS IPv4 público" e o IP que voce copiou na etapa passada
- Colocar o usuario e senha do airflow, geralmente user=airflow pass=airflow

## Metabase
Esta pasta contem tudo que e necessario para subir um container no seu servidor com a aplicacao Metabase que e uma ferramenta de visualizacao de dados baseada em SQL. 

Na primeira vez que um container desta aplicacao subir, sera necessario colocar alguns dados como Nome, Email, Senha que podem ser fakes. Sera necessario tambem passar a informacao do seu banco de dados como Host, Database, User e Password para que a aplciacao se conecte ao Banco de dados e consiga executar as queries posteriormente.

Os comandos para subir um container sao:
```
cd /<path_para_pasta_metabase_no_servidor>/
docker-compose up -d 
```

Os comandos para derrubar um container sao:
```
cd /<path_para_pasta_metabase_no_servidor>/
docker-compose down
```

Para acessar a UI da sua aplicacao Metabase sera necessario: 
- No seu navegador, ir a sua instancia EC2 criada anteriormente
- Achar a Aba "Detalhes" na sua instancia EC2 (Pagina Web)
- Copiar a informacao "DNS IPv4 público"
- Abrir nova aba no seu navegador
- Digitar: <DNS IPv4 público>:3000, onde "DNS IPv4 público" e o IP que voce copiou na etapa passada
- Colocar o usuario e senha do metabase, se for solicitado.

## Postgresql
Esta pasta e apenas um demonstrativo de como montar um docker-compose.yaml para subir um container com um banco de dados postgresql. O mesmo nao sera utilizado no projeto pois cada aplicacao tem seu banco de dados de metadados e o banco de dados utilizado sera o RDS da AWS.


# Infos
Autor: Cesar Vinixius Zuge

Linkedin: https://www.linkedin.com/in/cesar-zuge/

