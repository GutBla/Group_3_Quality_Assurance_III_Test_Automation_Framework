# Group_3_Quality_Assurance_III_Test_Automation_Framework
API automation testing framework using Python and Pytest

Tecnologías utilizadas

Python 3.14+

Pytest

Requests

JSONSchema

python-dotenv

GitHub REST API

Instalación

1. Clonar el repositorio

git clone <URL_DEL_REPO>

cd Group_3_Quality_Assurance_III_Test_Automation_Framework

2. Crear entorno virtual

python3 -m venv venv

source venv/bin/activate

3. Instalar dependencias

pip install -r requirements.txt

Configuración del proyecto



Crear un archivo .env en la raíz del proyecto:



BASE_URL=https://api.github.com

USERNAME=tu_usuario_github

REPO=tu_repositorio

TOKEN=tu_github_token

Estructura del proyecto

Group_3_Quality_Assurance_III_Test_Automation_Framework/

│

├── config/

│   └── config.py              # Variables de entorno y configuración

│

├── data/

│   └── issue_data.py         # Payloads de pruebas

│

├── services/

│   └── github_issues_api.py  # API Client (Requests wrapper)

│

├── tests/

│   ├── issues/

│   │   └── test_create_issue.py

│   └── users/

│       └── test_get_user.py

│

├── utils/

│   └── schemas.py            # JSON Schemas para validación

│

├── conftest.py               # Fixtures globales (setup/teardown)

│

├── pytest.ini

└── requirements.txt

Cómo ejecutar las pruebas



Ejecutar todos los tests:



pytest -v



Ejecutar un archivo específico:



pytest tests/issues/test_create_issue.py -v