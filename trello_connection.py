from trello import TrelloApi


class TrelloConnection(TrelloApi):

    def __init__(self):
        self.trello_connection = None
        self.api_key = None
        self.api_key = None
        self.api_token = None
        self.board = None

    def set_key(self, key):
        self.api_key = key

    def set_token(self, token):
        self.api_token = token

    def set_board(self, board_id):
        self.board = board_id

    def connect(self):
        self.trello_connection = TrelloApi(self.api_key)
        self.trello_connection.set_token(self.api_token)

    def get_trello_lists(self):
        trello_lists = self.trello_connection.boards.get_list(self.board)
        return trello_lists

    def get_trello_cards(self):
        trello_cards = self.trello_connection.boards.get_card(self.board)
        return trello_cards

    def get_trello_board_actions(self):
        trello_actions = self.trello_connection.boards.get_action(self.board, filter='updateCard')
        return trello_actions

    def get_trello_labels(self):
        trello_labels = self.trello_connection.boards.get_label(self.board)
        return trello_labels
