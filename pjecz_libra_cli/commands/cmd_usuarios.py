"""
Command Usuarios
"""

import os
import sys

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
def consultar():
    """Consultar usuarios"""
    click.echo("Consultando usuarios")

    # Validar HERCULES_API_BASE_URL
    if HERCULES_API_BASE_URL is None:
        click.echo(click.style("FALTA: La variable de entorno HERCULES_API_BASE_URL", fg="red"))
        sys.exit(1)

    # Validar HERCULES_API_KEY
    if HERCULES_API_KEY is None:
        click.echo(click.style("FALTA: La variable de entorno HERCULES_API_KEY", fg="red"))
        sys.exit(1)

    # Inicializar el limit y el offset para hacer la paginación
    limit = None
    offset = 0

    # Bucle para hacer la paginación
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
            click.echo(usuario["email"])

        # Definir el limit
        limit = datos["limit"]
        offset += limit

        # Si el offset sobrepasa el total, salir del bucle
        if offset >= datos["total"]:
            break

    # Mensaje final
    click.echo()
    click.echo(click.style("Termina la consulta", fg="green"))


cli.add_command(consultar)
