import operator


def parse_list(expr):
    l = []
    if not expr:
        return l, expr
    while expr:
        s = expr.pop()
        if s == "(":
            subl, rest = parse_list(expr)
            l.append(subl)
            expr = rest
        elif s == ")":
            return l, expr
        else:
            l.append(s)
    return l, expr

def eval_expr(expr):
    if not expr:
        return 0
    op = None
    val = None
    operand = None
    for s in expr:
        if type(s) == list:
            operand = eval_expr(s)
        elif s == "+":
            op = operator.add
        elif s == "*":
            op = operator.mul
        else:
            operand = int(s)
        if operand and val is None:
            val = operand
            operand = None
        if operand and op:
            val = op(val, operand)
            op = None
            operand = None
    return val

def eval_expr2_helper(expr):
    #print(f"eval_expr2 {expr}")
    if not expr:
        return 0
    if type(expr) is not list:
        return int(expr)
    if len(expr) == 1:
        return eval_expr2_helper(expr[0])
    lhs = None
    op = None
    rhs = None
    newl = []
    while expr:
        s = expr.pop()
        if s == "+" or s == "*":
            op = s
        else:
            if lhs is None:
                lhs = eval_expr2_helper(s)
            elif rhs is None:
                rhs = eval_expr2_helper(s)
        #print(f"={expr} {s}, {op}, {lhs}, {rhs}, {newl}")
        if lhs and op and rhs:
            if op == "*":
                if type(lhs) is int and type(rhs) is int and expr == []:
                    newl.insert(0,(lhs * rhs))
                    op = None
                    lhs = None
                    rhs = None
                else:
                    newl.insert(0,lhs)
                    newl.insert(0,op)
                    lhs = rhs
                    op = None
                    rhs = None
            if op == "+":
                if type(lhs) is int and type(rhs) is int:
                    lhs = lhs + rhs
                    op = None
                    rhs = None
                else:
                    #newl.insert(0,[rhs, op, lhs])
                    lhs = [rhs, op, lhs]
                    op = None
                    rhs = None
    if op:
        newl.insert(0, op)
    if rhs or lhs:
        newl.insert(0, rhs or lhs)
    #print(newl)
    return newl

def eval_expr2(expr):
    while True:
        before_expr = expr.copy()
        after_expr = eval_expr2_helper(expr)
        if after_expr == before_expr or type(after_expr) is int:
            return after_expr
        expr = after_expr

def to_expr_list(input_str):
    expr = [s for s in list(input_str) if s != " "]
    expr.reverse()
    expr, _ = parse_list(expr)
    return expr


if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    input_test1 = "1 + (2 * 3) + (4 * (5 + 6))"
    expr = to_expr_list(input_test1)
    assert(eval_expr(expr) == 51)
    assert(eval_expr2(expr) == 51)

    input_test2 = "1 + 2 * 3 + 4 * 5 + 6"
    expr = to_expr_list(input_test2)
    assert(eval_expr(expr) == 71)
    assert(eval_expr2(expr) == 231)

    input_test3 = "2 * 3 + (4 * 5)"
    expr = to_expr_list(input_test3)
    print(expr)
    assert(eval_expr(expr) == 26)
    assert(eval_expr2(expr) == 46)

    input_test4 = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
    expr = to_expr_list(input_test4)
    assert(eval_expr(expr) == 437)
    assert(eval_expr2(expr) == 1445)

    input_test5 = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
    expr = to_expr_list(input_test5)
    assert(eval_expr(expr) == 12240)
    assert(eval_expr2(expr) == 669060)

    input_test6 = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
    expr = to_expr_list(input_test6)
    assert(eval_expr(expr) == 13632)
    assert(eval_expr2(expr) == 23340)

    answer1 = sum([eval_expr(to_expr_list(line)) for line in lines])
    print(answer1)

    # part 2

    answer2 = sum([eval_expr2(to_expr_list(line)) for line in lines])
    print(answer2)

