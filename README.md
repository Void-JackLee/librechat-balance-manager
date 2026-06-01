# librechat-balance-manager

## Install

1. Add this component to `deploy-compose.yml` in `LibreChat`.

    ```yml
    balance-manager:
    build: ../librechat-balance-manager
    ports:
        - "3010:3010"
    volumes:
        - ../librechat-balance-manager/config.docker:/app/config
    depends_on:
        - mongodb
    ```

2. Copy `config.example.yml` to `config.yml` in `config.docker`.

    ```shell
    cp config.docker/config.example.yml config.docker/config.yml
    ```

3. Fill the `xxx` in `config.yml` and start the `deploy-compose.yml` in `LibreChat`.