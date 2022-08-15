import os
from dotenv import load_dotenv
from trello_connection import TrelloConnection
from db_connection import DbConnection
from datetime import datetime
import utilities


def main(db_conn):

    print('Main Started in ', datetime.now())
    execution_id = db_connection.execution_history()

    db_conn.insert_lists()
    db_conn.update_lists()
    db_conn.delete_lists()

    db_conn.insert_cards()
    db_conn.update_cards()
    db_conn.delete_cards()

    db_conn.insert_actions()

    db_conn.insert_cfd()
    db_conn.insert_cfd_priority_order()
    db_conn.delete_cfd_priority_order()
    db_conn.cfd_priority_definition()

    db_conn.insert_labels()
    db_conn.update_labels()

    db_conn.insert_cards_labels(execution_id)
    db_conn.insert_board_state(execution_id)

    print('Main Completed in ', datetime.now())


if __name__ == '__main__':
    load_dotenv()

    trello_connection = TrelloConnection(os.getenv('TRELLO_API_KEY'))
    trello_connection.set_api_token(os.getenv('TRELLO_API_TOKEN'))
    trello_connection.set_board(os.getenv('TRELLO_API_BOARD'))

    db_connection = DbConnection('TRELLO_TECHSALLUS.db', trello_connection, datetime.now())

    main(db_connection)
    # utilities.remove_cards_labels(trello_connection)

    db_connection.close()
