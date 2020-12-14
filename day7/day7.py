"""
--- Day 7: Handy Haversacks ---
You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)

--- Part Two ---
It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

faded blue bags contain 0 other bags.
dotted black bags contain 0 other bags.
vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
"""

import re
from collections import defaultdict

if __name__ == "__main__":
    with open("input.txt") as input:
        rules = input.readlines()
        rules = [rule.strip() for rule in rules]
    bag_contained_by_map = defaultdict(set)
    bag_contains_map = defaultdict(set)
    for rule in rules:
        if re.match(r".*no other bags.*", rule):
            continue
        # print(rule)
        (outer_bag, inner_bag_list) = rule.split(" contain ")
        inner_bag_list = inner_bag_list.split(", ")
        outer_bag = re.match("(.*) bags", outer_bag).group(1)
        for inner_bag in inner_bag_list:
            m = re.match(r"(\d+) (.+) bags?", inner_bag)
            bag_count = int(m.group(1))
            bag_color = m.group(2)
            bag_contained_by_map[bag_color].add(outer_bag)
            bag_contains_map[outer_bag].add((bag_count, bag_color))
    before_set = {}
    after_set = bag_contained_by_map["shiny gold"]
    while len(after_set) > len(before_set):
        before_set = after_set
        for bag in before_set:
            after_set = after_set.union(bag_contained_by_map[bag])
    print(len(after_set))


    # part 2
    print(bag_contains_map["shiny gold"])
    def count_bags(bag):
        if not bag_contains_map[bag]:
            return 0
        inner_bags = bag_contains_map[bag]
        bag_ct = 0
        for n, inner_bag in inner_bags:
            bag_ct += n
            bag_ct += n*count_bags(inner_bag)
        return bag_ct

    print("shiny gold", count_bags("shiny gold"))
    print("faded blue", count_bags("faded blue"))
    print("dotted black", count_bags("dotted black"))
    print("vibrant plum", count_bags("vibrant plum"))
    print("dark olive", count_bags("dark olive"))


