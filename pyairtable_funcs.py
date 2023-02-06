from pyairtable import Table
import ast
import numpy as np

def load_list_of_clients_to_airtable(list_load_clients,api_key, base_id, table_name):

    table = Table(api_key = api_key,
                  base_id = base_id,
                  table_name = table_name)

    for i in range(len(list_load_clients)):

        table.create({"Name"                    : list_load_clients[i][0],       #Añade a la tabla de Airtable el nombre del cliente
                      "Surname"                 : list_load_clients[i][1],       #Añade a la tabla de Airtable el apellido del cliente
                      "Calories"                : str(list_load_clients[i][2]),  #Añade a la tabla de Airtable las calorías deseadas del cliente
                      "Days of the menu"        : str(list_load_clients[i][3]),  #Añade a la tabla de Airtable los días que el cliente quiere recibir menú
                      "Diet"                    : list_load_clients[i][4],       #Añade a la tabla de Airtable la dieta escogida del cliente
                      "Excluded ingredients"    : list_load_clients[i][5],       #Añade a la tabla de Airtable los ingredientes excluidos del cliente
                      "Address"                 : list_load_clients[i][6],      #Añade a la tabla de Airtable la dirección del cliente
                      "ID"                      : list_load_clients[i][7]})      #Añade a la tabla de Airtable el ID del cliente
    return

def load_client_to_airtable(load_client,api_key, base_id, table_name):

    table = Table(api_key = api_key,
                  base_id = base_id,
                  table_name = table_name)


    table.create({"Name"                    : load_client[0],       #Añade a la tabla de Airtable el nombre del cliente
                  "Surname"                 : load_client[1],       #Añade a la tabla de Airtable el apellido del cliente
                  "Calories"                : str(load_client[2]),  #Añade a la tabla de Airtable las calorías deseadas del cliente
                  "Days of the menu"        : str(load_client[3]),  #Añade a la tabla de Airtable los días que el cliente quiere recibir menú
                  "Diet"                    : load_client[4],       #Añade a la tabla de Airtable la dieta escogida del cliente
                  "Excluded ingredients"    : load_client[5],       #Añade a la tabla de Airtable los ingredientes excluidos del cliente
                  "Address"                 : load_client[6],       #Añade a la tabla de Airtable la dirección del cliente
                  "ID"                      : load_client[7]})      #Añade a la tabla de Airtable el ID del cliente
    return

def extract_all_clients_from_airtable(api_key, base_id, table_name):

    table = Table(api_key = api_key,
                  base_id = base_id,
                  table_name = table_name)

    records = table.all()

    airtable_clients = []

    for record in records:

        airtable_clients.append([record["fields"]["Name"],                 #Añade a la lista el nombre del cliente
                                 record["fields"]["Surname"],              #Añade a la lista el apellido del cliente
                                 record["fields"]["Calories"],             #Añade a la lista las calorías deseadas del cliente
                                 record["fields"]["Days of the menu"],     #Añade a la lista los días que el cliente quiere recibir menú
                                 record["fields"]["Diet"],                 #Añade a la lista la dieta escogida del cliente
                                 record["fields"]["Excluded ingredients"], #Añade a la lista los ingredientes excluidos del cliente
                                 record["fields"]["Address"],              #Añade a la lista la dirección del cliente
                                 record["fields"]["ID"]])                  #Añade a la lista el ID del cliente
    return airtable_clients


def extract_client_from_airtable(client_id, api_key, base_id, table_name):

    table = Table(api_key = api_key,
                  base_id = base_id,
                  table_name = table_name)

    records = table.all()

    for record in records:

        if record["fields"]["ID"] == str(client_id):

            client_info = [record["fields"]["Name"],
                          record["fields"]["Surname"],
                          record["fields"]["Calories"],
                          ast.literal_eval(record["fields"]["Days of the menu"]),
                          record["fields"]["Diet"],
                          record["fields"]["Excluded ingredients"],
                          record["fields"]["Address"],
                          record["fields"]["ID"]]

    return client_info

def return_max_id(api_key, base_id, table_name):

    table = Table(api_key = api_key,
                  base_id = base_id,
                  table_name = table_name)

    records = table.all()

    list_records = []

    for record in records:

        list_records.append(int(record["fields"]["ID"]))

    max_id = np.max(list_records)

    return max_id


def delete_all_records(api_key, base_id, table_name):

    table = Table(api_key = api_key,
                  base_id = base_id,
                  table_name = table_name)

    records = table.all()
    list_ids = []

    for record in records:

        list_ids.append(record["id"])

    table.batch_delete(list_ids)

    return
