def recursive_combat(decks):
    seen_decks = []
    #print(f"recursive_combat {decks}")
    while True:
        #print(f"Decks {decks}")
        if not decks[0]:
            return 1
        if not decks[1]:
            return 0
        if decks in seen_decks:
            #print("Seen decks", decks)
            return 0 # player 1 in winner
        seen_decks.append([deck.copy() for deck in decks])
        combat_cards = [deck.pop() for deck in decks]
        # for i in range(2):
        #     print(f"Player {i} plays {combat_cards[i]}")
        can_play = [len(decks[i]) >= combat_cards[i] for i in range(2)]
        if can_play[0] and can_play[1]:
            winner = recursive_combat([decks[i][-combat_cards[i]:] for i in range(2)])
        else:
            winner = combat_cards.index(max(combat_cards))
        if winner == 0:
            for combat_card in combat_cards:
                decks[0].insert(0, combat_card)
        else:
            for combat_card in combat_cards[::-1]:
                decks[1].insert(0, combat_card)



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
                deck.insert(0, int(line))
    decks.append(deck)
    print(decks)

    decks1 = [deck.copy() for deck in decks]
    print(decks1)
    while(True):
        # print(decks)
        combat_cards = [deck.pop() for deck in decks1]
        # print("Combat cards:", combat_cards)
        if combat_cards[0] > combat_cards[1]:
            for combat_card in combat_cards:
                decks1[0].insert(0, combat_card)
        else:
            for combat_card in combat_cards[::-1]:
                decks1[1].insert(0, combat_card)
        if [] in decks1:
            break

    winner = [deck for deck in decks1 if deck != []][0]
    print("Winner:", winner)

    score = 0
    for i, card in enumerate(winner):
        score += (i + 1)*card

    print("Score1: ", score)

    # part 2

    winner = recursive_combat(decks)
    print(winner)
    print(decks[winner])
    score = 0
    for i, card in enumerate(decks[winner]):
        score += (i + 1)*card

    print("Score2: ", score)

