# Airflow Parlametria

Esse README irá descrever como fazer o settup do ambiente do airflow.

É utilizado o docker e docker-compose para a execução do airflow:
- Instalação do docker: https://docs.docker.com/engine/install/ubuntu/
- Instalação do docker-compose: https://docs.docker.com/compose/install/

## Variáveis de ambiente

- Crie um arquivo chamado .env e cole nele as variáveis do .env.example, os valores são os mesmos utilizados pelo [leggo-geral](https://github.com/parlametria/leggo-geral);
- Crie um arquivo .env.leggo-twitter-dados, os valores são os mesmo do repositório [leggo-twitter-dados](https://github.com/parlametria/leggo-twitter-dados)

## Pre-instalação

O airflow usa os mesmos containers das builds do setup do [leggo-geral](https://github.com/parlametria/leggo-geral), então é necessário buildar todos os repositórios listados no setup do [leggo-geral](https://github.com/parlametria/leggo-geral). Não é necessário buildar o [leggo-geral](https://github.com/parlametria/leggo-geral) em si mas os demais repositórios listados no setup deste.

## Setup ambiente de desenvolvimento

### Instalação

Tendo o docker o docker-compose instaladados para fazer a build basta fazer:

Primeiramente, faça um build:
```bash
make dev-build
```

Em seguida, para fazer o settup do banco de dados:
```bash
make dev-bash
```
Estando dentro do container execute:
```bash
airflow db init
```

Após o settup do banco, ainda dentro do container, crie um usuário admin:
```bash
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
```

### Utilização

Com o seu ambiente devidamente preparado, para executar o airflow mas utilizar os comandos do Makefile: `make dev-webserver` para o webserver e `make dev-scheduler` para o scheduler, caso queira executar ambos tem o comando `make dev-up`.

- make webserver: aplicação web que possibilita o gerenciamento das Dags.
- make scheduler: serviço que busca por novas Dags na pasta dags e também é responsável por executar-las de acordo com o settup do `schedule_interval` e `start_date` de cada Dag.

Para a ativação das Dags é necessário que ambos webserver e scheduler estejam sendo executados simultaneamente, mas uma vez ativada apenas o scheduler é necessário.

## Setup ambiente de produção

### Instalação

Tendo o docker o docker-compose instaladados para fazer a build basta fazer:

Primeiramente, faça um build:
```bash
make prod-build
```

Em seguida, para fazer o settup do banco de dados:
```bash
make prod-bash
```
Estando dentro do container execute:
```bash
airflow db init
```

Após o settup do banco, ainda dentro do container, crie um usuário admin:
```bash
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
```

### Utilização

Com o seu ambiente devidamente preparado, para executar o airflow mas utilizar os comandos do Makefile: `make prod-webserver` para o webserver e `make prod-scheduler` para o scheduler, caso queira executar ambos tem o comando `make prod-up`.

- make webserver: aplicação web que possibilita o gerenciamento das Dags.
- make scheduler: serviço que busca por novas Dags na pasta dags e também é responsável por executar-las de acordo com o settup do `schedule_interval` e `start_date` de cada Dag.

Para a ativação das Dags é necessário que ambos webserver e scheduler estejam sendo executados simultaneamente, mas uma vez ativada apenas o scheduler é necessário.
