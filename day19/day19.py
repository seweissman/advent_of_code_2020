def expand_rules(rule, rules):
    # print(f"expand_rules {rule}")
    if type(rule) == str and rule not in rules:
        return rule
    if type(rule) == str and rule in rules:
        return expand_rules(rules[rule], rules)
    if type(rule) == tuple:
        return tuple([expand_rules(x, rules) for x in rule])
    new_rule = rule.copy()
    for i,c in enumerate(rule):
        if type(c) is tuple:
            new_rule[i] = expand_rules(c, rules)
        elif c in rules:
            new_rule[i] = expand_rules(rules[c], rules)
    return new_rule


def matches_rule(rule, input, i=0):
    #print(f"matches_rule {input} {i} {rule}")
    if rule == ():
        return True, 0
    if rule == []:
        return False, 0
    if type(rule) is str:
        return input[i].startswith(rule), len(rule)
    if type(rule) is list:
        is_match, len_match = matches_rule(rule[0], input, i)
        if is_match:
            return is_match, len_match
        else:
            return matches_rule(rule[1:], input, i)
        return is_match or matches_rule(rule[1:], input, i)[0]
    if type(rule) is tuple:
        is_match, len_match = matches_rule(rule[0], input, i)
        is_match_rest, len_match_rest = matches_rule(rule[1:], input, i + len_match)
        return is_match and is_match_rest, len_match + len_match_rest

if __name__ == "__main__":
    with open("input-test2.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    # lines.append("8: 42 | 42 8")
    # lines.append("11: 42 31 | 42 11 31")

    rules = {}
    for i in range(0, len(lines)):
        line = lines[i]
        if line == "":
            break
        num, rule = line.split(": ")

        if rule.startswith("\""):
            rules[num] = (rule[1:2],)
        else:
            rule_list = [tuple(clause.split(" ")) for clause in rule.split(" | ")]
            rules[num] = rule_list

    inputs = lines[i+1:]

    print(rules)
    print(inputs)

    rule0 = rules["0"]
    print("rule0", rule0)
    new_rule = expand_rules(rule0, rules)
    print("expand rule0:", new_rule)

    match_ct = 0
    for input in inputs:
        is_match, len_match = matches_rule(new_rule, input)
        if is_match and len_match == len(input):
            match_ct += 1
            print(f"input {input} is match")
    print("answer:", match_ct)
    # (a', [([aa, bb], [ab, ba]), ([ab, ba], [aa, bb])], b)

    #(a, [([aa, bb], [ab, ba]), ([ab, ba], [aa, bb])], b)
