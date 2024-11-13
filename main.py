from trello_connection import TrelloConnection
from datetime import datetime
import utilities
from db_connection_mysql import MySQLConnection
from configuration.common import ConfigurationBuilder
from configuration.toml import TOMLFile
from configuration.env import EnvVars

builder = ConfigurationBuilder(
    TOMLFile("C:/trello-techsallus/settings.toml"),
    EnvVars(prefix="APP_")
)

config = builder.build()


def main(db_conn):
    print('Main Started at ', datetime.now())

    execution_id = db_conn.insert_execution_history()

    db_conn.insert_lists()
    db_conn.update_lists()
    db_conn.close_lists()

    db_conn.insert_cards()
    db_conn.update_cards()
    db_conn.close_cards()

    # TODO fix collation for dev database
    db_conn.insert_cfd()
    db_conn.insert_cfd_priority_order()
    db_conn.delete_cfd_priority_order()
    db_conn.cfd_priority_definition()

    db_conn.insert_labels()
    db_conn.update_labels()
    db_conn.close_labels()

    db_conn.insert_db_members()

    db_conn.insert_cards_labels(execution_id)
    db_conn.insert_cards_members(execution_id)
    db_conn.insert_board_state(execution_id)

    db_conn.insert_done_list()
    db_conn.update_execution_history(execution_id)

    print('Main Completed at ', datetime.now())


def remove_cards_labels(trello, db_conn, board_id, bypass=False):
    # TODO create a condition to check if the routine has already been executed on mondays
    if datetime.today().isoweekday() == 1 or bypass:
        utilities.remove_cards_labels(trello, db_conn, board_id)
    else:
        print('Remove_cards_labels é executado apenas nas segundas-feiras')


def insert_all_board_actions(trello_conn, db_conn):
    print('insert_all_board_actions Started at', datetime.now())
    bypass = False
    if datetime.today().isoweekday() == 1 or bypass:
        all_actions = trello_conn.get_all_board_actions_formatted()
        all_actions_ids = [actionId['id'] for actionId in all_actions]
        exclusive_actions = db_conn.get_exclusive_actions(all_actions_ids)
        if len(exclusive_actions) > 0:
            exclusive = [x for x in all_actions if x['id'] in exclusive_actions]
            db_conn.insert_exclusive_actions(exclusive)
    else:
        print('insert_all_board_actions é executado apenas nas segundas-feiras')
    print('insert_all_board_actions done at', datetime.now())


def get_active_boards(conn):
    boards = conn.get_active_boards()
    sanitized_boards = [x[0] for x in boards]
    return sanitized_boards


if __name__ == '__main__':

    trello_connection = TrelloConnection(config.trello.TRELLO_API_KEY)
    trello_connection.set_api_token(config.trello.TRELLO_API_TOKEN)

    mysql = MySQLConnection(trello_connection, config)

    active_boards = get_active_boards(mysql)
    if len(active_boards) > 0:
        for board in active_boards:
            trello_connection.set_board(board)
            main(mysql)
            insert_all_board_actions(trello_connection, mysql)
            remove_cards_labels(trello_connection, mysql, board)
    mysql.close()
