# Airflow Parlametria

Esse README irá descrever como fazer o settup do ambiente do airflow.

## Settup ambiente de desenvolvimento

É utilizado o docker e docker-compose para a execução do airflow:
- Instalação do docker: https://docs.docker.com/engine/install/ubuntu/
- Instalação do docker-compose: https://docs.docker.com/compose/install/

### Instalação

Tendo o docker o docker-compose instaladados para fazer a build basta fazer:

Para intalar basta fazer um pip install:
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

## Utilização

Com o seu ambiente devidamente preparado, para executar o airflow mas utilizar os comandos do Makefile: `make dev-webserver` para o webserver e `make dev-scheduler` para o scheduler, caso queira executar ambos tem o comando `make dev-up`.

- make webserver: aplicação web que possibilita o gerenciamento das Dags.
- make scheduler: serviço que busca por novas Dags na pasta dags e também é responsável por executar-las de acordo com o settup do `schedule_interval` e `start_date` de cada Dag.

Para a ativação das Dags é necessário que ambos webserver e scheduler estejam sendo executados simultaneamente, mas uma vez ativada apenas o scheduler é necessário.
