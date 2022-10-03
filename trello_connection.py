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
        trello_actions = self.trello_connection.boards.get_action(self.board, filter='updateCard', limit=1000)
        return trello_actions

    def get_trello_labels(self):
        trello_labels = self.trello_connection.boards.get_label(self.board, limit=1000)
        return trello_labels

    def get_cards_actions(self, card_id, param):
        # card_id = '62388f4cc42ec1865a9ef4fe'
        trello_card_actions = self.trello_connection.cards.get_action(card_id, filter=param)
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

    def get_members_from_board(self):
        members = self.trello_connection.boards.get_member(self.board)
        return members

    def get_all_board_actions_formatted(self, limit=1000):
        list_of_actions = ["updateCard", "copyCard", "createCard", "deleteCard", "moveCardToBoard"]
        action_id = ''
        formatted_board_actions = []
        action_list = []
        action_object = {}
        interface = {
            "id": "id",
            "idMemberCreator": "idMemberCreator",
            "cardId": "data.card.id",
            "boardId": "data.board.id",
            "listBefore": "data.listBefore.id",
            "listAfter": "data.listAfter.id",
            "type": "type",
            "date": "date",
            "cardPos": "data.card.pos",
            "oldPos": "data.old.pos",
            "listId": "data.list.id",
            "appCreator": "appCreator.name",
            "translationKey": "display.translationKey",
            "labelId": "data.label.id",
            "cardSource": "data.cardSource.id",
            "boardSource": "data.boardSource.id"
        }
        default_dict = interface

        for action in list_of_actions:
            response_is_empty = False
            num_execution = 0
            board_actions = []

            while not response_is_empty:
                if num_execution == 0:
                    actions = self.trello_connection.boards.get_action(self.board, filter=action, limit=limit)
                    board_actions = board_actions + actions
                elif num_execution > 0:
                    actions = self.trello_connection.boards.get_action(self.board, filter=action, limit=limit,
                                                                       before=action_id)
                    board_actions = board_actions + actions
                num_execution = num_execution + 1
                if len(actions) == 0:
                    response_is_empty = True
                elif len(actions) > 0:
                    action_id = actions[-1]['id']
                if num_execution == 50:
                    print('num_execution reached 50')
                    break
            for item in board_actions:
                for key in default_dict:
                    splitted_values = default_dict[key].split('.')
                    if splitted_values[0] in item:
                        action_list.append(item[splitted_values[0]])
                    else:
                        action_object[key] = None
                        continue
                    for index, value in enumerate(splitted_values):
                        if index > 0:
                            if action_list[0] is not None:
                                if value in action_list[0]:
                                    action_list[0] = action_list[0][value]
                                else:
                                    action_list[0] = None
                    action_object[key] = action_list[0]
                    action_list = []
                formatted_board_actions.append(action_object)
                action_object = {}
        print('Total actions from board: {}'.format(len(formatted_board_actions)))
        return formatted_board_actions
