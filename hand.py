from scoring import fetch_scores, possible_hands
from rules import cards

from numba import njit
from scipy.stats import percentileofscore
from statistics import mean

cards_set = {cards}

def _expected_outcome(hole_cards: set, com_cards: set, min_cards: int):

    hand_scores = []

    player_mins = [set(x) for x in possible_hands(list(hole_cards)+list(com_cards), min_cards)]

    opponent_base_possible = scores_df[scores_df['hands'].apply(lambda x: x.intersection(hole_cards) == set())]

    for hand in player_mins:

        player_hand_scores = scores_df[scores_df['hands'].apply(lambda x: x.issuperset(hand))]

        non_hole_cards = hand.difference(set(hole_cards))

        opponent_possible_scores = opponent_base_possible[opponent_base_possible.hands.apply(lambda x: x.intersection(non_hole_cards) == set())].score

        for score in player_hand_scores.score:

            hand_scores.append(percentileofscore(opponent_possible_scores, score, kind='strict'))



    return mean(hand_scores)

class Hand():

    def __init__(self,hole_cards):
        self.flop = []
        self.turn = []
        self.river = []
        self.com_cards = []

        self.hole_cards = hole_cards
        self.win_percent = 0

    def _calculate_odds(self, round: str):

        cards_left_dict = {'flop': 3, 'turn': 4, 'river': 5}
        return _expected_outcome({self.hole_cards},{self.com_cards},cards_left_dict[round])

    def _player_input(self, round: str):

        num_cards_dict = {'flop': 3, 'turn': 1, 'river': 1}

        valid_input = False

        while valid_input == False:

            input = input("Input flop Cards:").split(' ')

            if (diff_set := {input}.difference(cards_set)) == set() and len(input) == num_cards_dict[round]:

                setattr(self,round, input)

                self.com_cards += input

                valid_input = True

            else: print(f'Input {diff_set} is invalid')

    def commence_hand(self):

        print('New Hand - suits are h (hearts), c (clubs), s (spades), d (diamonds) and values are 1-13 (aces high)')
        print('Card examples: h1, c13, d10')

        









if __name__ == '__main__':

    print('check correct run')

    scores_df = fetch_scores()
    print('scores returned successfully')

    print(expected_outcome({'H13', 'C13'}, {'S13', 'D13', 'S1'}, 3))

