import sqlite3
from sqlite3 import Error
from datetime import datetime
from dateutil import parser


class DbConnection:

    def __init__(self, db_file, trello_conn):
        self.database = db_file
        self.connection = None
        self.execution_time = datetime.now()
        self.trello_connection = trello_conn
        try:
            self.connection = sqlite3.connect(self.database)
        except Error as e:
            print(e)

    def get_db_cards_labels(self):
        query = 'SELECT CL_CARD_ID, CL_LABEL_ID FROM CARDS_LABELS'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_response = cursor.fetchall()
            return db_response
        except Error as e:
            print(e)
            return 0

    def get_db_lists(self):
        query = 'SELECT LIST_ID FROM LISTS ORDER BY LIST_POS DESC'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_lists = cursor.fetchall()
            return db_lists
        except Error as e:
            print(e)
            return 0

    def get_db_labels_ids(self):
        query = 'SELECT LABEL_ID FROM LABELS'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_labels = cursor.fetchall()
            return db_labels
        except Error as e:
            print(e)
            return 0

    def get_db_cards_ids(self):
        query = 'SELECT CARD_ID FROM CARDS'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_cards = cursor.fetchall()
            return db_cards
        except Error as e:
            print(e)
            return 0

    def get_db_board_actions_ids(self):
        query = 'SELECT ACTION_ID FROM ACTIONS'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_actions = cursor.fetchall()
            return db_actions
        except Error as e:
            print(e)
            return 0

    def get_cfd_priority_list(self):
        query = 'SELECT PRIORITY_ID_LIST FROM CFD_PRIORITY_ORDER'
        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            db_cfd_list = cursor.fetchall()
            return db_cfd_list
        except Error as e:
            print(e)
            return 0

    def insert_lists(self):
        inserted_rows = []

        trello_lists = self.trello_connection.get_trello_lists()
        db_lists_ids = self.get_db_lists()

        sanitized_db_lists_ids = [x[0] for x in db_lists_ids]
        exclusive_lists = [x for x in trello_lists if x['id'] not in sanitized_db_lists_ids]

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

    def insert_cards(self):
        inserted_rows = []

        trello_cards = self.trello_connection.get_trello_cards()
        db_cards_ids = self.get_db_cards_ids()

        sanitized_db_cards_ids = [x[0] for x in db_cards_ids]
        exclusive_cards = [x for x in trello_cards if x['id'] not in sanitized_db_cards_ids]

        cursor = self.connection.cursor()

        for data in exclusive_cards:
            insert_data = (data['id'], data['name'], data['closed'], data['dateLastActivity'], data['idBoard'],
                           data['pos'], data['idList'],
                           data['desc'], data['cover']['color'], data['isTemplate'], data['idShort'], data['due'])
            query = 'INSERT INTO CARDS (CARD_ID, CARD_NAME, CARD_CLOSED, CARD_DATE_LAST_ACTIVITY, CARD_ID_BOARD,' \
                    'CARD_POS, CARD_ID_LIST, CARD_DESC, CARD_COVER_COLOR, CARD_IS_TEMPLATE, CARD_ID_SHORT, CARD_DUE)' \
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        return inserted_rows

    def insert_actions(self):
        inserted_rows = []

        trello_actions = self.trello_connection.get_trello_board_actions()
        db_actions_ids = self.get_db_board_actions_ids()

        sanitized_db_actions_ids = [x[0] for x in db_actions_ids]
        exclusive_actions = [x for x in trello_actions if x['id'] not in sanitized_db_actions_ids]

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
                    self.connection.commit()
                    inserted_rows.append(cursor.lastrowid)
                except Error as e:
                    print(e)
                    return e

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

    def delete_cfd_priority_order(self):

        trello_lists = self.trello_connection.get_trello_lists()
        cfd_lists = self.get_cfd_priority_list()

        trello_lists_ids = [x['id'] for x in trello_lists]
        sanitized_db_cfd_ids = [x[0] for x in cfd_lists]
        exclusive_lists = [x for x in sanitized_db_cfd_ids if x not in trello_lists_ids]

        cursor = self.connection.cursor()

        for list_id in exclusive_lists:
            try:
                cursor.execute("DELETE FROM CFD_PRIORITY_ORDER WHERE PRIORITY_ID_LIST = '" + list_id + "'")
                self.connection.commit()
            except Error as e:
                print(e)
                return 0

    def insert_labels(self):
        inserted_rows = []

        trello_labels = self.trello_connection.get_trello_labels()
        db_cards_ids = self.get_db_labels_ids()

        sanitized_db_labels_ids = [x[0] for x in db_cards_ids]
        exclusive_labels = [x for x in trello_labels if x['id'] not in sanitized_db_labels_ids]

        cursor = self.connection.cursor()

        for data in exclusive_labels:
            insert_data = (data['id'], data['idBoard'], data['name'], data['color'])
            query = 'INSERT INTO LABELS (LABEL_ID, LABEL_ID_BOARD, LABEL_NAME, LABEL_COLOR)' \
                    'VALUES (?, ?, ?, ?)'
            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        return inserted_rows

    def insert_cards_labels(self, execution_id):

        inserted_rows = []
        labels = []

        trello_cards = self.trello_connection.get_trello_cards()

        for card in trello_cards:
            if len(card['idLabels']) > 0:
                for label_id in card['idLabels']:
                    labels.append((card['id'], label_id))

        cursor = self.connection.cursor()

        for data in labels:
            query = 'INSERT INTO CARDS_LABELS (CL_CARD_ID, CL_LABEL_ID, CL_CREATE_DATE, CL_STATE_ID)' \
                    'VALUES (?, ?, ?, ?)'
            insert_data = (data[0], data[1], self.execution_time, execution_id)

            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        return inserted_rows

    def update_labels(self):

        trello_labels_update = self.trello_connection.get_trello_labels()

        update_cursor = self.connection.cursor()

        for data in trello_labels_update:
            update_data = (data['idBoard'], data['name'], data['color'], self.execution_time, data['id'])
            query = 'UPDATE LABELS SET LABEL_ID_BOARD = ? ,LABEL_NAME = ?, LABEL_COLOR = ?, ' \
                    'LABEL_LAST_MODIFIED = ? WHERE LABEL_ID = ?'
            try:
                update_cursor.execute(query, update_data)
            except Error as e:
                print(e)
                return e
        self.connection.commit()

    def update_lists(self):

        trello_lists_update = self.trello_connection.get_trello_lists()

        update_cursor = self.connection.cursor()

        for data in trello_lists_update:
            update_data = (data['name'], data['closed'], data['pos'], self.execution_time, data['id'])
            query = 'UPDATE LISTS SET LIST_NAME = ? ,LIST_CLOSED = ?, LIST_POS = ?, ' \
                    'LIST_LAST_MODIFIED = ? WHERE LIST_ID = ?'
            try:
                update_cursor.execute(query, update_data)
                self.connection.commit()
            except Error as e:
                print(e)
                return e

    def update_cards(self):

        trello_cards_update = self.trello_connection.get_trello_cards()

        update_cursor = self.connection.cursor()
        cards_without_id = self.get_db_card_without_date()
        sanitized_cards = [x[0] for x in cards_without_id]

        for data in trello_cards_update:
            if data['id'] in sanitized_cards:
                creation_date = self.get_card_create_date(data)
                update_data = (data['name'], data['closed'], data['dateLastActivity'], data['idBoard'], data['pos'],
                               data['idList'], data['desc'], data['cover']['color'], data['isTemplate'],
                               data['idShort'],
                               data['due'], creation_date, self.execution_time, data['id'])
                query = 'UPDATE CARDS SET CARD_NAME = ? ,CARD_CLOSED = ?, ' \
                        'CARD_DATE_LAST_ACTIVITY = ?, CARD_ID_BOARD = ?,' \
                        'CARD_POS = ?, CARD_ID_LIST = ?, CARD_DESC = ?, CARD_COVER_COLOR = ?, CARD_IS_TEMPLATE = ?, ' \
                        'CARD_ID_SHORT = ?, CARD_DUE = ?,CARD_CREATION_DATE= ?,CARD_LAST_MODIFIED = ? WHERE CARD_ID = ?'
            else:
                update_data = (data['name'], data['closed'], data['dateLastActivity'], data['idBoard'], data['pos'],
                               data['idList'], data['desc'], data['cover']['color'], data['isTemplate'],
                               data['idShort'],
                               data['due'], self.execution_time, data['id'])
                query = 'UPDATE CARDS SET CARD_NAME = ? ,CARD_CLOSED = ?, ' \
                        'CARD_DATE_LAST_ACTIVITY = ?, CARD_ID_BOARD = ?,' \
                        'CARD_POS = ?, CARD_ID_LIST = ?, CARD_DESC = ?, CARD_COVER_COLOR = ?, CARD_IS_TEMPLATE = ?, ' \
                        'CARD_ID_SHORT = ?, CARD_DUE = ?,CARD_LAST_MODIFIED = ? WHERE CARD_ID = ?'
            try:
                update_cursor.execute(query, update_data)
                self.connection.commit()
            except Error as e:
                print(e)
                return e

    def cfd_priority_definition(self):
        query = 'UPDATE CFD_PRIORITY_ORDER ' \
                'SET PRIORITY_ORDER = ?, PRIORITY_LIST_NAME = ? || "- " || LIST_NAME ' \
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
                self.connection.commit()
            except Error as e:
                print(e)
                return e
            counter = counter + 1

    def delete_labels(self):

        db_labels_ids = self.get_db_labels_ids()
        trello_labels = self.trello_connection.get_trello_labels()

        sanitized_db_labels_ids = [x[0] for x in db_labels_ids]
        trello_labels_ids = [x['id'] for x in trello_labels]
        exclusive_labels = [x for x in sanitized_db_labels_ids if x not in trello_labels_ids]

        cursor = self.connection.cursor()

        for data in exclusive_labels:
            query = "DELETE FROM LABELS WHERE LABEL_ID = '" + data + "'"
            try:
                cursor.execute(query)
                self.connection.commit()
            except Error as e:
                print(e)
                return e

    def delete_lists(self):

        trello_lists = self.trello_connection.get_trello_lists()
        db_lists = self.get_db_lists()

        sanitized_db_lists_ids = [x[0] for x in db_lists]
        sanitized_trello_lists = [y['id'] for y in trello_lists]

        exclusive_lists = [x for x in sanitized_db_lists_ids if x not in sanitized_trello_lists]

        cursor = self.connection.cursor()

        for list_id in exclusive_lists:
            try:
                cursor.execute("DELETE FROM LISTS WHERE LIST_ID = '" + list_id + "'")
                self.connection.commit()
            except Error as e:
                print(e)
                return 0

    def delete_cards(self):

        trello_cards = self.trello_connection.get_trello_cards()
        db_cards = self.get_db_cards_ids()

        sanitized_db_cards_ids = [x[0] for x in db_cards]
        sanitized_trello_cards = [y['id'] for y in trello_cards]

        exclusive_cards = [x for x in sanitized_db_cards_ids if x not in sanitized_trello_cards]

        cursor = self.connection.cursor()

        for card_id in exclusive_cards:
            try:
                cursor.execute("DELETE FROM CARDS WHERE CARD_ID = '" + card_id + "'")
                self.connection.commit()
            except Error as e:
                print(e)
                return 0

    def insert_board_state(self, execution_id):

        trello_cards = self.trello_connection.get_trello_cards()
        trello_lists = self.trello_connection.get_trello_lists()
        lists_pos = []
        for list in trello_lists:
            lists_pos.append([list['id'], list['pos']])

        cursor = self.connection.cursor()
        list_pos = 0
        for card in trello_cards:
            for pos in lists_pos:
                if pos[0] == card['idList']:
                    list_pos = pos[1]

            query = 'INSERT INTO BOARD_STATE (BS_BOARD_ID, BS_LIST_ID, BS_CARD_ID, BS_CREATE_DATE, BS_STATE_ID, ' \
                    'BS_CARD_POS, BS_LIST_POS) ' \
                    'VALUES (?, ?, ?, ?, ?, ?, ?)'

            board_state_data = (card['idBoard'], card['idList'], card['id'], self.execution_time, execution_id,
                                card['pos'], list_pos)

            try:
                cursor.execute(query, board_state_data)
                self.connection.commit()
            except Error as e:
                print(e)
                return 0

    def execution_history(self):
        cursor = self.connection.cursor()
        current_time = ('DONE', self.execution_time)

        query = 'INSERT INTO EXECUTION_HISTORY (EH_DESCRIPTION, EH_CREATE_DATE) VALUES (?, ?)'
        try:
            cursor.execute(query, current_time)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(e)
            return 0

    def get_last_execution_date(self):
        query = 'SELECT MAX(EH_CREATE_DATE) FROM EXECUTION_HISTORY'
        cursor = self.connection.cursor()

        try:
            response = cursor.execute(query)
            response = response.fetchone()
            return response[0]
        except Error as e:
            print(e)
            return 0

    def get_card_create_date(self, card):

        date = ''
        action = self.trello_connection.get_cards_actions(card['id'], 'createCard')
        if not action:
            action = self.trello_connection.get_cards_actions(card['id'], 'copyCommentCard')
            if not action:
                action = self.trello_connection.get_cards_actions(card['id'], 'copyCard')
                if not action:
                    action = self.trello_connection.get_cards_actions(card['id'], 'addAttachmentToCard')
                    if not action[len(action)-1]['appCreator']:
                        action[0]['appCreator']
                        action = None

        if action:
            action = action.pop()
            date = parser.parse(action['date']).date()
        if date != '':
            return date
        else:
            return None

    def get_db_card_without_date(self):
        cursor = self.connection.cursor()
        query = 'SELECT CARD_ID FROM CARDS WHERE CARD_CREATION_DATE IS NULL'
        try:
            cursor.execute(query)
            response = cursor.fetchall()
            return response
        except Error as e:
            return 0

    def close(self):
        self.connection.close()
