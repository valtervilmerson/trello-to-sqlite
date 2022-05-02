import sqlite3
from sqlite3 import Error
import datetime


class DbConnection:

    def __init__(self, db_file):
        self.database = db_file
        self.connection = None
        try:
            self.connection = sqlite3.connect(self.database)
        except Error as e:
            print(e)

    def get_db_lists(self):
        query = 'SELECT LIST_ID FROM LISTS ORDER BY LIST_POS DESC'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_lists = cursor.fetchall()
            return db_lists
        except Error as e:
            print(e)
            return e

    def get_db_cards_ids(self):
        query = 'SELECT CARD_ID FROM CARDS'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_cards = cursor.fetchall()
            return db_cards
        except Error as e:
            print(e)
            return e

    def get_db_board_actions_ids(self):
        query = 'SELECT ACTION_ID FROM ACTIONS'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_actions = cursor.fetchall()
            return db_actions
        except Error as e:
            print(e)
            return e

    def insert_list(self, trello_connection):

        sanitized_db_lists_ids = []
        exclusive_lists = []
        inserted_rows = []

        trello_lists = trello_connection.get_trello_lists()
        db_lists_ids = self.get_db_lists()

        for item in db_lists_ids:
            sanitized_db_lists_ids.append(item[0])

        for data_id in trello_lists:
            if data_id['id'] not in sanitized_db_lists_ids:
                exclusive_lists.append(data_id)

        cursor = self.connection.cursor()

        for data in exclusive_lists:
            insert_data = (data['id'], data['name'], data['closed'], data['idBoard'], data['pos'])
            query = 'INSERT INTO LISTS (LIST_ID, LIST_NAME ,LIST_CLOSED, LIST_ID_BOARD, LIST_POS) VALUES (?, ?, ?,' \
                    '?, ?)'
            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        return inserted_rows

    def insert_cards(self, trello_connection):
        sanitized_db_cards_ids = []
        exclusive_cards = []
        inserted_rows = []

        trello_cards = trello_connection.get_trello_cards()
        db_cards_ids = self.get_db_cards_ids()

        for item in db_cards_ids:
            sanitized_db_cards_ids.append(item[0])

        for data_id in trello_cards:
            if data_id['id'] not in sanitized_db_cards_ids:
                exclusive_cards.append(data_id)

        cursor = self.connection.cursor()

        for data in exclusive_cards:
            insert_data = (data['id'], data['name'], data['closed'], data['dateLastActivity'], data['idBoard'],
                           data['pos'], data['idList'],
                           data['desc'], data['cover']['color'], data['isTemplate'], data['due'])
            query = 'INSERT INTO CARDS (CARD_ID, CARD_NAME, CARD_CLOSED, CARD_DATE_LAST_ACTIVITY, CARD_ID_BOARD,' \
                    'CARD_POS, CARD_ID_LIST, CARD_DESC, CARD_COVER_COLOR, CARD_IS_TEMPLATE, CARD_DUE)' \
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        return inserted_rows

    def insert_actions(self, trello_connection):

        sanitized_db_actions_ids = []
        exclusive_actions = []
        inserted_rows = []

        trello_actions = trello_connection.get_trello_board_actions()
        db_actions_ids = self.get_db_board_actions_ids()

        for item in db_actions_ids:
            sanitized_db_actions_ids.append(item[0])

        for data_id in trello_actions:
            if data_id['id'] not in sanitized_db_actions_ids:
                exclusive_actions.append(data_id)

        cursor = self.connection.cursor()
        for data in exclusive_actions:
            if 'listBefore' in data['data']:
                insert_data = (data['id'], data['idMemberCreator'], data['data']['card']['id'],
                               data['data']['board']['id'], data['data']['listBefore']['id'],
                               data['data']['listAfter']['id'], data['type'], data['date'])
                query = 'INSERT INTO ACTIONS (ACTION_ID, ACTION_ID_MEMBER_CREATOR ,ACTION_CARD_ID, ACTION_BOARD_ID,' \
                        'ACTION_LIST_BEFORE, ACTION_LIST_AFTER, ACTION_TYPE, ACTION_DATE)' \
                        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                try:
                    cursor.execute(query, insert_data)
                    inserted_rows.append(cursor.lastrowid)
                except Error as e:
                    print(e)
                    return e
        self.connection.commit()
        return inserted_rows

    def insert_cfd(self):
        inserted_rows = []
        query = 'INSERT INTO CFD (CFD_LIST_ID, CFD_TOTAL_CARDS, CFD_PROCESSING_DATE)' \
                'SELECT ' \
                'LIST_ID AS CFD_LIST_NAME' \
                ',COUNT (CARD_ID) AS CFD_TOTAL_TASKS' \
                ',DATETIME("NOW") AS CFD_PROCESSING_DATE ' \
                'FROM ' \
                'CARDS ' \
                'INNER JOIN LISTS ON LIST_ID = CARD_ID_LIST ' \
                'GROUP BY ' \
                'LIST_NAME' \
                ',LIST_CREATE_DATE'

        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            self.connection.commit()
            inserted_rows.append(cursor.lastrowid)
        except Error as e:
            print(e)
            return e

    def insert_cfd_priority_order(self):

        inserted_rows = []
        query = 'INSERT INTO CFD_PRIORITY_ORDER (PRIORITY_ID_LIST, PRIORITY_ORDER) ' \
                'SELECT ' \
                'LIST_ID' \
                ',0 ' \
                'FROM ' \
                'LISTS ' \
                'WHERE ' \
                'LIST_ID NOT IN (SELECT PRIORITY_ID_LIST FROM CFD_PRIORITY_ORDER)'

        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            self.connection.commit()
            inserted_rows.append(cursor.lastrowid)
        except Error as e:
            print(e)
            return e

    def update_lists(self, trello_connection):

        trello_lists_update = trello_connection.get_trello_lists()

        update_cursor = self.connection.cursor()
        current_time = datetime.datetime.now()

        for data in trello_lists_update:
            update_data = (data['name'], data['closed'], data['pos'], current_time, data['id'])
            query = 'UPDATE LISTS SET LIST_NAME = ? ,LIST_CLOSED = ?, LIST_POS = ?, ' \
                    'LIST_LAST_MODIFIED = ? WHERE LIST_ID = ?'
            try:
                update_cursor.execute(query, update_data)
            except Error as e:
                print(e)
                return e
        self.connection.commit()

    def update_cards(self, trello_connection):

        trello_cards_update = trello_connection.get_trello_cards()

        update_cursor = self.connection.cursor()
        current_time = datetime.datetime.now()

        for data in trello_cards_update:
            update_data = (data['name'], data['closed'], data['dateLastActivity'], data['idBoard'], data['pos'],
                           data['idList'], data['desc'], data['cover']['color'], data['isTemplate'], data['due'],
                           current_time, data['id'])
            query = 'UPDATE CARDS SET CARD_NAME = ? ,CARD_CLOSED = ?, CARD_DATE_LAST_ACTIVITY = ?, CARD_ID_BOARD = ?,' \
                    'CARD_POS = ?, CARD_ID_LIST = ?, CARD_DESC = ?, CARD_COVER_COLOR = ?, CARD_IS_TEMPLATE = ?,' \
                    'CARD_DUE = ?, CARD_LAST_MODIFIED = ? WHERE CARD_ID = ?'
            try:
                update_cursor.execute(query, update_data)
            except Error as e:
                print(e)
                return e
        self.connection.commit()

    def cfd_priority_definition(self):
        query = 'UPDATE CFD_PRIORITY_ORDER SET PRIORITY_ORDER = ?, PRIORITY_LIST_NAME = ? || " - " || LIST_NAME ' \
                'FROM ' \
                'LISTS ' \
                'WHERE LIST_ID = PRIORITY_ID_LIST AND PRIORITY_ID_LIST = ?'
        db_lists = self.get_db_lists()
        cursor = self.connection.cursor()
        counter = 0
        for data in db_lists:
            update_data = (counter, counter, data[0])
            try:
                cursor.execute(query, update_data)
            except Error as e:
                print(e)
                return e
            counter = counter + 1
        self.connection.commit()

    def close(self):
        self.connection.close()
