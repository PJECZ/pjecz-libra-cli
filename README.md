# pjecz-libra-cli

CLI (Command Line Interface) para actualizar las bases de datos a partir de una API en el servidor Neptuno.

## Instalación

Crear el entorno virtual con **Python 3.11**

```bash
python3.11 -m venv .venv
```

Ingresar al entorno virtual

```bash
. .venv/bin/activate
```

Actualizar e instalar **poetry 2**

```bash
pip install --upgrade pip 
pip install --upgrade setuptools
pip install wheel
pip install poetry
```

Crear un archivo para las variables de entorno

```bash
nano .env
```

Instalar el CLI

```bash
poetry install
```

Escriba las siguientes variables cambiándolas a sus requerimientos

```ini
# Hercules API Key
HERCULES_API_BASE_URL="https://datos.XXXXXXXXXXXX.gob.mx/api/v5"
HERCULES_API_KEY="XXXXXXXX.XXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXX"
LIMIT=10
TIMEOUT=30
```

Ejecutar el CLI

```bash
cli --help
```
