from collections import deque
import itertools
from datetime import datetime


def combat(decks):
    """Regular combat"""
    while True:
        if not decks[0]:
            return 1
        if not decks[1]:
            return 0
        # print(decks)
        combat_cards = [deck.popleft() for deck in decks1]
        # print("Combat cards:", combat_cards)
        if combat_cards[0] > combat_cards[1]:
            for combat_card in combat_cards:
                decks1[0].append(combat_card)
        else:
            for combat_card in combat_cards[::-1]:
                decks1[1].append(combat_card)


def recursive_combat(decks):
    """Recursive Combat"""
    seen_decks = set()
    #print(f"recursive_combat {decks}")
    while True:
        #print(f"Decks {decks}")
        if not decks[0]:
            return 1
        if not decks[1]:
            return 0
        if str(decks) in seen_decks:
            #print("Seen decks", decks)
            return 0 # recursion break: player 1 is winner
        seen_decks.add(str(decks))
        combat_cards = [deck.popleft() for deck in decks]
        # for i in range(2):
        #     print(f"Player {i} plays {combat_cards[i]}")
        can_play = [len(decks[i]) >= combat_cards[i] for i in range(2)]
        if can_play[0] and can_play[1]:
            new_decks = [deque(itertools.islice(decks[i], 0, combat_cards[i])) for i in range(2)]
            winner = recursive_combat(new_decks)
        else:
            winner = combat_cards.index(max(combat_cards))
        if winner == 0:
            for combat_card in combat_cards:
                decks[0].append(combat_card)
        else:
            for combat_card in combat_cards[::-1]:
                decks[1].append(combat_card)


def score_deck(deck):
    score = 0
    for i, card in enumerate(deck):
        score += (len(deck) - i)*card
    return score


if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    deck = None
    decks = []
    for line in lines:
        if line.startswith("Player"):
            if deck:
                decks.append(deck)
            deck = []
        else:
            if line != "":
                deck.append(int(line))
    decks.append(deck)

    # part 2
    decks1 = [deque(deck) for deck in decks]
    winner = combat(decks1)
    score = score_deck(decks1[winner])
    print("Score1: ", score)

    # part 2
    start = datetime.now()
    decks2 = [deque(deck) for deck in decks]
    winner = recursive_combat(decks2)
    score = score_deck(decks2[winner])
    print("Score2: ", score)

    end = datetime.now()
    print("Part 2 time: ", end - start)

