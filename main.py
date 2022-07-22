import json

from trello_connection import TrelloConnection
from db_connection import DbConnection
from datetime import datetime
from create_json import WriteJson

trello_connection = TrelloConnection('ab47763a5af3b88111bbda128e1e5498')
trello_connection.set_api_token('ffd5c4ea8ec16ae8c01258639c3dfe81f9f36adbb397ef2a5923a86a9a0c0a8b')
trello_connection.set_board('62388d998a93181c0fe96d58')


def main():

    db_connection = DbConnection('TRELLO_TECHSALLUS.db')

    db_connection.insert_lists(trello_connection)
    db_connection.update_lists(trello_connection)

    db_connection.insert_cards(trello_connection)
    db_connection.update_cards(trello_connection)

    db_connection.insert_actions(trello_connection)

    db_connection.insert_cfd()
    db_connection.insert_cfd_priority_order()
    db_connection.cfd_priority_definition()

    db_connection.insert_labels(trello_connection)
    db_connection.update_labels(trello_connection)
    db_connection.delete_labels(trello_connection)

    db_connection.insert_cards_labels(trello_connection)


def update_cards():
    list_id = '62388db39989c82d991ce470'
    label_id = '62695479d0676034bae7fdf8'
    new_list = '62388db5b91b032488cea097'

    cards_certification = []
    cards = trello_connection.get_trello_cards()
    for card in cards:
        if card['idList'] == list_id:
            for label in card['idLabels']:
                if label_id in label:
                    cards_certification.append(card['id'])
    print(cards_certification)
    for card_id in cards_certification:
        trello_connection.update_card_id_list(card_id, new_list)


def create_json():
    actions = trello_connection.get_members_actions()
    print(actions)
    WriteJson.write("teste", actions)


if __name__ == '__main__':
    main()
    print('Completed in ', datetime.now())
