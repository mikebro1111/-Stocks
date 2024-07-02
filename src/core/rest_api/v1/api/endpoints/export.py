from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from slowapi.util import get_remote_address
from slowapi import Limiter
from typing import List
from pydantic import BaseModel
import csv
import os
import xml.etree.ElementTree as ET
from openpyxl import Workbook

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

# Moodel of data
class Item(BaseModel):
    id: int
    name: str
    description: str = None
    price: float
    tax: float = None


# Example
items_db = [
    Item(id=1, name="Item 1", description="Description 1", price=10.0, tax=1.5),
    Item(id=2, name="Item 2", description="Description 2", price=20.0, tax=3.0),
]


@router.get("/items/", response_model=List[Item])
@limiter.limit("5/minute")
def get_items():
    return items_db


@router.get("/items/export/csv/")
@limiter.limit("5/minute")
def export_items_csv():
    filename = "items_export.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "description", "price", "tax"])
        for item in items_db:
            writer.writerow([item.id, item.name, item.description, item.price, item.tax])

    return FileResponse(filename, media_type='text/csv', filename=filename)


@router.get("/items/export/json/")
@limiter.limit("5/minute")
def export_items_json():
    return JSONResponse(content=[item.dict() for item in items_db])


@router.get("/items/export/xml/")
@limiter.limit("5/minute")
def export_items_xml():
    root = ET.Element("Items")
    for item in items_db:
        item_element = ET.SubElement(root, "Item")
        for key, value in item.dict().items():
            child = ET.SubElement(item_element, key)
            child.text = str(value)

    tree = ET.ElementTree(root)
    filename = "items_export.xml"
    tree.write(filename)

    return FileResponse(filename, media_type='application/xml', filename=filename)


@router.get("/items/export/xlsx/")
@limiter.limit("5/minute")
def export_items_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.append(["id", "name", "description", "price", "tax"])
    for item in items_db:
        ws.append([item.id, item.name, item.description, item.price, item.tax])

    filename = "items_export.xlsx"
    wb.save(filename)

    return FileResponse(filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        filename=filename)
