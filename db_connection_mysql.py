import pymysql as mysql
from pymysql import Error
from datetime import datetime
from dateutil import parser


class MySQLConnection:

    def __init__(self, trello_conn, config):
        self.connection = None
        self.execution_time = datetime.now()
        self.trello_connection = trello_conn
        self.config = config
        self.environment = config.environment.ENV
        self.execution_id = None
        try:
            if self.environment == 'production':
                self.connection = mysql.connect(user=config.database.MYSQL_USER, passwd=config.database.MYSQL_PASSWORD,
                                                db=config.database.MYSQL_DATABASE, host=config.database.MYSQL_HOST)
            else:
                self.connection = mysql.connect(user=config.database.DEV_MYSQL_USER,
                                                passwd=config.database.DEV_MYSQL_PASSWORD,
                                                db=config.database.DEV_MYSQL_DATABASE,
                                                host=config.database.DEV_MYSQL_HOST,
                                                port=config.database.DEV_MYSQL_PORT
                                                )
        except Error as e:
            print(e)
            return 0

    def get_db_cards_labels(self):
        message = 'get_db_cards_labels started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        query = "SELECT CL_CARD_ID, CL_LABEL_ID FROM CARDS_LABELS " \
                "WHERE CL_BOARD_ID = '" + self.trello_connection.board + "'"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_response = cursor.fetchall()
            return db_response
        except Error as e:
            print(e)
            return 0

    def get_db_lists(self):
        message = 'get_db_lists started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        query = 'SELECT LIST_ID FROM LISTS WHERE ' \
                "LIST_ID_BOARD = '" + self.trello_connection.board + "' ORDER BY LIST_POS DESC"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_lists = cursor.fetchall()
            return db_lists
        except Error as e:
            print(e)
            return 0

    def get_db_labels_ids(self):
        message = 'get_db_labels_ids started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        query = "SELECT LABEL_ID FROM LABELS WHERE LABEL_ID_BOARD = '" + self.trello_connection.board + "'"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_labels = cursor.fetchall()
            return db_labels
        except Error as e:
            print(e)
            return 0

    def get_db_cards_ids(self):
        message = 'get_db_cards_ids started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        query = "SELECT CARD_ID FROM CARDS WHERE CARD_ID_BOARD ='" + self.trello_connection.board + "'"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_cards = cursor.fetchall()
            return db_cards
        except Error as e:
            print(e)
            return 0

    def get_db_board_actions_ids(self):
        message = 'get_db_board_actions_ids started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        query = "SELECT ACTION_ID FROM ACTIONS WHERE ACTION_BOARD_ID = '" + self.trello_connection.board + "'"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_actions = cursor.fetchall()
            return db_actions
        except Error as e:
            print(e)
            return 0

    def get_cfd_priority_list(self):
        message = 'get_cfd_priority_list started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        query = "SELECT PRIORITY_ID_LIST FROM CFD_PRIORITY_ORDER " \
                "WHERE PRIORITY_ID_BOARD ='" + self.trello_connection.board + "'"
        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            db_cfd_list = cursor.fetchall()
            return db_cfd_list
        except Error as e:
            print(e)
            return 0

    def insert_lists(self):
        message = 'insert_lists started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        self.insert_execution_log(message)
        inserted_rows = []

        trello_lists = self.trello_connection.get_trello_lists()
        db_lists_ids = self.get_db_lists()

        sanitized_db_lists_ids = [x[0] for x in db_lists_ids]
        exclusive_lists = [x for x in trello_lists if x['id'] not in sanitized_db_lists_ids]

        cursor = self.connection.cursor()

        for data in exclusive_lists:
            insert_data = (data['id'], data['name'], data['closed'], data['idBoard'], data['pos'])
            query = 'INSERT INTO LISTS (LIST_ID, LIST_NAME ,LIST_CLOSED, LIST_ID_BOARD, LIST_POS) VALUES (%s, %s, %s,' \
                    '%s, %s)'
            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        return inserted_rows

    def insert_cards(self):
        message = 'insert_cards started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        inserted_rows = []

        trello_cards = self.trello_connection.get_all_cards()
        db_cards_ids = self.get_db_cards_ids()

        sanitized_db_cards_ids = [x[0] for x in db_cards_ids]
        exclusive_cards = [x for x in trello_cards if x['id'] not in sanitized_db_cards_ids]

        cursor = self.connection.cursor()

        for data in exclusive_cards:
            insert_data = (
                data['id'], data['name'], data['closed'], parser.parse(data['dateLastActivity']).date(),
                data['idBoard'],
                data['pos'], data['idList'], data['desc'], data['cover']['color'], data['isTemplate'],
                data['idShort'], data['due'], data['shortUrl'])
            query = 'INSERT INTO CARDS (CARD_ID, CARD_NAME, CARD_CLOSED, CARD_DATE_LAST_ACTIVITY, CARD_ID_BOARD,' \
                    'CARD_POS, CARD_ID_LIST, CARD_DESC, CARD_COVER_COLOR, CARD_IS_TEMPLATE, CARD_ID_SHORT, ' \
                    'CARD_DUE, CARD_SHORT_URL)' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        return inserted_rows

    def insert_actions(self):
        message = 'insert_actions started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
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
                               data['data']['listAfter']['id'], data['type'], data['date'], 'PYTHON')
                query = 'INSERT INTO ACTIONS (ACTION_ID, ACTION_ID_MEMBER_CREATOR ,ACTION_CARD_ID, ACTION_BOARD_ID,' \
                        'ACTION_LIST_BEFORE, ACTION_LIST_AFTER, ACTION_TYPE, ACTION_DATE, ACTION_INSERT_SOURCE)' \
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                try:
                    cursor.execute(query, insert_data)
                    self.connection.commit()
                    inserted_rows.append(cursor.lastrowid)
                except Error as e:
                    print(e)
                    return e

        return inserted_rows

    def insert_cfd(self):
        message = 'insert_cfd started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        inserted_rows = []
        query = 'INSERT INTO CFD (CFD_BOARD_ID, CFD_LIST_ID, CFD_TOTAL_CARDS, CFD_PROCESSING_DATE) ' \
                'SELECT LIST_ID_BOARD AS CFD_BOARD_ID ' \
                ',LIST_ID AS CFD_LIST_NAME ' \
                ',COUNT(CARD_ID) AS CFD_TOTAL_TASKS ' \
                ',NOW() AS CFD_PROCESSING_DATE ' \
                'FROM ' \
                'CARDS ' \
                'INNER JOIN LISTS ON LIST_ID = CARD_ID_LIST ' \
                'WHERE CARD_CLOSED = 0 ' \
                'GROUP BY  ' \
                'LIST_ID_BOARD ' \
                ',LIST_ID'

        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            self.connection.commit()
            inserted_rows.append(cursor.lastrowid)
        except Error as e:
            print(e)
            return e

    def insert_cfd_priority_order(self):
        message = 'insert_cfd_priority_order started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        inserted_rows = []
        query = 'INSERT INTO CFD_PRIORITY_ORDER (PRIORITY_ID_BOARD,PRIORITY_ID_LIST, PRIORITY_ORDER) ' \
                'SELECT LIST_ID_BOARD' \
                ',LIST_ID' \
                ',0 ' \
                'FROM ' \
                'LISTS ' \
                'WHERE ' \
                'LIST_ID NOT IN (SELECT PRIORITY_ID_LIST FROM CFD_PRIORITY_ORDER ' \
                'WHERE PRIORITY_ID_BOARD = "' + self.trello_connection.board + '") AND ' \
                                                                               "LIST_ID_BOARD = '" + self.trello_connection.board + "'"

        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            self.connection.commit()
            inserted_rows.append(cursor.lastrowid)
        except Error as e:
            print(e)
            return e

    def delete_cfd_priority_order(self):
        message = 'delete_cfd_priority_order started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
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
        message = 'insert_labels started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        inserted_rows = []

        trello_labels = self.trello_connection.get_trello_labels()
        db_cards_ids = self.get_db_labels_ids()

        sanitized_db_labels_ids = [x[0] for x in db_cards_ids]
        exclusive_labels = [x for x in trello_labels if x['id'] not in sanitized_db_labels_ids]

        cursor = self.connection.cursor()

        for data in exclusive_labels:
            insert_data = (data['id'], data['idBoard'], data['name'], data['color'])
            query = 'INSERT INTO LABELS (LABEL_ID, LABEL_ID_BOARD, LABEL_NAME, LABEL_COLOR)' \
                    'VALUES (%s, %s, %s, %s)'
            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        return inserted_rows

    def insert_cards_labels(self, execution_id):
        message = 'insert_cards_labels started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        inserted_rows = []
        labels = []

        trello_cards = self.trello_connection.get_trello_cards()
        done_list = self.get_board_done_list()
        done_list = done_list[0]
        cards_not_on_done_list = [x for x in trello_cards if x['idList'] not in done_list]

        for card in cards_not_on_done_list:
            if len(card['idLabels']) > 0:
                for label_id in card['idLabels']:
                    labels.append((card['id'], label_id, card['idBoard']))

        cursor = self.connection.cursor()

        for data in labels:
            query = 'INSERT INTO CARDS_LABELS (CL_CARD_ID, CL_LABEL_ID, CL_BOARD_ID, CL_INSERTED_AT, CL_STATE_ID)' \
                    'VALUES (%s, %s, %s, %s, %s)'
            insert_data = (data[0], data[1], data[2], self.execution_time, execution_id)

            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        return inserted_rows

    def insert_cards_members(self, execution_id):
        message = 'insert_cards_members started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        inserted_rows = []
        members = []

        trello_cards = self.trello_connection.get_trello_cards()
        done_list = self.get_board_done_list()
        done_list = done_list[0]
        cards_not_on_done_list = [x for x in trello_cards if x['idList'] not in done_list]

        for card in cards_not_on_done_list:
            if len(card['idMembers']) > 0:
                for member in card['idMembers']:
                    members.append((card['idBoard'], card['id'], member))
        cursor = self.connection.cursor()

        for member in members:
            query = 'INSERT INTO CARDS_MEMBERS (CM_BOARD_ID, CM_CARD_ID, CM_MEMBER_ID, CM_STATE_ID, ' \
                    'CM_INSERTED_AT, CM_UPDATED_AT) VALUES (%s, %s, %s, %s, %s, %s)'
            insert_data = (member[0], member[1], member[2], execution_id, self.execution_time,
                           self.execution_time)
            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        return inserted_rows

    def update_labels(self):
        message = 'update_labels started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        trello_labels = self.trello_connection.get_trello_labels()

        update_cursor = self.connection.cursor()

        for data in trello_labels:
            update_data = (data['idBoard'], data['name'], data['color'], self.execution_time, data['id'])
            query = 'UPDATE LABELS SET LABEL_ID_BOARD = %s ,LABEL_NAME = %s, LABEL_COLOR = %s, ' \
                    'LABEL_LAST_MODIFIED = %s WHERE LABEL_ID = %s'
            try:
                update_cursor.execute(query, update_data)
            except Error as e:
                print(e)
                return e
        self.connection.commit()

    def update_lists(self):
        message = 'update_lists started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        trello_lists_update = self.trello_connection.get_trello_lists()

        update_cursor = self.connection.cursor()

        for data in trello_lists_update:
            update_data = (data['name'], data['closed'], data['pos'], self.execution_time, data['id'])
            query = 'UPDATE LISTS SET LIST_NAME = %s ,LIST_CLOSED = %s, LIST_POS = %s, ' \
                    'LIST_LAST_MODIFIED = %s WHERE LIST_ID = %s'
            try:
                update_cursor.execute(query, update_data)
                self.connection.commit()
            except Error as e:
                print(e)
                return e

    def update_cards(self):
        message = 'update_cards started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        trello_cards_update = self.trello_connection.get_all_cards()

        update_cursor = self.connection.cursor()
        cards_without_date = self.get_db_card_without_date()
        sanitized_cards = [x[0] for x in cards_without_date]

        for data in trello_cards_update:
            if data['id'] in sanitized_cards:
                creation_date = self.get_card_create_date(data)
                update_data = (data['name'], data['closed'], parser.parse(data['dateLastActivity']), data['idBoard'],
                               data['pos'],
                               data['idList'], data['desc'], data['cover']['color'], data['isTemplate'],
                               data['idShort'],
                               data['due'], creation_date, self.execution_time, data['id'])
                query = 'UPDATE CARDS SET CARD_NAME = %s ,CARD_CLOSED = %s, ' \
                        'CARD_DATE_LAST_ACTIVITY = %s, CARD_ID_BOARD = %s,' \
                        'CARD_POS = %s, CARD_ID_LIST = %s, CARD_DESC = %s, CARD_COVER_COLOR = %s, CARD_IS_TEMPLATE = ' \
                        '%s, ' \
                        'CARD_ID_SHORT = %s, CARD_DUE = %s,CARD_CREATION_DATE= %s,CARD_LAST_MODIFIED = %s WHERE ' \
                        'CARD_ID = %s '
            else:
                update_data = (data['name'], data['closed'], parser.parse(data['dateLastActivity']), data['idBoard'],
                               data['pos'],
                               data['idList'], data['desc'], data['cover']['color'], data['isTemplate'],
                               data['idShort'],
                               data['due'], self.execution_time, data['id'])
                query = 'UPDATE CARDS SET CARD_NAME = %s ,CARD_CLOSED = %s, ' \
                        'CARD_DATE_LAST_ACTIVITY = %s, CARD_ID_BOARD = %s,' \
                        'CARD_POS = %s, CARD_ID_LIST = %s, CARD_DESC = %s, CARD_COVER_COLOR = %s, ' \
                        'CARD_IS_TEMPLATE = %s, ' \
                        'CARD_ID_SHORT = %s, CARD_DUE = %s,CARD_LAST_MODIFIED = %s WHERE CARD_ID = %s'
            try:
                update_cursor.execute(query, update_data)
                self.connection.commit()
            except Error as e:
                print(e)
                return e

    def cfd_priority_definition(self):
        message = 'cfd_priority_definition started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        query = 'UPDATE CFD_PRIORITY_ORDER ' \
                'JOIN LISTS ON LIST_ID = PRIORITY_ID_LIST ' \
                'SET PRIORITY_ORDER = %s, PRIORITY_LIST_NAME = CONCAT(%s, " - " , LIST_NAME) ' \
                'WHERE PRIORITY_ID_LIST = %s'
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

    def close_labels(self):
        message = 'close_labels started at: ' + str(datetime.now())
        print(message)
        db_labels_ids = self.get_db_labels_ids()
        trello_labels = self.trello_connection.get_trello_labels()

        sanitized_db_labels_ids = [x[0] for x in db_labels_ids]
        trello_labels_ids = [x['id'] for x in trello_labels]
        exclusive_labels = [x for x in sanitized_db_labels_ids if x not in trello_labels_ids]

        cursor = self.connection.cursor()

        for data in exclusive_labels:
            query = "UPDATE LABELS SET LABEL_CLOSED = 1 WHERE LABEL_ID = '" + data + "'"
            try:
                cursor.execute(query)
                self.connection.commit()
            except Error as e:
                print(e)
                return e

    def close_lists(self):
        message = 'close_lists started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        trello_lists = self.trello_connection.get_trello_lists()
        db_lists = self.get_db_lists()

        sanitized_db_lists_ids = [x[0] for x in db_lists]
        sanitized_trello_lists = [y['id'] for y in trello_lists]

        exclusive_lists = [x for x in sanitized_db_lists_ids if x not in sanitized_trello_lists]

        cursor = self.connection.cursor()

        for list_id in exclusive_lists:
            try:
                cursor.execute("UPDATE LISTS SET LIST_CLOSED = 1 WHERE LIST_ID = '" + list_id + "'")
                self.connection.commit()
            except Error as e:
                print(e)
                return 0

    def close_cards(self):
        message = 'close_cards started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        trello_cards = self.trello_connection.get_trello_cards()
        db_cards = self.get_db_cards_ids()

        sanitized_db_cards_ids = [x[0] for x in db_cards]
        sanitized_trello_cards = [y['id'] for y in trello_cards]

        exclusive_cards = [x for x in sanitized_db_cards_ids if x not in sanitized_trello_cards]

        cursor = self.connection.cursor()

        for card_id in exclusive_cards:
            try:
                cursor.execute("UPDATE CARDS SET CARD_CLOSED = 1 WHERE CARD_ID = '" + card_id + "'")
                self.connection.commit()
            except Error as e:
                print(e)
                return 0

    def get_board_done_list(self):
        message = 'get_board_done_list started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        query = "SELECT RULES_TRELLO_OBJECT_ID FROM RULES WHERE RULES_KEY = 'doneList' " \
                "AND RULES_ID_BOARD = '" + self.trello_connection.board + "' LIMIT 1"
        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            db_cfd_list = cursor.fetchall()
            return db_cfd_list
        except Error as e:
            print(e)
            return 0

    def insert_board_state(self, execution_id):
        message = 'insert_board_state started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        trello_cards = self.trello_connection.get_trello_cards()
        trello_lists = self.trello_connection.get_trello_lists()
        done_list = self.get_board_done_list()
        done_list = done_list[0]
        cards_not_on_done_list = [x for x in trello_cards if x['idList'] not in done_list]
        lists_pos = []

        for list in trello_lists:
            lists_pos.append([list['id'], list['pos']])

        cursor = self.connection.cursor()
        list_pos = 0

        for card in cards_not_on_done_list:
            for pos in lists_pos:
                if pos[0] == card['idList']:
                    list_pos = pos[1]

            query = 'INSERT INTO BOARD_STATE (BS_BOARD_ID, BS_LIST_ID, BS_CARD_ID, BS_CREATE_DATE, BS_STATE_ID, ' \
                    'BS_CARD_POS, BS_LIST_POS) ' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)'

            board_state_data = (card['idBoard'], card['idList'], card['id'], self.execution_time, execution_id,
                                card['pos'], list_pos)

            try:
                cursor.execute(query, board_state_data)
                self.connection.commit()
            except Error as e:
                print(e)
                return 0

    def get_done_list(self, done_list):
        message = 'get_done_list started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        cursor = self.connection.cursor()
        query = "SELECT DL_BOARD_ID, DL_LIST_ID, DL_CARD_ID ,DL_LABEL_ID FROM DONE_LIST WHERE " \
                "DL_BOARD_ID = '" + self.trello_connection.board + "' AND DL_LIST_ID = '" + done_list + "'"
        try:
            cursor.execute(query)
            response = cursor.fetchall()
            return response
        except Error as e:
            return 0

    def insert_done_list(self):
        message = 'insert_done_list started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        trello_cards = self.trello_connection.get_trello_cards()
        done_list = self.get_board_done_list()
        if len(done_list) > 0:
            done_list = done_list[0][0]
            cards_on_done_list = [x for x in trello_cards if x['idList'] == done_list]
            cards_already_done = self.get_done_list(done_list)
            cards_already_done = [x[2] for x in cards_already_done]
            new_cards = [x for x in cards_on_done_list if x['id'] not in cards_already_done]
            cursor = self.connection.cursor()
            for card in new_cards:
                for label in card['idLabels']:
                    done_list_data = (card['idBoard'], card['idList'], card['id'], label, self.execution_time,
                                      self.execution_time)

                    query = 'INSERT INTO DONE_LIST (DL_BOARD_ID, DL_LIST_ID, DL_CARD_ID, DL_LABEL_ID,DL_INSERTED_AT, ' \
                            'DL_UPDATED_AT) VALUES (%s, %s, %s, %s, %s, %s)'

                    try:
                        cursor.execute(query, done_list_data)
                        self.connection.commit()
                    except Error as e:
                        print(e)
                        return 0

    def insert_execution_history(self):
        message = 'insert_execution_history started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)

        cursor = self.connection.cursor()

        query = 'INSERT INTO EXECUTION_HISTORY (EH_DESCRIPTION, EH_CREATE_DATE, EH_ID_BOARD) VALUES (%s, %s, %s)'
        try:
            cursor.execute(query, ('DONE', self.execution_time, self.trello_connection.board))
            self.connection.commit()
            self.execution_id = cursor.lastrowid
            self.insert_execution_log(message)
            return cursor.lastrowid
        except Error as e:
            print(e)
            return 0

    def get_card_create_date(self, card):
        message = 'get_card_create_date started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        date = ''
        action = self.trello_connection.get_cards_actions(card['id'], 'createCard')
        if not action:
            action = self.trello_connection.get_cards_actions(card['id'], 'copyCommentCard')
            if not action:
                action = self.trello_connection.get_cards_actions(card['id'], 'copyCard')
                if not action:
                    action = self.trello_connection.get_cards_actions(card['id'], 'addAttachmentToCard')
                    if not action[len(action) - 1]['appCreator']:
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
        message = 'get_db_card_without_date started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        cursor = self.connection.cursor()
        query = "SELECT CARD_ID FROM CARDS WHERE CARD_CREATION_DATE IS NULL " \
                "AND CARD_ID_BOARD = '" + self.trello_connection.board + "'"
        try:
            cursor.execute(query)
            response = cursor.fetchall()
            return response
        except Error as e:
            return 0

    def get_db_members(self):
        message = 'get_db_members started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        query = 'SELECT MEMBER_ID FROM MEMBER WHERE MEMBER_BOARD_ID = "' + self.trello_connection.board + '"'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            response = cursor.fetchall()
            return response
        except Error as e:
            print(e)
            return 0

    def insert_db_members(self):
        message = 'insert_db_members started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        inserted_rows = []

        trello_members = self.trello_connection.get_members_from_board()
        db_members_ids = self.get_db_members()

        sanitized_db_members_ids = [x[0] for x in db_members_ids]
        exclusive_members = [x for x in trello_members if x['id'] not in sanitized_db_members_ids]

        cursor = self.connection.cursor()

        if len(exclusive_members) > 0:
            for data in exclusive_members:
                insert_data = (data['id'], data['fullName'], data['username'], self.trello_connection.board)
                query = 'INSERT INTO MEMBER (MEMBER_ID, MEMBER_FULL_NAME ,MEMBER_USER_NAME, MEMBER_BOARD_ID) VALUES ' \
                        '(%s, %s, %s, %s)'
                try:
                    cursor.execute(query, insert_data)
                    self.connection.commit()
                    inserted_rows.append(cursor.lastrowid)
                except Error as e:
                    print(e)
                    return e
            return inserted_rows

    def insert_all_actions(self, actions):
        message = 'insert_all_actions started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)
        inserted_rows = []

        trello_actions = actions
        db_actions_ids = self.get_db_board_actions_ids()

        sanitized_db_actions_ids = [x[0] for x in db_actions_ids]
        exclusive_actions = [x for x in trello_actions if x['id'] not in sanitized_db_actions_ids]
        print('Total exclusive actions: {}'.format(len(exclusive_actions)))

        cursor = self.connection.cursor()
        for data in exclusive_actions:
            insert_data = (data['id'], data['idMemberCreator'], data['cardId'], data['boardId'], data['listBefore'],
                           data['listAfter'],
                           data['type'], parser.parse(data['date']).replace(hour=parser.parse(data['date']).hour - 3),
                           data['cardPos'],
                           data['oldPos'],
                           data['listId'], data['appCreator'], data['translationKey'], data['labelId'],
                           data['cardSource'], data['boardSource'], 'PYTHON')
            query = 'INSERT INTO ACTIONS ' \
                    '(ACTION_ID, ACTION_ID_MEMBER_CREATOR ,ACTION_CARD_ID, ACTION_BOARD_ID,' \
                    'ACTION_LIST_BEFORE, ACTION_LIST_AFTER, ACTION_TYPE, ACTION_DATE, ACTION_CARD_POS,' \
                    'ACTION_OLD_POS, ACTION_LIST_ID, ACTION_APP_CREATOR, ACTION_TRANSLATION_KEY, ' \
                    'ACTION_LABEL_ID, ACTION_CARD_SOURCE, ACTION_BOARD_SOURCE, ACTION_INSERT_SOURCE)' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        print("{} actions were inserted".format(len(inserted_rows)))
        return inserted_rows

    def get_active_boards(self):
        message = 'get_active_boards started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)

        query = 'SELECT BOARD_ID FROM BOARDS WHERE BOARD_ACTIVE = 1'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            response = cursor.fetchall()
            return response
        except Error as e:
            print(e)
            return 0

    def get_exclusive_actions(self, actions):
        message = 'get_exclusive_actions started at:', datetime.now()
        print(message)
        self.insert_execution_log(message)

        trello_actions = actions

        db_actions_ids = self.get_db_board_actions_ids()

        sanitized_db_actions_ids = [x[0] for x in db_actions_ids]
        exclusive_actions = [x for x in trello_actions if x not in sanitized_db_actions_ids]
        return exclusive_actions

    def insert_exclusive_actions(self, exclusive_actions):
        message = 'insert_exclusive_actions started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)

        inserted_rows = []
        cursor = self.connection.cursor()

        for data in exclusive_actions:
            insert_data = (data['id'], data['idMemberCreator'], data['cardId'], data['boardId'], data['listBefore'],
                           data['listAfter'], data['type'],
                           parser.parse(data['date']).replace(hour=parser.parse(data['date']).hour - 3),
                           data['cardPos'],
                           data['oldPos'],
                           data['listId'], data['appCreator'], data['translationKey'], data['labelId'],
                           data['cardSource'], data['boardSource'], 'PYTHON')
            query = 'INSERT INTO ACTIONS ' \
                    '(ACTION_ID, ACTION_ID_MEMBER_CREATOR ,ACTION_CARD_ID, ACTION_BOARD_ID,' \
                    'ACTION_LIST_BEFORE, ACTION_LIST_AFTER, ACTION_TYPE, ACTION_DATE, ACTION_CARD_POS,' \
                    'ACTION_OLD_POS, ACTION_LIST_ID, ACTION_APP_CREATOR, ACTION_TRANSLATION_KEY, ' \
                    'ACTION_LABEL_ID, ACTION_CARD_SOURCE, ACTION_BOARD_SOURCE, ACTION_INSERT_SOURCE)' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            try:
                cursor.execute(query, insert_data)
                self.connection.commit()
                inserted_rows.append(cursor.lastrowid)
            except Error as e:
                print(e)
                return e
        print("{} actions were inserted".format(len(inserted_rows)))
        return inserted_rows

    def update_execution_history(self, execution_id):
        message = 'update_execution_history started at: ' + str(datetime.now())
        print(message)
        self.insert_execution_log(message)

        update_cursor = self.connection.cursor()

        query = 'UPDATE EXECUTION_HISTORY SET EH_FINISHED_AT = %s WHERE EH_IDENTITY = %s'
        update_data = (datetime.now(), execution_id)

        try:
            update_cursor.execute(query, update_data)
        except Error as e:
            print(e)
            return e
        self.connection.commit()

    def insert_execution_log(self, process_message):
        # message = 'insert_execution_log started at: ' + str(datetime.now())
        # print(message)

        insert_cursor = self.connection.cursor()

        query = 'INSERT INTO EXECUTION_LOG (EL_EXECUTION_ID, EL_MESSAGE) VALUES (%s, %s)'
        insert_data = (self.execution_id, process_message)

        try:
            insert_cursor.execute(query, insert_data)
        except Error as e:
            print(e)
            return e
        self.connection.commit()

    def close(self):
        self.connection.close()
