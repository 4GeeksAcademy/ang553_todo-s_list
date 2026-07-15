import csv
import os
from typing import List

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="Inventory API", version="1.0.0")

CSV_FILE = "products.csv"
CSV_HEADERS = ["id", "name", "quantity", "unit"]


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    quantity: float = Field(..., ge=0)
    unit: str = Field(..., min_length=1)


class ProductDelta(BaseModel):
    delta: float


class Product(BaseModel):
    id: int
    name: str
    quantity: float
    unit: str


def ensure_csv_exists() -> None:
    if os.path.exists(CSV_FILE):
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writeheader()


def read_products() -> List[Product]:
    ensure_csv_exists()

    with open(CSV_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [
            Product(
                id=int(row["id"]),
                name=row["name"],
                quantity=float(row["quantity"]),
                unit=row["unit"],
            )
            for row in reader
        ]


def write_products(products: List[Product]) -> None:
    ensure_csv_exists()

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for product in products:
            writer.writerow(product.model_dump())


def next_product_id(products: List[Product]) -> int:
    return max((product.id for product in products), default=0) + 1


def find_product_index(products: List[Product], product_id: int) -> int:
    for index, product in enumerate(products):
        if product.id == product_id:
            return index

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe ningun producto con id {product_id}.",
    )


@app.get("/")
def root() -> dict:
    return {
        "message": "Inventory API running",
        "docs": "/docs",
        "inventory": "/inventory",
        "alerts": "/inventory/alerts",
    }


@app.get("/inventory", response_model=List[Product])
def list_inventory() -> List[Product]:
    return read_products()


@app.post("/inventory", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_inventory_product(product: ProductCreate) -> Product:
    products = read_products()

    new_product = Product(
        id=next_product_id(products),
        name=product.name.strip(),
        quantity=product.quantity,
        unit=product.unit.strip(),
    )

    products.append(new_product)
    write_products(products)
    return new_product


@app.patch("/inventory/{product_id}", response_model=Product)
def update_inventory_stock(product_id: int, payload: ProductDelta) -> Product:
    products = read_products()
    product_index = find_product_index(products, product_id)
    product = products[product_index]

    updated_quantity = product.quantity + payload.delta
    if updated_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Stock insuficiente para el producto {product.name}. "
                f"Cantidad actual: {product.quantity}, delta solicitado: {payload.delta}."
            ),
        )

    updated_product = Product(
        id=product.id,
        name=product.name,
        quantity=updated_quantity,
        unit=product.unit,
    )
    products[product_index] = updated_product
    write_products(products)
    return updated_product


@app.get("/inventory/alerts", response_model=List[Product])
def get_inventory_alerts(threshold: float = Query(10, gt=0)) -> List[Product]:
    products = read_products()
    return [product for product in products if product.quantity < threshold]