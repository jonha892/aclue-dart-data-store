# aclue-dart-data-store

Mini backend für das Aclue DartNet Projekt.

Die API ermöglicht es Wurfreihen und deren Labels zu verwalten. Bilder werden als `png` Dateien in einem `data` Ordner gespeichert. Beschreibungen werden in einem key-value store über DBM im `db` Ordner gespeichert.

## Requirements
```
python >=3.8
poetry
```

## Setup

poetry install

## Start
cd src
poetry shell
uvicorn main:app --reload --host=0.0.0.0 --port=6666

## Beispiel Requests

Beispiel für Requests finden sich in der postman collection.