import os
from dotenv import load_dotenv
from trello_connection import TrelloConnection
from datetime import datetime
import utilities
from db_connection_mysql import MySQLConnection


def main(db_conn):

    print('Main Started at ', datetime.now())

    execution_id = db_conn.execution_history()

    db_conn.insert_lists()
    db_conn.update_lists()
    db_conn.delete_lists()

    db_conn.insert_cards()
    db_conn.update_cards()

    db_conn.insert_cfd()
    db_conn.insert_cfd_priority_order()
    db_conn.delete_cfd_priority_order()
    db_conn.cfd_priority_definition()

    db_conn.insert_labels()
    db_conn.update_labels()

    db_conn.insert_db_members()

    db_conn.insert_cards_labels(execution_id)
    db_conn.insert_board_state(execution_id)

    print('Main Completed at ', datetime.now())


def remove_cards_labels(trello):
    print('Remove_cards Started at ', datetime.now())
    if datetime.today().isoweekday() == 1:
        utilities.remove_cards_labels(trello)
    else:
        print('Executado apenas nas segundas-feiras')
    print('Remove_cards Completed at ', datetime.now())


def insert_all_board_actions(trello_conn, db_conn):
    if datetime.today().isoweekday() == 1:
        print('insert_all_board_actions Started at', datetime.now())
        all_actions = trello_conn.get_all_board_actions_formatted()
        db_conn.insert_all_actions(all_actions)
        print('insert_all_board_actions done at', datetime.now())
    else:
        print('Executado apenas nas segundas-feiras')


if __name__ == '__main__':
    load_dotenv()

    trello_connection = TrelloConnection(os.getenv('TRELLO_API_KEY'))
    trello_connection.set_api_token(os.getenv('TRELLO_API_TOKEN'))
    trello_connection.set_board(os.getenv('TRELLO_API_BOARD'))

    mysql = MySQLConnection(trello_connection)
    insert_all_board_actions(trello_connection, mysql)
    main(mysql)

    remove_cards_labels(trello_connection)

    mysql.close()

