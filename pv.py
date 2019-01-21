import click
from clients import commands as clients_commands

CLIENTS_TABLE =  '.clients.csv'

@click.group()
@click.pass_context
def cli(ctx):
    #Contexto tiene todo los parametros globales en un diccionario
    ctx.obj = {}
    ctx.obj['clients_table'] = CLIENTS_TABLE

cli.add_command(clients_commands.all)
