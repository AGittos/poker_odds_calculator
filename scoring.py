from rules import cards
import numpy as np
import itertools as itr
from pandas import DataFrame, read_pickle
import time

from resources.codetools import timefunc


hand_scores_filepath = 'resources/hand_scores.pkl'

def possible_hands(all_cards, n):
    arr = np.asarray(all_cards)
    t = np.dtype([('', arr.dtype)] * n)
    result = np.fromiter(itr.combinations(arr, n), t)
    return result.view(arr.dtype).reshape(-1, n)

def _check_four_of_a_kind(numbers):
    for i in numbers:
            if numbers.count(i) == 4:
                four = i
            elif numbers.count(i) == 1:
                card = i
    score = 105 + four + card/100
    return score

def _check_full_house(numbers):
    for i in numbers:
        if numbers.count(i) == 3:
            full = i
        elif numbers.count(i) == 2:
            p = i
    score = 90 + full + p/100
    return score

def _check_three_of_a_kind(numbers):
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            three = i
        else:
            cards.append(i)
    score = 45 + three + max(cards) + min(cards)/1000
    return score

def _check_two_pair(numbers):
    pairs = []
    cards = []
    for i in numbers:
        if numbers.count(i) == 2:
            pairs.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards, reverse=True)
    score = 30 + max(pairs) + min(pairs)/100 + cards[0]/1000
    return score

def _check_pair(numbers):
    pair = []
    cards  = []
    for i in numbers:
        if numbers.count(i) == 2:
            pair.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards, reverse=True)
    score = 15 + pair[0] + cards[0]/100 + cards[1]/1000 + cards[2]/10000
    return score


def _hands_score(hand):
    letters = [hand[i][:1] for i in range(5)]  # We get the suit for each card in the hand
    numbers = [int(hand[i][1:]) for i in range(5)]  # We get the number for each card in the hand
    rnum = [numbers.count(i) for i in numbers]  # We count repetitions for each number
    rlet = [letters.count(i) for i in letters]  # We count repetitions for each letter
    dif = max(numbers) - min(numbers)  # The difference between the greater and smaller number in the hand
    handtype = ''
    score = 0
    if 5 in rlet:
        if numbers == [14, 13, 12, 11, 10]:
            handtype = 'royal_flush'
            score = 135
        elif dif == 4 and max(rnum) == 1:
            handtype = 'straight_flush'
            score = 120 + max(numbers)
        elif 4 in rnum:
            handtype == 'four of a kind'
            score = _check_four_of_a_kind(numbers)
        elif sorted(rnum) == [2, 2, 3, 3, 3]:
            handtype == 'full house'
            score = _check_full_house(numbers)
        elif 3 in rnum:
            handtype = 'three of a kind'
            score = _check_three_of_a_kind(numbers)
        elif rnum.count(2) == 4:
            handtype = 'two pair'
            score = _check_two_pair(numbers)
        elif rnum.count(2) == 2:
            handtype = 'pair'
            score = _check_pair(numbers)
        else:
            handtype = 'flush'
            score = 75 + max(numbers) / 100
    elif 4 in rnum:
        handtype = 'four of a kind'
        score = _check_four_of_a_kind(numbers)
    elif sorted(rnum) == [2, 2, 3, 3, 3]:
        handtype = 'full house'
        score = _check_full_house(numbers)
    elif 3 in rnum:
        handtype = 'three of a kind'
        score = _check_three_of_a_kind(numbers)
    elif rnum.count(2) == 4:
        handtype = 'two pair'
        score = _check_two_pair(numbers)
    elif rnum.count(2) == 2:
        handtype = 'pair'
        score = _check_pair(numbers)
    elif dif == 4:
        handtype = 'straight'
        score = 65 + max(numbers)

    else:
        handtype = 'high card'
        n = sorted(numbers, reverse=True)
        score = n[0] + n[1] / 100 + n[2] / 1000 + n[3] / 10000 + n[4] / 100000

    return handtype,score

def _generate_hand_scores():

    print('generating hands...')

    hands = possible_hands(cards, 5)

    hands_set = [set(x) for x in hands]

    results = [_hands_score(x) for x in hands]

    names = [i[0] for i in results]

    scores = [i[1] for i in results]

    df = DataFrame({'hands': hands_set})

    df['name'] = names
    df['score'] = scores

    print(f'saving hands to {hand_scores_filepath}')

    df.to_pickle(hand_scores_filepath)

    return df

def fetch_scores():

    try:
        print('attempting to fetch pre-calculated scores...')

        start = time.perf_counter()
        result = read_pickle(hand_scores_filepath)
        time_elapsed = time.perf_counter() - start
        print(f"Function: Read_scores, Time: {time_elapsed}")

        return result

    except:
        print('failed; re-generating hand scores...')
        return _generate_hand_scores()


if __name__ == '__main__':

    df = _generate_hand_scores()

    df