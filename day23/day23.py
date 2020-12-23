
class CupNode:
    def __init__(self, label):
        self.label = label
        self.nextNode = None

    def __repr__(self):
        return f"Cup({self.label})"

def print_cups(cup):
    start_label = cup.label
    cup_str = ""
    while True:
        cup_str += str(cup.label)
        cup = cup.nextNode
        if cup.label == start_label:
            break
        cup_str += " "
    print(cup_str)

def make_move(current_cup: CupNode, cups_map, nCups):
    # print_cups(current_cup)
    following_cup = current_cup.nextNode
    current_cup.nextNode = following_cup.nextNode.nextNode.nextNode
    following_cup.nextNode.nextNode.nextNode = None
    following_cup_labels = [following_cup.label, following_cup.nextNode.label, following_cup.nextNode.nextNode.label]
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
    after_cup = destination_cup.nextNode
    destination_cup.nextNode = following_cup
    following_cup.nextNode.nextNode.nextNode = after_cup

def make_cups(input, cups_map):
    first_cup = None
    prev_cup = None
    cup = None
    for cup_str in list(input):
        label = int(cup_str)
        cup = CupNode(label)
        cups_map[label] = cup
        if prev_cup:
            prev_cup.nextNode = cup
        # Set current cup to the first cup
        if not first_cup:
            first_cup = cup
        prev_cup = cup
    cup.nextNode = first_cup
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
        curr_cup = curr_cup.nextNode
        # print(cups, index)

    cup = cups_map[1].nextNode

    print_cups(cup)
    answer = ""
    while cup.label != 1:
        answer += str(cup.label)
        cup = cup.nextNode

    print("Answer 1", answer)

    # part 2

    # Reset cups
    cups_map = {}
    first_cup = make_cups(input, cups_map)

    curr_cup = first_cup
    for _ in range(10000000):
        make_move(curr_cup, cups_map, 9)
        curr_cup = curr_cup.nextNode
        # print(cups, index)

    # cups = [int(cup) for cup in list(input)]
    # remaining_cups = range(len(cups)+1, 1000001)
    # cups = cups + list(remaining_cups)
    # print(len(cups))
    # print(cups[-1])
    #
    # for i in range(1000):
    #     index = make_move(cups, in)
    #     if i % 100 == 0:
    #         print(i)
    #     # print(cups, index)
