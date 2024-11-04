from create_json import WriteJson
from datetime import datetime
from pymysql import Error


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


def remove_cards_labels(trello_connection, db_conn, board_id):
    print('Remove_labels started at ', datetime.now())

    list_id_query = "SELECT RULES_TRELLO_OBJECT_ID FROM RULES WHERE RULES_KEY = 'doneList' AND" \
            " RULES_ID_BOARD = '" + board_id + "'"

    label_query = "SELECT RULES_TRELLO_OBJECT_ID FROM RULES WHERE RULES_KEY = 'doneLabel' AND" \
            " RULES_ID_BOARD = '" + board_id + "'"

    cursor = db_conn.connection.cursor()
    try:
        cursor.execute(list_id_query)
        list_id = cursor.fetchall()
        cursor.execute(label_query)
        label_id = cursor.fetchall()
        list_id = list_id[0][0]
        if len(list_id) > 0:
            cards = trello_connection.get_cards_from_list(list_id)
            if len(cards) > 0 and len(label_id) > 0:
                label_id = label_id[0][0]
                for card in cards:
                    if label_id in card['idLabels']:
                        trello_connection.delete_card_label(label_id, card['id'])

    except Error as e:
        print(e)
        return 0




    print('Remove_labels completed at ', datetime.now())


def create_json(trello_connection):
    actions = trello_connection.get_members_actions()
    print(actions)
    WriteJson.write("teste", actions)


def fix(trello_connection):
    label_id = '62695479d0676034bae7fdf8'
    id_list = '62388db5b91b032488cea097'

    cards = trello_connection.get_cards_from_list(id_list)

    for card in cards:
        if label_id in card['idLabels']:
            for label in card['idLabels']:
                if label != label_id:
                    trello_connection.delete_card_label(label, card['id'])


def update_short_link(trello_connection, db_connection):
    cards = trello_connection.get_trello_cards()
    update_cursor = db_connection.connection.cursor()

    for data in cards:
        update_data = (data['shortUrl'], data['id'])
        query = 'UPDATE CARDS SET CARD_SHORT_URL = %s WHERE CARD_ID = %s'
        try:
            update_cursor.execute(query, update_data)
        except:
            print("errooou")
    db_connection.connection.commit()


def iso_date_to_standard(date):
    print(date)
    formatted = datetime.strptime(date, "%Y-%m-%d ").date()
    return formatted
