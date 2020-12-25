


def transform(n, subject):
    return (n * subject) % 20201227


if __name__ == "__main__":

    subject = 7
    input = (2069194, 16426071)
    test_input = (5764801, 17807724)
    card_pk, door_pk = input

    # card loop size
    i = 0
    n = 1
    while n != card_pk:
        n = transform(n, subject)
        i += 1
    card_loop_size = i
    print("Card loop size", i)

    # door loop size
    # i = 0
    # n = 1
    # while n != door_pk:
    #     n = transform(n, subject)
    #     i += 1
    # door_loop_size = i
    # print("Door loop size", i)


    encryption_key = door_pk
    n = 1
    for i in range(card_loop_size):
        n = transform(n, encryption_key)

    print("Answer 1:", n)