![Build Status](https://github.com//martinkuechler/einfuehrungsblatt/actions/workflows/main.yml/badge.svg)
![GitHub License](https://img.shields.io/github/license/martinkuechler/einfuehrungsblatt)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)






# Hausaufgabe 2

Dieses Projekt ist ein einfaches To-Do-Backend, das es ermöglicht, Aufgaben anzulegen, auszulesen und zu löschen.
Die Daten werden in einer SQLite-Datenbank gespeichert, und die API stellt dafür übersichtliche Endpunkte zur Verfügung.



## Authors

- [DenisGelgorn](https://github.com/DenisUni)
- [Martin Küchler](https://github.com/martinkuechler)




## Installation

Install my-project with npm


  #### 1. Repository klonen:
  ```bash
git clone https://github.com/martinkuechler/einfuehrungsblatt.git
cd einfuehrungsblatt
```

#### 2. Umgebung einrichten:
```bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. Server starten:
```bash
uvicorn backend.api:app --reload
```
Der Server läuft standardmäßig auf: http://127.0.0.1:8000


Der Server läuft standardmäßig auf: http://127.0.0.1:8000



