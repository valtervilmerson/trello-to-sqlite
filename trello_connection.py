from trello import TrelloApi


class TrelloConnection(TrelloApi):

    def __init__(self, api_key: str):
        self.trello_connection = TrelloApi(api_key)
        self.api_token = None
        self.board = None

    def set_api_token(self, api_token: str):
        self.trello_connection.set_token(api_token)

    def set_board(self, board_id: str):
        self.board = board_id

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

    def get_cards_actions(self):
        trello_card_actions = self.trello_connection.cards.get_action('62388f4cc42ec1865a9ef4fe')
        return trello_card_actions

    def get_members_actions(self):
        trello_members_actions = self.trello_connection.members.get_action('5d277e86ce62ae7ecc7a13c1')
        return trello_members_actions
