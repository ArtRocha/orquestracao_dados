# Image Pipeline System

Sistema de processamento de imagens baseado em microserviços.

## Como rodar

1. Vá até a pasta `infra/`
2. Suba o ambiente:
   ```bash
   docker compose up --build

3. Acesse:

Backend: http://localhost:8000

Frontend: http://localhost:5173

MinIO: http://localhost:9001

Redis: porta 6379

Postgres: porta 5432



---

✅ **Depois de criar esses arquivos**, você deve conseguir rodar:
```bash
cd infra
docker compose up --build


E ver:

O backend rodando no localhost:8000 e respondendo {"message": "API online 🚀"}

O worker imprimindo logs no terminal

O frontend servindo uma página HTML simples