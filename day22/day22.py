from collections import deque
import itertools
from datetime import datetime


def recursive_combat(decks):
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
    print(decks)

    decks1 = [deque(deck) for deck in decks]
    print(decks)
    while(True):
        # print(decks)
        combat_cards = [deck.popleft() for deck in decks1]
        # print("Combat cards:", combat_cards)
        if combat_cards[0] > combat_cards[1]:
            for combat_card in combat_cards:
                decks1[0].append(combat_card)
        else:
            for combat_card in combat_cards[::-1]:
                decks1[1].append(combat_card)
        if deque([]) in decks1:
            break

    winner = [deck for deck in decks1 if deck != deque([])][0]
    print("Winner:", winner)

    score = 0
    for i, card in enumerate(winner):
        score += (len(winner) -i)*card

    print("Score1: ", score)

    start = datetime.now()
    # part 2
    decks2 = [deque(deck) for deck in decks]
    winner = recursive_combat(decks2)
    print(winner)
    print(decks2[winner])
    score = 0
    for i, card in enumerate(decks2[winner]):
        score += (len(decks2[winner]) - i)*card

    print("Score2: ", score)
    end = datetime.now()
    print("Time: ", end - start)

