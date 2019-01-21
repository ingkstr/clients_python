import csv
import os

from clients.models import ClienteModel

class ClienteService:
    def __init__(self,table_name):
            self.table_name = table_name

    def create_client(self, clientemodel):
        with open(self.table_name, mode='a') as f:
            writer = csv.DictWriter(f, fieldnames=ClienteModel.schema())
            writer.writerow(clientemodel.to_dict())

    def list_clients(self):
        with open(self.table_name, mode='r') as f:
            reader = csv.DictReader(f, fieldnames=ClienteModel.schema())
            return list(reader)

    def update_clients(self, updated_client):
        clients = self.list_clients()
        updated_clients =[]
        for client in clients:
            if client['uid'] == updated_client.uid:
                updated_clients.append(updated_client.to_dict())
            else:
                updated_clients.append(client)
        self._save_to_disk(updated_clients)

    def delete_client(self, client_removed):
        clients = self.list_clients()
        for client in clients:
            if client['uid'] == client_removed.uid:
                clients.remove(client)
        self._save_to_disk(clients)

    def _save_to_disk(self,clients):
        tmp_table_name = '{}.tmp'.format(self.table_name)
        with open(tmp_table_name, mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=ClienteModel.schema())
            writer.writerows(clients)
        os.remove(self.table_name)
        os.rename(tmp_table_name, self.table_name)
