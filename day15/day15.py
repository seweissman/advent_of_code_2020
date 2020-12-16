from collections import defaultdict



if __name__ == "__main__":
    input = [0, 20, 7, 16, 1, 18, 15]
    # input = [0, 3, 6]
    last_spoken_map = defaultdict(int)
    ct = 0
    for i in range(0, len(input) - 1):
        n = input[i]
        last_spoken_map[n] = i
    n = input[-1]
    ct = i + 1
    while ct < 30000000 - 1:
        # print(ct, n, last_spoken_map)
        if not n in last_spoken_map:
            new_n = 0
        else:
            new_n = ct - last_spoken_map[n]
        last_spoken_map[n] = ct
        n = new_n
        ct += 1
    print(n, ct, new_n)



