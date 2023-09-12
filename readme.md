# Deploy System on Linux

1. Clone github repo to target machine
2. Create .env file for airflow follow 
    ```sh
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```
3. Create folder 
    ```
    logs
    plugins
    config
    ```
4. Run docker compose follow command below
    ```sh
    docker compose build
    docker compose -f .\docker-compose.airflow.yaml -f .\docker-compose.yaml up -d --build
    ```
5. Connect to Postgres with your favor cilent and execute all of SQL statement in table.sql (**user**:postgres **password**:123456789)
6. Airflow UI running at localhost:8080 (**user**: admin **password**:airflow)
7. Login Airflow UI 
8. Go to DAGs and turn on ETL dags
9. Run DAGs



