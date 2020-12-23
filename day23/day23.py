
class Cup:
    cup_map = {}

    def __init__(self, label):
        self.label = label
        self.next_cup = None
        Cup.cup_map[label] = self

    def __next__(self):
        return self.next_cup

    def set_next(self, cup):
        self.next_cup = cup

    def __repr__(self):
        return f"Cup({self.label})"

    @classmethod
    def by_label(cls, label):
        return cls.cup_map.get(label)

    @classmethod
    def clear(cls):
        cls.cup_map.clear()


def print_cups(cup):
    start_label = cup.label
    cup_str = ""
    while True:
        cup_str += str(cup.label)
        cup = next(cup)
        if cup.label == start_label:
            break
        cup_str += " "
    print(cup_str)

def make_move(current_cup: Cup, n_cups):
    # print_cups(current_cup)
    following_cup = next(current_cup)
    current_cup.set_next(next(next(next(following_cup))))
    next(next(following_cup)).set_next(None)
    following_cup_labels = [following_cup.label, next(following_cup).label, next(next(following_cup)).label]
    # print(f"pick up: {following_cup_labels}")
    destination_label = current_cup.label - 1
    if destination_label == 0:
        destination_label = n_cups

    while destination_label in following_cup_labels:
        destination_label -= 1
        if destination_label == 0:
            destination_label = n_cups
    # print("destination:", destination_label, "\n")

    destination_cup = Cup.by_label(destination_label)
    after_cup = next(destination_cup)
    destination_cup.set_next(following_cup)
    next(next(following_cup)).set_next(after_cup)

def make_cups(input, extend=None):
    Cup.clear()
    first_cup = None
    prev_cup = None
    cup = None
    max_label = 0
    for cup_str in list(input):
        label = int(cup_str)
        if label > max_label:
            max_label = label
        cup = Cup(label)
        if prev_cup:
            prev_cup.set_next(cup)
        # Set current cup to the first cup
        if not first_cup:
            first_cup = cup
        prev_cup = cup

    # for part 2
    if extend:
        for i in range(max_label + 1, extend + 1):
            cup = Cup(i)
            prev_cup.set_next(cup)
            prev_cup = cup

    cup.set_next(first_cup)
    return first_cup

if __name__ == "__main__":
    test_input = "389125467"
    #input = test_input
    input = "716892543"

    first_cup = make_cups(input)
    print_cups(first_cup)

    curr_cup = first_cup
    for _ in range(100):
        make_move(curr_cup, 9)
        curr_cup = next(curr_cup)
        # print(cups, index)

    cup1 = Cup.by_label(1)

    print_cups(cup1)
    answer = ""
    cup = next(cup1)
    while cup.label != 1:
        answer += str(cup.label)
        cup = next(cup)

    print("Answer 1", answer)

    # part 2

    # Reset cups
    first_cup = make_cups(input, extend=1000000)

    curr_cup = first_cup
    for i in range(10000000):
        make_move(curr_cup, 1000000)
        curr_cup = next(curr_cup)
        if i % 1000000 == 0:
            print("At move: ", i)
        # print(cups, index)

    cup1 = Cup.by_label(1)
    print("Answer2", next(cup1).label*next(next(cup1)).label)
