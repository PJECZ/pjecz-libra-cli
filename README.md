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
pip install --upgrade pip setuptools wheel poetry
```

Crear un archivo para las variables de entorno

```bash
nano .env
```

Escriba las siguientes variables cambiándolas a sus requerimientos

```ini
```

Instalar en este entorno el comando `hercules`

```bash
pip install --editable .
```

Probar que funcione el CLI

```bash
hercules --help
```
