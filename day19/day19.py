
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

def search_rule(rules, rule, input, rule_rest=None, i=0):
    if rule_rest is None:
        rule_rest = []
    # if i < len(input):
    #     c = input[i]
    # else:
    #     c = None
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
        if is_match:
            return True
        else:
            return search_rule(rules, OrList(rule[1:]), input, rule_rest=rule_rest, i=i)
    if type(rule) is AndList:
        if rule_rest and len(rule) > 1:
            rule_rest = AndList([rule[1:], rule_rest])
        if not rule_rest and len(rule) > 1:
            rule_rest = rule[1:]
        return search_rule(rules, rule[0], input, rule_rest=rule_rest, i=i)


if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    rules = {}
    for i in range(0, len(lines)):
        line = lines[i]
        if line == "":
            break
        num, rule = line.split(": ")

        # Rule changes for part 2
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

    inputs = lines[i+1:]

    rule0 = rules["0"]

    match_ct = 0
    for input in inputs:
        is_match = search_rule(rules, rule0, input)
        if is_match:
            match_ct += 1
            print(f"input {input} is match")
        else:
            print(f"input {input} is not match")
    print("answer1:", match_ct)

