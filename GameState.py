class GameState:
    deck_cards_top = []
    draw_deck_top_card = []
    column_cards = []
    new_cards_in_column = []
    column_all_cards = []
    empty_column_indices = []

    ui_components_to_render = {}
    def __init__(self):
        self.ui_components_to_render['draw_deck'] = []
        self.ui_components_to_render['top_deck'] = []
        self.ui_components_to_render['columns'] = [1,2,3,4,5,6,7]
        return        

