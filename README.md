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

```mermaid
graph TD
    subgraph ROOT["Group_3_Quality_Assurance_III_Test_Automation_Framework"]

        subgraph RAIZ["Archivos Raíz"]
            direction LR
            RF1(["conftest.py"])
            RF2(["pytest.ini"])
            RF3(["requirements.txt"])
            RF4([".env"])
            RF5(["README.md"])
        end

        subgraph CFG["config/"]
            C1(["config.py"])
        end

        subgraph DATA["data/"]
            direction LR
            D1(["issue_data.py"])
            D2(["label_data.py"])
            D3(["repository_data.py"])
            D4(["user_data.py"])
        end

        subgraph SVC["services/"]
            direction LR
            S1(["github_api.py"])
            S2(["github_issues_api.py"])
            S3(["github_labels_api.py"])
            S4(["github_repositories_api.py"])
            S5(["github_user_api.py"])
        end

        subgraph UTL["utils/"]
            U1(["schemas.py"])
        end

        subgraph TST["tests/"]
            direction LR
            subgraph TI["issues/"]
                T1(["test_create_issue.py"])
            end
            subgraph TL["labels/"]
                T2(["test_labels.py"])
            end
            subgraph TR["repositories/"]
                T3(["test_create_repository.py"])
            end
            subgraph TU["users/"]
                direction TB
                T4(["test_get_user.py"])
                T5(["test_hltc18_update_profile.py"])
            end
        end

        subgraph DOC["documentation/"]
            direction LR
            Doc1(["collections/"])
            Doc2(["environments/"])
            Doc3(["reports/"])
            Doc4(["newman-report/"])
            Doc5(["Newman_runner.py"])
        end
    end

    CFG --> |"configuración"| SVC
    SVC --> |"clientes API"| TST
    DATA --> |"test payloads"| TST
    UTL --> |"JSON schemas"| TST
    RAIZ --> |"fixtures"| TST

    classDef configStyle  fill:#dbeafe,stroke:#2563eb,color:#1e3a5f
    classDef dataStyle    fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef serviceStyle fill:#ffedd5,stroke:#ea580c,color:#7c2d12
    classDef testStyle    fill:#fef9c3,stroke:#ca8a04,color:#713f12
    classDef utilStyle    fill:#f3e8ff,stroke:#9333ea,color:#581c87
    classDef docStyle     fill:#f1f5f9,stroke:#64748b,color:#1e293b
    classDef rootStyle    fill:#e0f2fe,stroke:#0369a1,color:#082f49

    class C1 configStyle
    class D1,D2,D3,D4 dataStyle
    class S1,S2,S3,S4,S5 serviceStyle
    class T1,T2,T3,T4,T5 testStyle
    class U1 utilStyle
    class Doc1,Doc2,Doc3,Doc4,Doc5 docStyle
    class RF1,RF2,RF3,RF4,RF5 rootStyle
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