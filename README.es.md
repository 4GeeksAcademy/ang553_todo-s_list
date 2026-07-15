# Agente de Inventario con IA

Este proyecto tiene dos procesos que trabajan juntos:

- Una API REST con FastAPI en [api/app.py](/workspaces/MarcJuvanteny_python-hello/api/app.py) que guarda el inventario en `products.csv`.
- Un agente CLI en [agent.py](/workspaces/MarcJuvanteny_python-hello/agent.py) que usa la API como tools y registra cada paso en `conversation_log.csv`.

## Requisitos

- Python 3.10 o superior.
- Una clave de Groq guardada en `.env`.

Instala las dependencias:

```bash
pip install fastapi uvicorn openai requests python-dotenv
```

Crea un archivo `.env` en la raiz del proyecto:

```env
GROQ_API_KEY=tu_clave_aqui
```

Asegurate de incluir `.env` en `.gitignore`.

## Como arrancarlo

Necesitas dos terminales.

Terminal 1, arranca la API:

```bash
uvicorn api.app:app --reload
```

Terminal 2, arranca el agente:

```bash
python agent.py
```

La API debe estar en ejecucion antes de arrancar el agente.

## Endpoints de la API

- `GET /inventory`: lista completa del inventario.
- `POST /inventory`: crea un producto con `name`, `quantity` y `unit`.
- `PATCH /inventory/{product_id}`: actualiza el stock usando `delta`.
- `GET /inventory/alerts`: devuelve productos por debajo de un umbral configurable, por defecto `10`.

## Ejemplos de mensajes

- `Anade 30 litros de leche de avena`
- `Vendimos 12 unidades de vasos termicos`
- `Que productos estan por agotarse?`
- `Ensename el inventario completo`
