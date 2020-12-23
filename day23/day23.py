
class Cup:
    def __init__(self, label):
        self.label = label
        self.nextCup = None

    def __repr__(self):
        return f"Cup({self.label})"

def print_cups(cup):
    start_label = cup.label
    cup_str = ""
    while True:
        cup_str += str(cup.label)
        cup = cup.nextCup
        if cup.label == start_label:
            break
        cup_str += " "
    print(cup_str)

def make_move(current_cup: Cup, cups_map, nCups):
    # print_cups(current_cup)
    following_cup = current_cup.nextCup
    current_cup.nextCup = following_cup.nextCup.nextCup.nextCup
    following_cup.nextCup.nextCup.nextCup = None
    following_cup_labels = [following_cup.label, following_cup.nextCup.label, following_cup.nextCup.nextCup.label]
    # print(f"pick up: {following_cup_labels}")
    destination_label = current_cup.label - 1
    if destination_label == 0:
        destination_label = nCups

    while destination_label in following_cup_labels:
        destination_label -= 1
        if destination_label == 0:
            destination_label = nCups
    # print("destination:", destination_label, "\n")

    destination_cup = cups_map[destination_label]
    after_cup = destination_cup.nextCup
    destination_cup.nextCup = following_cup
    following_cup.nextCup.nextCup.nextCup = after_cup

def make_cups(input, cups_map, extend=None):
    first_cup = None
    prev_cup = None
    cup = None
    max_label = 0
    for cup_str in list(input):
        label = int(cup_str)
        if label > max_label:
            max_label = label
        cup = Cup(label)
        cups_map[label] = cup
        if prev_cup:
            prev_cup.nextCup = cup
        # Set current cup to the first cup
        if not first_cup:
            first_cup = cup
        prev_cup = cup

    # for part 2
    if extend:
        for i in range(max_label + 1, extend + 1):
            cup = Cup(i)
            cups_map[i] = cup
            prev_cup.nextCup = cup
            prev_cup = cup

    cup.nextCup = first_cup
    return first_cup

if __name__ == "__main__":
    test_input = "389125467"
    #input = test_input
    input = "716892543"

    cups_map = {}
    first_cup = make_cups(input, cups_map)
    # Make this list circular
    print_cups(first_cup)

    curr_cup = first_cup
    for _ in range(100):
        make_move(curr_cup, cups_map, 9)
        curr_cup = curr_cup.nextCup
        # print(cups, index)

    cup1 = cups_map[1]

    print_cups(cup1)
    answer = ""
    cup = cup1.nextCup
    while cup.label != 1:
        answer += str(cup.label)
        cup = cup.nextCup

    print("Answer 1", answer)

    # part 2

    # Reset cups
    cups_map = {}
    first_cup = make_cups(input, cups_map, extend=1000000)

    curr_cup = first_cup
    for i in range(10000000):
        make_move(curr_cup, cups_map, 1000000)
        curr_cup = curr_cup.nextCup
        if i % 1000000 == 0:
            print("At move: ", i)
        # print(cups, index)

    cup1 = cups_map[1]
    print("Answer2", cup1.nextCup.label*cup1.nextCup.nextCup.label)
