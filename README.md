# 🗂️ API para Red Social (Posteos y Usuarios)

Este es un proyecto de aprendizaje desarrollado con **FastAPI**, que comenzó como una API para gestionar posteos en una red social y fue evolucionando para incluir autenticación de usuarios y manejo seguro de contraseñas.

## 🧩 Funcionalidades actuales

- 📬 Crear, leer, actualizar y eliminar posteos
- 👤 Registro de usuarios
- 🔐 Hashing de contraseñas con `bcrypt` (en desarrollo)
- 🧠 Validación de datos con Pydantic
- 📦 Conexión a base de datos PostgreSQL con SQLAlchemy

## 🛠️ Tecnologías usadas

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- (próximamente) JWT para autenticación

## 📁 Estructura del proyecto

app/
├── main.py # Punto de entrada de la app FastAPI
├── models.py # Modelos de SQLAlchemy para usuarios y posteos
├── schemas.py # Esquemas de entrada/salida con Pydantic
├── utils.py # Funciones auxiliares (hashing, validaciones, etc.)
├── database_example.py # Configuración de conexión a la base de datos (sin datos reales)
└── init.py


## 📌 Seguridad

⚠️ **Importante:** El archivo real con la contraseña de la base de datos (`database.py`) está **excluido con `.gitignore`** y no se sube al repositorio. Solo se incluye un archivo de ejemplo sin credenciales (`database_example.py`).

## ▶️ Cómo correr la API

#1. Crear un entorno virtual:
python -m venv venv


#2.Activar el entorno:
# En Windows
venv\Scripts\activate

# En Mac/Linux
source venv/bin/activate

#3.Instalar dependencias:
pip install -r requirements.txt


#4.Ejecutar la API:
uvicorn app.main:app --reload

#5.Acceder a la documentación interactiva:

http://localhost:8000/docs

💡 Nota final
Este proyecto es parte de mi formación como backend developer. Estoy construyéndolo paso a paso. ¡Toda sugerencia es bienvenida!




