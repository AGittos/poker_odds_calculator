suits = ['C','H','S','D']
numbers = tuple(range(2,15))

cards = [x + str(i) for x in suits for i in numbers]

hands = (
'royal_flush', 'straight_flush', '4_kind', 'full_house', 'flush', 'straight', 'trips', '2_pair', 'pair', 'high_card')


if __name__ == '__main__':

    print(cards)