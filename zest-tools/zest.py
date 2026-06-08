# mon_outil.py
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument("nom")
def saluer(nom):
    click.echo(f"Bonjour {nom} !")

@cli.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def additionner(a, b):
    click.echo(f"{a} + {b} = {a + b}")

