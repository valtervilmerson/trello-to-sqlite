from create_json import WriteJson
from datetime import datetime
import pandas as pd
import numpy as np


def update_cards_list(trello_connection):
    old_list = '62388db39989c82d991ce470'
    label_id = '62695479d0676034bae7fdf8'
    new_list = '62388db5b91b032488cea097'

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


def remove_cards_labels(trello_conn):

    label_id = '626bbaf4ab76f467e0893a4e'
    id_list = '62388db5b91b032488cea097'

    cards = trello_conn.get_trello_cards()
    for card in cards:
        if card['idList'] == id_list:
            trello_conn.delete_card_label(label_id, card['id'])

    print('Remove_labels completed in ', datetime.now())


def create_json(trello_connection):
    actions = trello_connection.get_members_actions()
    print(actions)
    WriteJson.write("teste", actions)


def pandas(conn):
    query = 'SELECT * FROM EXECUTION_HISTORY'
    result = pd.read_sql_query(query, conn)
    print(result)

def numpy():
    a = []
    for e in 'Rafael Viado':
        a.append(e)
    r = np.diag(a)
    print(r)
