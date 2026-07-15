# AI Inventory Agent

This project includes two processes that work together:

- A FastAPI REST API in [api/app.py](/workspaces/MarcJuvanteny_python-hello/api/app.py) that stores inventory data in `products.csv`.
- A CLI agent in [agent.py](/workspaces/MarcJuvanteny_python-hello/agent.py) that uses the API as tools and logs every loop step in `conversation_log.csv`.

## Requirements

- Python 3.10+
- A Groq API key stored in `.env`

Install dependencies:

```bash
pip install fastapi uvicorn openai requests python-dotenv
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_key_here
```

Make sure `.env` is included in `.gitignore`.

## Run the project

You need two terminals.

Terminal 1, start the API:

```bash
uvicorn api.app:app --reload
```

Terminal 2, start the agent:

```bash
python agent.py
```

The API must be running before you start the agent.

## API endpoints

- `GET /inventory`: list all products.
- `POST /inventory`: create a product with `name`, `quantity` and `unit`.
- `PATCH /inventory/{product_id}`: update stock using a `delta` value.
- `GET /inventory/alerts`: list products below a configurable threshold, default `10`.

## Example prompts

- `Anade 30 litros de leche de avena`
- `Vendimos 12 unidades de vasos termicos`
- `Que productos estan por agotarse?`
- `Ensename el inventario completo`
