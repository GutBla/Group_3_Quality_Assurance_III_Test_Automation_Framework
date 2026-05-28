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
│   ├── conftest.py                    # Configuración principal de Pytest (Carga de plugins)
│   │
│   ├── fixtures/                      # Fixtures modularizadas (pytest_plugins)
│   │   ├── __init__.py                # Inicializador de paquete de Python (vacío)
│   │   ├── api_fixtures.py            # Inicializadores de clientes API
│   │   ├── data_fixtures.py           # Precondiciones y postcondiciones de datos
│   │   └── logging_fixtures.py        # Hooks globales de logging y sesión
│   │
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
├── pytest.ini                         # Configuración de Pytest (incluye pythonpath y markers)
├── requirements.txt                   # Dependencias del proyecto
├── show_logs.py                       # Script para ejecutar tests y visualizar logs
└── .env        
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

## Calidad de Código (Linter)

Este proyecto utiliza **Flake8** junto con el plugin **flake8-naming** para garantizar que todo el código del framework cumpla de manera estricta con las buenas prácticas de Python (PEP 8) y las convenciones oficiales de nomenclatura de variables, clases y funciones.

### Instalación del Plugin de Nomenclatura

Para habilitar la verificación de nombres en tu entorno local, instala el siguiente paquete:

```bash
python -m pip install flake8-naming
```

Ejecución
Para analizar el código, activa tu entorno virtual y ejecuta en la raíz del proyecto:

Bash
flake8 .

## Calidad de Código (Linter)

Este proyecto utiliza **Flake8** junto con el plugin **flake8-naming** para garantizar que todo el código del framework cumpla de manera estricta con las buenas prácticas de Python (PEP 8) y las convenciones oficiales de nomenclatura de variables, clases y funciones.

### Instalación del Plugin de Nomenclatura

Para habilitar la verificación de nombres en tu entorno local, instala el siguiente paquete:

```bash
python -m pip install flake8-naming
```

Si el comando no devuelve ningún mensaje, el código está limpio. De lo contrario, la herramienta reportará los siguientes tipos de error:

| Código | Tipo de Error | Significado Técnico (PEP 8) |
| :--- | :--- | :--- |
| **F401** | *Unused Import* | Librería o módulo importado que no se está utilizando en el archivo. |
| **E501** | *Line Too Long* | Línea que excede el límite máximo de caracteres configurado para el proyecto. |
| **W292** | *No Newline at EOF* | Falta una línea en blanco al final del archivo (End Of File). |
| **W291 / W293** | *Trailing Whitespace* | Espacios en blanco huérfanos o invisibles al final de una línea de código. |
| **N802** | *Function Name Case* | El nombre de una función no está en minúsculas separadas por guiones bajos (*snake_case*). |
| **N803** | *Argument Name Case* | El argumento de una función o método no cumple con el formato *snake_case*. |
| **N806** | *Local Variable Case* | Una variable declarada dentro de una función tiene letras mayúsculas (deben ser *snake_case*). |
| **N801** | *Class Name Case* | El nombre de una clase no sigue el formato de palabras juntas con mayúsculas iniciales (*CamelCase* / *PascalCase*). |

**Ejecutar pruebas filtrando por etiquetas (Tags / Markers):**
El framework permite filtrar ejecuciones usando las etiquetas registradas en `pytest.ini` mediante el flag `-m`.

```bash
# Ejecución genérica por etiqueta
python -m pytest -m <tag_name> -v

# Ejemplos prácticos:
python -m pytest -m smoke -v       
python -m pytest -m negative -v    
python -m pytest -m functional -v  

python -m pytest -m "functional and smoke" -v
```