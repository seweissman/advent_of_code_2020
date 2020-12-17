from collections import defaultdict

def check_constraints(constraints, val):
    """Check if val matches any of the given constraints"""
    for c_list in constraints.values():
        for c_low, c_high in c_list:
            if c_low <= val <= c_high:
                return True
    return False

def find_matching_fields(constraints, val):
    """Find the set of fields that val is consistent with based on the given constraints"""
    matching_fields = set()
    for field, c_list in constraints.items():
        for c_low, c_high in c_list:
            if c_low <= val <= c_high:
                matching_fields.add(field)
    return matching_fields


def simplify_index_constraints(index_constraints):
    """Iterate through the constraints, reducing possibilities
    based on fields that have been constrained to a single value
    e.g. if index_constraints[i] = {"field1"} and
            index_constraints[j] = {"field1", "field2"}
         then we remove "field1" from index_constraints[j]
    """
    while True:
        changed = False
        for i, c_set in index_constraints.items():
            if len(c_set) == 1:
                for j, other_c_set in index_constraints.items():
                    if j != i:
                        len_before = len(index_constraints[j])
                        index_constraints[j] = index_constraints[j].difference(c_set)
                        len_after = len(index_constraints[j])
                        if len_before != len_after:
                            changed = True
        if not changed:
            break

if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    constraints = defaultdict(list)
    for i in range(0, len(lines)):
        line = lines[i]
        if line == "":
            break
        field, constraint_list = line.split(": ")
        for constraint in constraint_list.split(" or "):
            c_low, c_high = constraint.split("-")
            constraints[field].append((int(c_low), int(c_high)))

    my_ticket = [int(val) for val in lines[i+2].split(",")]

    # Save valid tickets for part2
    valid_tickets = []
    error_rate = 0
    for j in range(i+5, len(lines)):
        line = lines[j]
        ticket = [int(val) for val in line.split(",")]
        is_valid = True
        for val in ticket:
            if not check_constraints(constraints, val):
                # If any value has no matching constraints then the ticket is invalid
                is_valid = False
                error_rate += val
        if is_valid:
            valid_tickets.append(ticket)

    print(f"Error rate {error_rate}")

    # part 2

    all_fields = set(constraints.keys())
    # Map from index i to the set of constraints that are possible for this index
    index_constraints = defaultdict(lambda: all_fields.copy())

    for ticket in valid_tickets:
        for i in range(0, len(ticket)):
            val = ticket[i]
            matching_fields = find_matching_fields(constraints, val)
            index_constraints[i] = index_constraints[i].intersection(matching_fields)
        simplify_index_constraints(index_constraints)
    simplify_index_constraints(index_constraints)
    print(index_constraints)

    prod = 1
    for i, field in index_constraints.items():
        field = field.pop()
        if field.startswith("departure"):
            prod *= my_ticket[i]

    print(prod)




