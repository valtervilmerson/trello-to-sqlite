from create_json import WriteJson


def update_cards_list(trello_connection):
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


def delete_labels(trello_connection):
    id_label = '626bbaf4ab76f467e0893a4e'
    cards = trello_connection.get_trello_cards()
    for card in cards:
        if card['idList'] == '62388db5b91b032488cea097':
            trello_connection.delete_card_label(id_label, card['id'])


def create_json(trello_connection):
    actions = trello_connection.get_members_actions()
    print(actions)
    WriteJson.write("teste", actions)