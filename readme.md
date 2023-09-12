# Deploy System on Linux
    - Clone github repo to target machine
    - Create .env file for airflow follow 
    ```sh
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```
    - Create folder 
    ```
    logs
    plugins
    config
    ```
    - Run docker compose follow command below
    ```sh
        docker compose build
        docker compose -f .\docker-compose.airflow.yaml -f .\docker-compose.yaml up -d --build
    ```
    - Connect to Postgres with your favor cilent and execute all of SQL statement in table.sql (user:postgres password:123456789)
    - Airflow UI running at localhost:8080 (user: admin password:airflow)
    - Login Airflow UI 
    - Go to DAGs and turn on ETL dags
    



