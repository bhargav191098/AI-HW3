from sympy.logic.boolalg import to_cnf


sentence = "~(a|b&c)"

print(to_cnf(sentence))
