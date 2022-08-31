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
        card_id = '62388f4cc42ec1865a9ef4fe'
        trello_card_actions = self.trello_connection.cards.get_action(card_id)
        return trello_card_actions

    def get_members_actions(self):
        id_member = '5d277e86ce62ae7ecc7a13c1'
        trello_members_actions = self.trello_connection.members.get_action(id_member)
        return trello_members_actions

    def get_cards_from_list(self, list_id: str):
        cards = self.trello_connection.lists.get_card(list_id)
        return cards

    def add_label_to_card(self, card_id: str):
        label_id = '62c6cfabd2f01b44dbd0fe22'
        add_label = self.trello_connection.cards.new_idLabel(card_id, label_id)
        return add_label

    def update_card_id_list(self, card_id: str, id_list: str):
        new_list = self.trello_connection.cards.update_idList(card_id, id_list)
        return new_list

    def delete_card_label(self, id_label: str, card_id: str):
        deleted_label = self.trello_connection.cards.delete_idLabel_idLabel(id_label, card_id)
        return deleted_label
