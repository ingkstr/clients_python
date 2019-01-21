import click
from clients.services import ClienteService
from clients.models import ClienteModel

@click.group()
def clientes():
    """Administra los clientes"""
    pass


@clientes.command()
@click.option('-n','--name',
              type=str,
              prompt=True,
              help='Client name')
@click.option('-c','--company',
              type=str,
              prompt=True,
              help='Client company')
@click.option('-e','--email',
              type=str,
              prompt=True,
              help='Client email')
@click.option('-P','--position',
              type=str,
              prompt=True,
              help='Client position')
@click.pass_context
def create(ctx, name, company, email, position):
    """Crear un nuevo cliente"""
    client = ClienteModel(name, company, email, position)
    client_service = ClienteService(ctx.obj['clients_table'])
    client_service.create_client(client)

@clientes.command()
@click.pass_context
def list(ctx):
    """Enlista los clientes"""
    client_service = ClienteService(ctx.obj['clients_table'])
    clients_list = client_service.list_clients()
    click.echo('  ID  |  NAME  |  COMPANY  |  EMAIL  |  POSITION')
    click.echo('*'*100)
    for client in clients_list:
        click.echo('  {}  |  {}  |  {}  |  {}  |  {}'.format(client['uid'],client['name'], client['company'], client['email'], client['position']))


@clientes.command()
@click.argument('client_uid',
              type=str)
@click.pass_context
def update(ctx, client_uid):
    """Actualiza el client"""
    client_service = ClienteService(ctx.obj['clients_table'])
    client_list = client_service.list_clients()
    client = [client for client in client_list if client['uid'] == client_uid]
    if client:
            ##Desmpaqueta el diccionario al modelo de ClientModel
            client = _update_client_flow(ClienteModel(**client[0]))
            client_service.update_clients(client)
            click.echo('Client updated')
    else:
            click.echo('ID not in list')

def _update_client_flow(client):
    client.name = click.prompt('New name', type=str, default=client.name)
    client.company = click.prompt('New company', type=str, default=client.company)
    client.email = click.prompt('New email', type=str, default=client.email)
    client.position = click.prompt('New position', type=str, default=client.position)
    return client


@clientes.command()
@click.argument('client_uid',
              type=str)
@click.pass_context
def delete(ctx, client_uid):
    """Elimina un cliente"""
    client_service = ClienteService(ctx.obj['clients_table'])
    client_list = client_service.list_clients()
    client = [client for client in client_list if client['uid'] == client_uid]
    if client:
            ##Desmpaqueta el diccionario al modelo de ClientModel
            client = ClienteModel(**client[0])
            client_service.delete_client(client)
            click.echo('Client deleted')
    else:
            click.echo('ID not in list')


all = clientes
