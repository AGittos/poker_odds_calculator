from hand import Hand

def play_hand():

    hole_cards = input('Enter hole cards:')
    hand = Hand(hole_cards)

    print(hand.win_percent)





if __name__ = '__main__':

    play_hand()
