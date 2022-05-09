from trello_connection import TrelloConnection
from db_connection import DbConnection


def main():
    trello_connection = TrelloConnection()
    trello_connection.set_key('ab47763a5af3b88111bbda128e1e5498')
    trello_connection.set_token('ffd5c4ea8ec16ae8c01258639c3dfe81f9f36adbb397ef2a5923a86a9a0c0a8b')
    trello_connection.set_board('62388d998a93181c0fe96d58')
    trello_connection.connect()

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
    # db_connection.insert_cards_labels(trello_connection)


if __name__ == '__main__':
    main()
    print('Completed')
