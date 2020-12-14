"""

"""
from collections import defaultdict
adaptor_compat_map = defaultdict(set)
if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]
    adaptors = [int(line) for line in lines]
    adaptors.sort()
    adaptors.insert(0, 0)
    last_adaptor = adaptors[-1] + 3
    adaptors.append(last_adaptor)

    diff3_ct = 0
    diff2_ct = 0
    diff1_ct = 0
    for i in range(0,len(adaptors)-1):
        diff = adaptors[i+1] - adaptors[i]
        if diff == 1:
            diff1_ct += 1
        if diff == 3:
            diff3_ct += 1
    print(diff1_ct, diff3_ct)
    print(diff1_ct*diff3_ct)

    # part2
    for i in range(0, len(adaptors) - 1):
        for j in range(i+1, len(adaptors)):
            if adaptors[j] - adaptors[i] <= 3:
                adaptor_compat_map[adaptors[j]].add(adaptors[i])
            else:
                break
    # print(adaptor_compat_map)

    path_ct_map = defaultdict(int)
    path_ct_map[0] = 1

    for adaptor in adaptors[1:]:
        for other_adaptor in adaptor_compat_map[adaptor]:
            path_ct_map[adaptor] += path_ct_map[other_adaptor]
    # print(path_ct_map)
    print(path_ct_map[last_adaptor])
    # print("Paths:", count_paths(last_adaptor))
    print("Done")




