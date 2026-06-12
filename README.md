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
git clone "https://github.com/Gutbla/Group_3_Quality_Assurance_III_Test_Automation_Framework"
```

```bash
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
USERNAME=tu_usuario_github
REPO_NAME=tu_repositorio
ACCESS_TOKEN=tu_github_token
```

> **Nota:** El token de GitHub debe tener los siguientes scopes habilitados: `repo`, `user`, `delete_repo`.

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
│   ├── pull_request_data.py           # Payloads para pruebas de pull requests
│   ├── repository_data.py             # Payloads para pruebas de repositorios
│   └── user_data.py                   # Payloads para pruebas de usuarios
│
├── documentation/
│   ├── collections/                   # Colecciones de Postman
│   ├── environments/                  # Variables de entorno Postman
│   └── reports/                       # Reportes HTML generados
│
├── logs/                              # Archivos de log generados por cada ejecución
│
├── services/
│   ├── github_issues_api.py           # Cliente para endpoints de issues
│   ├── github_labels_api.py           # Cliente para endpoints de labels
│   ├── github_pull_requests_api.py    # Cliente para endpoints de pull requests
│   ├── github_repositories_api.py     # Cliente para endpoints de repositorios
│   ├── github_user_api.py             # Cliente para endpoints de usuarios
│   └── request_manager.py             # Singleton — gestor de peticiones HTTP
│
├── tests/
│   ├── conftest.py                    # Configuración principal de Pytest (carga de plugins)
│   ├── fixtures/                      # Fixtures modularizadas (pytest_plugins)
│   │   ├── __init__.py                # Inicializador de paquete de Python (vacío)
│   │   ├── api_fixtures.py            # Inicializadores de clientes API
│   │   ├── data_fixtures.py           # Precondiciones y postcondiciones de datos
│   │   └── logging_fixtures.py        # Hooks globales de logging y sesión
│   │
│   ├── unit/                          # Tests unitarios para core y utilidades
│   │   ├── test_pull_requests_api.py
│   │   ├── test_request_manager.py
│   │   ├── test_schema_validator.py
│   │   └── test_user_api.py
│   │
│   ├── issues/
│   │   └── test_issues.py
│   ├── labels/
│   │   └── test_labels.py
│   ├── pull_requests/
│   │   ├── __init__.py
│   │   └── test_pull_requests.py
│   ├── repositories/
│   │   └── test_repository.py
│   └── users/
│       ├── test_user_follow.py
│       └── test_user_profile.py
│
├── utils/
│   ├── logger.py                      # Logger centralizado (genera archivos .log)
│   ├── schemas.py                     # JSON Schemas para validación de respuestas
│   └── schema_validator.py            # Motor de validación de esquemas
│
├── pytest.ini                         # Configuración de Pytest (pythonpath y markers)
├── requirements.txt                   # Dependencias del proyecto
├── show_logs.py                       # Script para ejecutar tests y visualizar logs
└── .env                               # Variables de entorno (no commitear)
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
python -m pytest tests/issues/test_issues.py -v
python -m pytest tests/users/test_user_profile.py -v
```

**Ejecutar tests por módulo:**

```bash
# Tests de usuarios
python -m pytest tests/users/ -v

# Tests de pull requests
python -m pytest tests/pull_requests/ -v

# Tests de labels
python -m pytest tests/labels/ -v

# Tests de repositorios
python -m pytest tests/repositories/ -v

# Tests unitarios
python -m pytest tests/unit/ -v
```

**Ejecutar pruebas filtrando por etiquetas (markers):**

```bash
python -m pytest -m smoke -v
python -m pytest -m negative -v
python -m pytest -m functional -v
python -m pytest -m regression -v
python -m pytest -m "functional and smoke" -v
```

**Ejecutar y visualizar logs:**

```bash
python show_logs.py
```

---

## Ramas del proyecto

| Rama | Descripción |
|------|-------------|
| `main` | Rama principal estable |
| `ct/day-1-03-06-2026` | CT Day 1 — 52 tests, 52 passed |
| `ct/day-2-04-06-2026` | CT Day 2 — 52 tests, 50 passed |
| `ct/day-3-05-06-2026` | CT Day 3 — 52 tests, 51 passed |
| `ct/day-4-06-06-2026` | CT Day 4 — 52 tests, 52 passed |
| `ct/day-5-07-06-2026` | CT Day 5 — 52 tests, 52 passed |

---

## Convención de commits

```
feat: descripción del feature agregado
fix: descripción del bug corregido
test: nueva prueba automatizada
docs: actualización de documentación
```

---

## Calidad de código (Linter)

Este proyecto utiliza **Flake8** junto con el plugin **flake8-naming** para garantizar que todo el código del framework cumpla con las buenas prácticas de Python (PEP 8) y las convenciones oficiales de nomenclatura de variables, clases y funciones.

### Instalación del plugin de nomenclatura

```bash
python -m pip install flake8-naming
```

### Ejecución

Activa tu entorno virtual y ejecuta en la raíz del proyecto:

```bash
flake8 .
```

Si el comando no devuelve ningún mensaje, el código está limpio. De lo contrario, la herramienta reportará los siguientes tipos de error:

| Código | Tipo de error | Significado técnico (PEP 8) |
| :--- | :--- | :--- |
| **F401** | *Unused Import* | Librería o módulo importado que no se está utilizando en el archivo. |
| **E501** | *Line Too Long* | Línea que excede el límite máximo de caracteres configurado para el proyecto. |
| **W292** | *No Newline at EOF* | Falta una línea en blanco al final del archivo (End Of File). |
| **W291 / W293** | *Trailing Whitespace* | Espacios en blanco huérfanos al final de una línea de código. |
| **N802** | *Function Name Case* | El nombre de una función no está en *snake_case*. |
| **N803** | *Argument Name Case* | El argumento de una función o método no cumple con *snake_case*. |
| **N806** | *Local Variable Case* | Una variable declarada dentro de una función tiene letras mayúsculas. |
| **N801** | *Class Name Case* | El nombre de una clase no sigue el formato *CamelCase* / *PascalCase*. |

---

## Calidad y testing

Este framework asegura la estabilidad mediante una estrategia de pruebas en dos niveles:

**Pruebas unitarias** (`tests/unit/`): Validan la lógica crítica, incluyendo el patrón Singleton en `request_manager.py`, los contratos de la API de pull requests y usuarios, y la integridad de los schemas mediante `schema_validator.py`.

**Pruebas funcionales** (`tests/issues/`, `tests/labels/`, `tests/pull_requests/`, `tests/repositories/`, `tests/users/`): Validan el comportamiento real de los endpoints de la GitHub REST API contra escenarios positivos, negativos, de smoke y de regresión.

### Cobertura

Se utiliza `pytest-cov` para medir la efectividad de las pruebas. La cobertura se genera automáticamente en el pipeline de CI/CD.

**Instalación:**

```bash
pip install pytest pytest-cov
```

**Ejecución local con reporte de cobertura:**

```bash
pytest --cov=services/ --cov=utils/ --cov-report=term-missing --cov-report=html:reports/coverage
```

**Ver resultados:**

- **Terminal:** El reporte de cobertura se mostrará automáticamente en la consola al finalizar.
- **HTML:** Abre el archivo `reports/coverage/index.html` en tu navegador para ver el reporte detallado.

---

## Continuous Testing — Daily Runs

Ejecuciones diarias del pipeline de CT durante los últimos 5 días. Cada ejecución se activa mediante un push o manualmente a través de GitHub Actions.

| Day   | Date       | Branch                | Total Tests | Passed | Failed | Duration | Status |
|-------|------------|-----------------------|-------------|--------|--------|----------|--------|
| Day 1 | 03-06-2026 | `ct/day-1-03-06-2026` | 52          | 52     | 0      | 01:16    | ✅     |
| Day 2 | 04-06-2026 | `ct/day-2-04-06-2026` | 52          | 50     | 2      | 00:51    | ⚠️     |
| Day 3 | 05-06-2026 | `ct/day-3-05-06-2026` | 52          | 51     | 1      | 00:18    | ⚠️     |
| Day 4 | 06-06-2026 | `ct/day-4-06-06-2026` | 52          | 52     | 0      | 00:17    | ✅     |
| Day 5 | 07-06-2026 | `ct/day-5-07-06-2026` | 52          | 52     | 0      | 00:19    | ✅     |
