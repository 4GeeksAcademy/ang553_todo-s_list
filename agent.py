import csv
import json
import os
from datetime import datetime
from typing import Any, Dict

import requests
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno desde .env
load_dotenv()

# ---------- CONFIGURACIÓN ----------
API_BASE_URL = "http://127.0.0.1:8000"
CSV_LOG = "conversation_log.csv"

# Cliente de Groq (compatible con OpenAI)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# ---------- TOOLS ----------
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_inventory",
            "description": "Devuelve la lista completa del inventario.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_product",
            "description": "Anade un nuevo producto al inventario con nombre, cantidad y unidad.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Nombre del producto"},
                    "quantity": {"type": "number", "description": "Cantidad inicial del producto"},
                    "unit": {"type": "string", "description": "Unidad de medida, por ejemplo kg, litros o unidades"},
                },
                "required": ["name", "quantity", "unit"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_stock",
            "description": "Actualiza el stock de un producto usando un delta. Un delta positivo suma stock y uno negativo resta stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer", "description": "ID del producto"},
                    "delta": {"type": "number", "description": "Cantidad que se suma o se resta al stock"},
                },
                "required": ["product_id", "delta"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_low_stock_alerts",
            "description": "Obtiene los productos cuya cantidad esta por debajo de un umbral. Si no se indica, usa 10 por defecto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold": {"type": "number", "description": "Umbral opcional para considerar stock bajo"},
                },
                "required": [],
            },
        },
    },
]

# ---------- EJECUTORES DE TOOLS ----------
def handle_response(response: requests.Response) -> Dict[str, Any]:
    try:
        payload = response.json()
    except ValueError:
        payload = {"detail": response.text or "Respuesta no valida del servidor."}

    if response.ok:
        return {"ok": True, "status_code": response.status_code, "data": payload}

    return {"ok": False, "status_code": response.status_code, "error": payload}


def list_inventory() -> Dict[str, Any]:
    response = requests.get(f"{API_BASE_URL}/inventory", timeout=30)
    return handle_response(response)


def create_product(name: str, quantity: float, unit: str) -> Dict[str, Any]:
    response = requests.post(
        f"{API_BASE_URL}/inventory",
        json={"name": name, "quantity": quantity, "unit": unit},
        timeout=30,
    )
    return handle_response(response)


def update_stock(product_id: int, delta: float) -> Dict[str, Any]:
    response = requests.patch(
        f"{API_BASE_URL}/inventory/{product_id}",
        json={"delta": delta},
        timeout=30,
    )
    return handle_response(response)


def get_low_stock_alerts(threshold: float = 10) -> Dict[str, Any]:
    params = {}
    if threshold is not None:
        params["threshold"] = threshold
    response = requests.get(f"{API_BASE_URL}/inventory/alerts", params=params, timeout=30)
    return handle_response(response)

TOOL_FUNCTIONS = {
    "list_inventory": list_inventory,
    "create_product": create_product,
    "update_stock": update_stock,
    "get_low_stock_alerts": get_low_stock_alerts,
}

# ---------- LOG ----------
def log_event(actor: str, message: str, tool_call: str = ""):
    with open(CSV_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([actor, message, tool_call, datetime.now().isoformat()])


def call_llm(messages):
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

# ---------- BUCLE PRINCIPAL ----------
def main():
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("Falta GROQ_API_KEY en el archivo .env o en las variables de entorno.")

    print("🤖 Agente de Inventario (escribe 'salir' para terminar)")
    print("=" * 50)

    if not os.path.exists(CSV_LOG):
        with open(CSV_LOG, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["actor", "message", "tool_call", "timestamp"])

    messages = [
        {
            "role": "system",
            "content": (
                "Eres un asistente de inventario para una cafetería. "
                "Ayudas a Carla a gestionar el stock de productos. "
                "Puedes listar productos, ver detalles, añadir nuevos, "
                "actualizar cantidades (entregas o ventas) y mostrar alertas de stock bajo. "
                "Responde siempre en español, de forma clara y amable."
            ),
        }
    ]

    while True:
        user_input = input("\n🧑‍💼 Carla: ")
        if user_input.lower() in ("salir", "exit", "quit"):
            print("👋 ¡Hasta luego!")
            break

        log_event("user", user_input)
        messages.append({"role": "user", "content": user_input})

        while True:
            response = call_llm(messages)

            choice = response.choices[0]
            message = choice.message

            if message.tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments or "{}",
                            },
                        }
                        for tool_call in message.tool_calls
                    ],
                })

                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    raw_arguments = tool_call.function.arguments or "{}"
                    func_args = json.loads(raw_arguments)
                    if func_args is None:
                        func_args = {}
                    tool_message = f"Llamando a {func_name} con argumentos {json.dumps(func_args, ensure_ascii=False)}"
                    print(f"  🔧 {tool_message}")
                    log_event("tool", tool_message, func_name)

                    func = TOOL_FUNCTIONS[func_name]
                    result = func(**func_args)

                    result_str = json.dumps(result, ensure_ascii=False)
                    print(f"  ✅ Resultado: {result_str[:200]}...")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": func_name,
                        "content": result_str,
                    })

                    log_event("tool", result_str, func_name)
            else:
                final_msg = message.content or "No he podido generar una respuesta final."
                print(f"\n🤖 Agente: {final_msg}")
                log_event("agent", final_msg)
                messages.append({"role": "assistant", "content": final_msg})
                break


if __name__ == "__main__":
    main()