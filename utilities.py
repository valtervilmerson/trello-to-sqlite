from create_json import WriteJson
from datetime import datetime
import pandas as pd
import numpy as np


def update_cards_list(trello_connection):
    old_list = '626a8cbda5616f41044c21da'
    label_id = '62695479d0676034bae7fdf8'
    new_list = '626a901794eb6b4b4202bda4'

    cards_certification = []
    cards = trello_connection.get_trello_cards()
    for card in cards:
        if card['idList'] == old_list:
            for label in card['idLabels']:
                if label_id in label:
                    cards_certification.append(card['id'])
    print(cards_certification)
    for card_id in cards_certification:
        trello_connection.update_card_id_list(card_id, new_list)

    print('Update_cards completed in ', datetime.now())


def move_cards_list(trello_connection):
    old_list = '626a8cbda5616f41044c21da'
    new_list = '626a901794eb6b4b4202bda4'

    cards = trello_connection.get_trello_cards()
    for card in cards:
        if card['idList'] == old_list:
            trello_connection.update_card_id_list(card['id'], new_list)

    print('Move_card_list completed in ', datetime.now())


def remove_cards_labels(trello_connection):

    print('Remove_labels started at ', datetime.now())

    label_id = '626bbaf4ab76f467e0893a4e'
    id_list = '62388db5b91b032488cea097'

    cards = trello_connection.get_cards_from_list(id_list)

    for card in cards:
        if card['idList'] == id_list:
            trello_connection.delete_card_label(label_id, card['id'])

    print('Remove_labels completed at ', datetime.now())


def create_json(trello_connection):
    actions = trello_connection.get_members_actions()
    print(actions)
    WriteJson.write("teste", actions)


def pandas(conn):
    query = 'SELECT LABEL_NAME, LABEL_ID FROM LABELS'
    result = pd.read_sql_query(query, conn)
    print(result)


def numpy():
    a = []
    for e in 'Teste':
        a.append(e)
    r = np.diag(a)
    print(r)


def fix(trello_connection):
    label_id = '62695479d0676034bae7fdf8'
    id_list = '62388db5b91b032488cea097'

    cards = trello_connection.get_cards_from_list(id_list)

    for card in cards:
        if label_id in card['idLabels']:
            for label in card['idLabels']:
                if label != label_id:
                    trello_connection.delete_card_label(label, card['id'])


def iso_date_to_standard(date):
    print(date)
    formatted = datetime.strptime(date, "%Y-%m-%d").date()
    return formatted
