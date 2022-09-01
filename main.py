import os
from dotenv import load_dotenv
from trello_connection import TrelloConnection
from db_connection import DbConnection
from datetime import datetime
import utilities
from db_connection_mysql import MySQLConnection
import pandas


def main(db_conn):

    print('Main Started in ', datetime.now())
    execution_id = db_conn.execution_history()
    print(execution_id)

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

    db_conn.close()

    print('Main Completed in ', datetime.now())


if __name__ == '__main__':
    load_dotenv()

    trello_connection = TrelloConnection(os.getenv('TRELLO_API_KEY'))
    trello_connection.set_api_token(os.getenv('TRELLO_API_TOKEN'))
    trello_connection.set_board(os.getenv('TRELLO_API_BOARD'))

    sqlite = DbConnection(os.getenv('SQLITE3_FILE_PATH'), trello_connection)
    mysql = MySQLConnection(trello_connection)

    main(sqlite)
    main(mysql)

    if datetime.today().isoweekday() == 1:
        utilities.remove_cards_labels(trello_connection)


