# Group 3 — Quality Assurance III: Test Automation Framework

Framework de automatización de pruebas de API usando Python y Pytest sobre la GitHub REST API.

## Tecnologías utilizadas

- Python 3.12+
- Pytest
- Requests
- JSONSchema
- python-dotenv
- GitHub REST API

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone "https://github.com/GutBla/Group_3_Quality_Assurance_III_Test_Automation_Framework.git"

cd Group_3_Quality_Assurance_III_Test_Automation_Framework
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

**Activar en Windows:**
```bash
.venv\Scripts\activate
```

**Activar en macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

---

## Configuración del proyecto

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
BASE_URL=https://api.github.com
GITHUB_USERNAME=tu_usuario_github
GITHUB_REPO=tu_repositorio
GITHUB_TOKEN=tu_github_token
```

---

## Estructura del proyecto

```
Group_3_Quality_Assurance_III_Test_Automation_Framework/
│
├── config/
│   └── config.py                      # Variables de entorno y configuración
│
├── data/
│   ├── issue_data.py                  # Payloads para pruebas de issues
│   ├── label_data.py                  # Payloads para pruebas de labels
│   ├── repository_data.py             # Payloads para pruebas de repositorios
│   └── user_data.py                   # Payloads para pruebas de usuarios
│
├── documentation/
│   ├── collections/
│   ├── environments/
│   └── reports/
│
├── logs/                              # Archivos de log generados por cada ejecución
│
├── services/
│   ├── github_issues_api.py           # Cliente para endpoints de issues
│   ├── github_labels_api.py           # Cliente para endpoints de labels
│   ├── github_repositories_api.py     # Cliente para endpoints de repositorios
│   ├── github_user_api.py             # Cliente para endpoints de usuarios
│   └── request_manager.py             # Singleton — gestor de peticiones HTTP
│
├── tests/
│   ├── issues/
│   │   └── test_create_issue.py
│   ├── labels/
│   │   └── test_labels.py
│   ├── repositories/
│   │   └── test_create_repository.py
│   └── users/
│       ├── test_get_user.py
│       └── test_hltc18_update_profile.py
│
├── utils/
│   ├── logger.py                      # Logger centralizado (genera archivos .log)
│   └── schemas.py                     # JSON Schemas para validación de respuestas
│
├── conftest.py                        # Fixtures globales + hooks de logging
├── pytest.ini                         # Configuración de Pytest
├── requirements.txt                   # Dependencias del proyecto
├── show_logs.py                       # Script para ejecutar tests y visualizar logs
└── .env                               # Variables de entorno (no subir al repo)
```

---

## Cómo ejecutar las pruebas

> Siempre usar `python -m pytest` para asegurar que se usa el entorno virtual activo.

**Ejecutar todos los tests:**
```bash
python -m pytest -v
```

**Ejecutar un archivo específico:**
```bash
python -m pytest tests/issues/test_create_issue.py -v
python -m pytest tests/users/test_hltc18_update_profile.py -v
```

**Ejecutar por rama de feature:**
```bash
git checkout feature/HLTC-18-actualizar-perfil-github-api
python -m pytest tests/users/test_hltc18_update_profile.py -v
```

---

## Ramas del proyecto

| Rama | Descripción |
|------|-------------|
| `main` | Rama principal estable |
| `feature/HLTC-18-actualizar-perfil-github-api` | Prueba automatizada HLTC-18: actualizar perfil de usuario |

---

## Convención de commits

```
feat: descripción del feature agregado
fix: descripción del bug corregido
test: nueva prueba automatizada
docs: actualización de documentación
```

##  Calidad de Código (Linter)

Este proyecto utiliza **Flake8** para garantizar que todo el código del framework cumpla con las buenas prácticas de Python (PEP 8).

### Ejecución

Para analizar el código, activa tu entorno virtual y ejecuta en la raíz del proyecto:

```bash
flake8 .

Códigos de Advertencia Comunes
Si el comando no devuelve ningún mensaje, el código está limpio. De lo contrario, podrías ver:

F401: Librería importada que no se está usando.

E501: Línea demasiado larga (Límite del proyecto: 88 caracteres).

W292: Falta una línea en blanco al final del archivo.

W291/W293: Espacios en blanco fantasmas o invisibles al final de las líneas.