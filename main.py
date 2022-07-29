import os
from dotenv import load_dotenv
from trello_connection import TrelloConnection
from db_connection import DbConnection
from datetime import datetime


def main(connection):
    db_connection = DbConnection('TRELLO_TECHSALLUS.db', datetime.now())
    execution_id = 0
    execution_id = db_connection.execution_history()

    db_connection.insert_lists(connection)
    db_connection.update_lists(connection)
    db_connection.delete_lists(connection)

    db_connection.insert_cards(connection)
    db_connection.update_cards(connection)
    db_connection.delete_cards(connection)

    db_connection.insert_actions(connection)

    db_connection.insert_cfd()
    db_connection.insert_cfd_priority_order()
    db_connection.delete_cfd_priority_order(connection)
    db_connection.cfd_priority_definition()

    db_connection.insert_labels(connection)
    db_connection.update_labels(connection)

    db_connection.insert_cards_labels(connection, execution_id)
    db_connection.insert_board_state(connection, execution_id)

    db_connection.close()


if __name__ == '__main__':
    load_dotenv()

    trello_connection = TrelloConnection(os.getenv('TRELLO_API_KEY'))
    trello_connection.set_api_token(os.getenv('TRELLO_API_TOKEN'))
    trello_connection.set_board(os.getenv('TRELLO_API_BOARD'))

    print('Started in ', datetime.now())
    main(trello_connection)
    print('Completed in ', datetime.now())
