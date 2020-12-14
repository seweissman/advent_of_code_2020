"""
Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?
"""

# import pandas as pd
#
# df1 = pd.read_csv("input.txt")
# df2 = pd.read_csv("input.txt")

if __name__ == "__main__":
    with open("input.txt") as input:
        entries = [int(line.strip()) for line in input.readlines()]
        for a in entries:
            for b in entries:
                if a + b == 2020:
                    print(a, b, a*b)

        for a in entries:
            for b in entries:
                for c in entries:
                    if a + b + c == 2020:
                        print(a,b,c, a*b*c)
