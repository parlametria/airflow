# Airflow Parlametria

Esse README irá descrever como fazer o settup do ambiente do airflow.

## Settup ambiente de desenvolvimento

Como os scripts do Parlametria executam o docker, para evitar de executar docker dentro de docker o ambiente do airflow é local, porém é recomendo a utilização de uma ferramenta para gerenciar ambientes python como [pyenv](https://github.com/pyenv/pyenv) por exemplo.

### Instalação

Para intalar basta fazer um pip install:
```bash
pip install -r requirements.txt
pip install -e .
```

Após o install do pip sete a variável de ambiente necessária:
- AIRFLOW_HOME: Variável de ambiente que indica para o airflow o caminho para a pasta do airflow local

Em seguida fazer o settup do banco de dados:
```bash
airflow db init
```

E após os settup do banco, crie um usuário admin:
```bash
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
```

## Utilização

Com o seu ambiente devidamente preparado, para executar o airflow mas utilizar os comandos do Makefile: `make webserver` e `make scheduler`.

- make webserver: aplicação web que possibilita o gerenciamento das Dags.
- make scheduler: serviço que busca por novas Dags na pasta dags e também é responsável por executar-las de acordo com o settup do `schedule_interval` e `start_date` de cada Dag.

Para a ativação das Dags é necessário que ambos webserver e scheduler estejam sendo executados simultaneamente, mas uma vez ativada apenas o scheduler é necessário.
