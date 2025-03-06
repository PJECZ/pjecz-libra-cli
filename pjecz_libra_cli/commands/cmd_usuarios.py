"""
Command Usuarios
"""

import csv
import os
import sys
from pathlib import Path

import click
from dotenv import load_dotenv
import requests

load_dotenv()
HERCULES_API_BASE_URL = os.getenv("HERCULES_API_BASE_URL")
HERCULES_API_KEY = os.getenv("HERCULES_API_KEY")
LIMIT = int(os.getenv("LIMIT", "10"))
TIMEOUT = int(os.getenv("TIMEOUT", "30"))


@click.group()
def cli():
    """Usuarios"""


@click.command()
@click.option("--output", default="usuarios.csv", type=str, help="Nombre del archivo CSV a crear")
def consultar(output):
    """Consultar usuarios"""
    click.echo("Consultando usuarios: ", nl=False)

    # Validar HERCULES_API_BASE_URL
    if HERCULES_API_BASE_URL is None:
        click.echo(click.style("FALTA: La variable de entorno HERCULES_API_BASE_URL", fg="red"))
        sys.exit(1)

    # Validar HERCULES_API_KEY
    if HERCULES_API_KEY is None:
        click.echo(click.style("FALTA: La variable de entorno HERCULES_API_KEY", fg="red"))
        sys.exit(1)

    # Inicializar listado de usuarios
    usuarios = []

    # Bucle para hacer la paginación
    offset = 0
    while True:
        # Consultar a Hercules API Key
        try:
            respuesta = requests.get(
                f"{HERCULES_API_BASE_URL}/usuarios",
                headers={"X-Api-Key": HERCULES_API_KEY},
                params={"limit": LIMIT, "offset": offset},
                timeout=TIMEOUT,
            )
            respuesta.raise_for_status()
        except requests.exceptions.ConnectionError:
            click.echo(click.style("ERROR: No hubo respuesta de la API", fg="red"))
            sys.exit(1)
        except requests.exceptions.HTTPError as error:
            click.echo(click.style("ERROR: Status Code con error: " + str(error), fg="red"))
            sys.exit(1)
        except requests.exceptions.RequestException:
            click.echo(click.style("ERROR: Error desconocido", fg="red"))
            sys.exit(1)

        # Convertir la respuesta a JSON
        datos = respuesta.json()

        # Validar que haya 'success'
        if "success" not in datos:
            click.echo(click.style("ERROR: No tiene 'success'", fg="red"))
            sys.exit(1)

        # Validar que 'success' sea True
        if datos["success"] is False:
            click.echo(click.style("FALLO: ", fg="yellow"))
            if "message" in datos:
                click.echo(click.style(datos["message"], fg="yellow"))
            sys.exit(1)

        # Validar que haya 'data'
        if len(datos["data"]) == 0:
            click.echo(click.style("FALLO: No hay 'data' en la respuesta", fg="yellow"))
            sys.exit(1)

        # Bucle entre los usuarios
        for usuario in datos["data"]:
            usuarios.append(
                [
                    usuario["email"],
                    usuario["nombres"],
                    usuario["apellido_paterno"],
                    usuario["apellido_materno"],
                ]
            )
            click.echo(".", nl=False)

        # Tomar el limit e incrementar el offset
        limit = datos["limit"]
        offset += limit

        # Si el offset sobrepasa el total, salir del bucle
        if offset >= datos["total"]:
            break

    # Si se dio output
    if output:
        # Si existe el archivo, eliminarlo
        ruta = Path(output)
        if ruta.is_file():
            ruta.unlink()

        # Escribir
        with open(ruta, "w", encoding="utf8") as puntero:
            archivo_csv = csv.writer(puntero)
            archivo_csv.writerow(["email", "nombres", "apellido_paterno", "apellido_materno"])
            archivo_csv.writerows(usuarios)

    # Mensaje final
    click.echo()
    click.echo(click.style(f"Termina la consulta con {len(usuarios)} usuarios", fg="green"))


cli.add_command(consultar)
