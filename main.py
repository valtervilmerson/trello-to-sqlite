import os
from dotenv import load_dotenv
from trello_connection import TrelloConnection
from datetime import datetime
import utilities
from db_connection_mysql import MySQLConnection


def main(db_conn):
    print('Main Started at ', datetime.now())

    execution_id = db_conn.insert_execution_history()

    db_conn.insert_lists()
    db_conn.update_lists()
    db_conn.close_lists()

    db_conn.insert_cards()
    db_conn.update_cards()
    db_conn.close_cards()

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
    if datetime.today().isoweekday() == 1:
        utilities.remove_cards_labels(trello)
    else:
        print('Remove_cards_labels é executado apenas nas segundas-feiras')


def insert_all_board_actions(trello_conn, db_conn):
    print('insert_all_board_actions Started at', datetime.now())
    bypass = False
    if datetime.today().isoweekday() == 1 or bypass == True:

        all_actions = trello_conn.get_all_board_actions_formatted()
        db_conn.insert_all_actions(all_actions)
    else:
        print('insert_all_board_actions é executado apenas nas segundas-feiras')
    print('insert_all_board_actions done at', datetime.now())


def get_active_boards(conn):
    boards = conn.get_active_boards()
    sanitazed_boards = [x[0] for x in boards]
    return sanitazed_boards


if __name__ == '__main__':
    load_dotenv()

    trello_connection = TrelloConnection(os.getenv('TRELLO_API_KEY'))
    trello_connection.set_api_token(os.getenv('TRELLO_API_TOKEN'))
    mysql = MySQLConnection(trello_connection)
    active_boards = get_active_boards(mysql)
    if len(active_boards) > 0:
        for board in active_boards:
            trello_connection.set_board(board)
            main(mysql)
    insert_all_board_actions(trello_connection, mysql)
    remove_cards_labels(trello_connection)
    mysql.close()
