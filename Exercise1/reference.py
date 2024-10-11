from oxidd.bdd import BDDManager

# Create a manager for up to 100,000,000 nodes with an apply cache for
# 1,000,000 entries and 1 worker thread
manager = BDDManager(100_000_000, 1_000_000, 1)

# Create 10 variables
x = [manager.new_var() for i in range(5)]

'''assert (x[0] & x[1]).satisfiable()
assert (x[0] & ~x[0]).sat_count_float(2) == 0
'''

'''assert (~x[2] or ~x[4]).satisfiable()
assert (x[1] or x[2] or x[4]).satisfiable()'''

'''Formula f1 = p.parse("A & (B | C)");
Formula f2 = p.parse("B | D");
Formula f3 = p.parse("~A | B & E");'''








( (x[0] & (x[1] or x[2]) ) & (x[1] or x[2]) & (~x[0] or (x[1] and x[4]) ) ).sat_count_float(5)
assert (x[0] or x[1] or ~x[2]).satisfiable()
assert (~x[0] or x[2]).satisfiable()


((x[1] or x[2] or x[4])&(~x[2] or ~x[4])).sat_count_float(5)
(x[1] & x[2] & x[4] & x[3] & x[0]).sat_count_float(5)

((x[0] or x[1] or ~x[2])&(~x[0] or x[2])).sat_count_float(3)

print()