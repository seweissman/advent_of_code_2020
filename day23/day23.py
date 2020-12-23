
def make_move(cups, current_cup_index):
    current_cup = cups[current_cup_index]
    if current_cup_index+1 < len(cups) - 3:
        following_cups = cups[current_cup_index+1:current_cup_index+4]
    else:
        rest_len = 3 - (len(cups) - current_cup_index - 1)
        following_cups = cups[current_cup_index+1:len(cups)] + cups[0:rest_len]
    # print("pick up:", following_cups)
    destination_cup = current_cup - 1
    if destination_cup == 0:
        destination_cup = len(cups)
    while destination_cup in following_cups:
        destination_cup -= 1
        if destination_cup == 0:
            destination_cup = len(cups)
    # print("destination:", destination_cup, "\n")
    for cup in following_cups:
        cups.remove(cup)
    destination_cup_index = cups.index(destination_cup)
    for cup in following_cups[::-1]:
        cups.insert(destination_cup_index+1, cup)
    current_cup_index = cups.index(current_cup)
    return (current_cup_index + 1) % len(cups)

if __name__ == "__main__":
    test_input = "389125467"
    #input = test_input
    input = "716892543"
    cups = [int(cup) for cup in list(input)]
    print(cups)
    index = 0
    for _ in range(100):
        index = make_move(cups, index)
        # print(cups, index)

    starting_cup = (cups.index(1) + 1) % len(cups)

    answer = ""
    for i in range(len(cups)):
        answer += str(cups[(starting_cup + i)%len(cups)])

    print("Answer 1", answer)

