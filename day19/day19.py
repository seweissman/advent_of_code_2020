
import re
class OrList(list):
    def __repr__(self):
        return "(or " + super().__repr__() + ")"

    def copy(self):
        return OrList(super().copy())

    def __getitem__(self, item):
        if isinstance(item, slice):
            return OrList(super().__getitem__(item))
        return super().__getitem__(item)

class AndList(list):
    def __repr__(self):
        return "(and " + super().__repr__() + ")"

    def copy(self):
        return AndList(super().copy())

    def __getitem__(self, item):
        if isinstance(item, slice):
            return AndList(super().__getitem__(item))
        return super().__getitem__(item)

def apply_sub(sub_rule, l):
    #print(f"apply_sub {sub_rule}, {l} ")

    n, rule = sub_rule
    new_l = l.copy()
    for i in range(0, len(l)):
        #print(f"type {l[i]} is {type(l[i])} {type(new_l)}")
        if type(l[i]) is str and l[i] == n:
            new_l[i] = rule
        elif isinstance(l[i], list):
            new_l[i] = apply_sub(sub_rule, l[i])
    #print(f"apply_sub {sub_rule}, {l} = {new_l}")
    return new_l

def expand_rule(rules, rule):
    new_rule = rule.copy()
    for n, other_rule in rules.items():
        # apply rule to rule
        new_rule = apply_sub((n, other_rule), new_rule)
    return new_rule

def rule_set(rule):
    paren_ct = 0
    rule_set = set()
    for i in range(0, len(rule)):
        #print(rule[i], paren_ct)
        if rule[i] == "(":
            paren_ct += 1
        elif rule[i] == ")":
            paren_ct -= 1
        else:
            if paren_ct == 0 and rule[i] == "|":
                sub_rule = rule[0:i]
                rule_set.add(sub_rule)
    return rule_set
"""

0: 1 2 3
1: a
2: 4 | 5 
3: b
4: d b
5: d 

adb

"""

def matches_rule(seen, rule, input, i=0):
    if i < len(input):
        c = input[i]
    else:
        c = None
    print(f"matches_rule {input} {i} {c} {type(rule)} {rule} ")
    if type(rule) is AndList and len(rule) == 0:
        #print("return True")
        return True, 0
    if type(rule) is OrList and len(rule) == 0:
        return False, 0
    if type(rule) is str:
        if i >= len(input):
            return False, 0
        return input[i].startswith(rule), len(rule)
    if type(rule) is OrList:
        j = 0
        while j < len(rule) and (i, str(rule[j])) in seen:
            j += 1
        if j == len(rule):
            return False, 0
        else:
            seen.add((i, str(rule[j])))

        is_match, len_match = matches_rule(seen, rule[j], input, i)
        if is_match:
            return is_match, len_match
        else:
            return matches_rule(seen, OrList(rule[j+1:]), input, i)
    if type(rule) is AndList:
        is_match, len_match = matches_rule(seen, rule[0], input, i)
        is_match_rest, len_match_rest = matches_rule(seen, AndList(rule[1:]), input, i + len_match)
        return is_match and is_match_rest, len_match + len_match_rest


def search_rule(rules, rule, input, rule_rest=None, i=0):
    if rule_rest is None:
        rule_rest = []
    if i < len(input):
        c = input[i]
    else:
        c = None
    #print(f"search_rule {input} {c} {i} {rule} {rule_rest}")
    if i >= len(input) and rule:
        return False
    if i >= len(input) and not rule and not rule_rest:
        return True
    if type(rule) is AndList and len(rule) == 0:
        if rule_rest == []:
            return True
        return search_rule(rules, rule_rest[0], input, rule_rest=rule_rest[1:], i=i)
    if type(rule) is OrList and len(rule) == 0:
        if i >= len(input):
            return True
        return False
    if type(rule) is str:
        if rule in rules:
            expand_rule = rules[rule]
            return search_rule(rules, expand_rule, input, rule_rest=rule_rest, i=i)
        else:
            if i >= len(input):
                return False
            return input[i].startswith(rule) and search_rule(rules, rule_rest, input, i=i+len(rule))
    if type(rule) is OrList:
        is_match = search_rule(rules, rule[0], input, rule_rest=rule_rest, i=i)
        # match_list = [matches_rule(rules, c, input, i) for c in rule]
        # return match_list
        if is_match: #and search_rule(rules, rule_rest[0], input, rule_rest=rule_rest[1:], i=i):
            #print("Or Match")
            return True
        else:
            return search_rule(rules, OrList(rule[1:]), input, rule_rest=rule_rest, i=i)
    if type(rule) is AndList:
        if rule_rest and len(rule) > 1:
            rule_rest = AndList([rule[1:], rule_rest])
        if not rule_rest and len(rule) > 1:
            rule_rest = rule[1:]
        return search_rule(rules, rule[0], input, rule_rest=rule_rest, i=i)


def matches_rule2(seen, rules, rule, input, rule_rest=None, i=0, prefix=None):
    if rule_rest is None:
        rule_rest = []
    if prefix is None:
        prefix = []
    if i < len(input):
        c = input[i]
    else:
        c = None
    print(f"matches_rule {input} {c} {i} {prefix} {rule}")
    if i >= len(input) and rule:
        return False, 0
    if type(rule) is AndList and len(rule) == ():
        return True, 0
    if type(rule) is OrList and len(rule) == 0:
        if i >= len(input):
            return True, 0
        return False, 0
    if type(rule) is str:
        if rule in rules:
            print(f"rule {rule} in rules")
            prefix.append(rule)
            expand_rule = rules[rule]
            return matches_rule2(seen, rules, expand_rule, input, i, prefix=prefix)
        else:
            if i >= len(input):
                return False, 0
            return input[i].startswith(rule), len(rule)
    if type(rule) is OrList:

        is_match, len_match = matches_rule2(seen, rules, rule[0], input, i, prefix=prefix)
        # match_list = [matches_rule(rules, c, input, i) for c in rule]
        # return match_list
        if is_match:
            #print(f"is match {rule[0]}, {len_match}")
            return is_match, len_match
        else:
            #print("is not match")
            return matches_rule2(seen, rules, OrList(rule[1:]), input, i, prefix=prefix)
    if type(rule) is AndList:
        is_match, len_match = matches_rule2(seen, rules, rule[0], input, i, prefix=prefix)
        rest = rule[1:]
        if is_match:
            if rest:
                is_match_rest, len_match_rest = matches_rule2(seen, rules, AndList(rule[1:]), input, i + len_match, prefix=prefix)
                return is_match and is_match_rest, len_match + len_match_rest
            else:
                return is_match, len_match
        else:
            return False, 0

if __name__ == "__main__":
    with open("input-test2.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    rules = {}
    for i in range(0, len(lines)):
        line = lines[i]
        if line == "":
            break
        num, rule = line.split(": ")
        if num == "8":
            rule = "42 | 42 8"
        if num == "11":
            rule = "42 31 | 42 11 31"
        if rule.startswith("\""):
            rule = rule[1:2]
            rules[num] = rule
        else:
            rule_as_list = [AndList(c.split(" ")) if (len(c.split(" ")) > 1) else c for c in rule.split(" | ") ]
            if len(rule_as_list) == 1:
                rule_as_list = rule_as_list[0]
            else:
                rule_as_list = OrList(rule_as_list)
            rules[num] = rule_as_list

        # print(f"rules[{num}] = {rules[num]}")

    # rules["8"] = "42 | 42 8"
    # rules["11"] = "42 31 | 42 11 31"

    print(rules)
    #print(rules["8"], rules["11"])
    inputs = lines[i+1:]

    #print(rules)
    #print(inputs)

    rule0 = rules["0"]
    part1 = False
    if part1:
        print("rule0", rule0)
        n_expands = 20
        i = 0
        while i < n_expands:
            new_rule0 = expand_rule(rules, rule0)
            if new_rule0 == rule0:
                break
            rule0 = new_rule0
            print("expanded rule0:", new_rule0)
            i += 1


    match_ct = 0
    # inputs = ["aaabbabaaa"]
    # rule0 = ('11', '31')

    # should match
    #inputs = ["bbbbbbbaaaabbbbaaabbabaaa"]
    # shouldn't match
    #inputs = ["aaaabbaaaabbaaa"]
    for input in inputs:
        is_match = search_rule(rules, rule0, input)
        if is_match:
            match_ct += 1
            print(f"input {input} is match")
        else:
            print(f"input {input} is not match")
    print("answer:", match_ct)
    # (a', [([aa, bb], [ab, ba]), ([ab, ba], [aa, bb])], b)

    #(a, [([aa, bb], [ab, ba]), ([ab, ba], [aa, bb])], b)

'aaabbabaaa'