from z3 import *

# List to store all the conditions extracted from the funcs file
conditions = []

with open('funcs.py', 'r') as file:
    cont = file.readlines()
    # For each line in the file, extract the condition if it contains 'if(inp' or 'if((inp'
    for line in cont:
        if("if(inp" in line or "if((inp" in line):
            conditions.append(line[line.find("if(") + 3:line.find("):")])

# Create 26 (length of the string) 7 bit BitVec 
inp = [BitVec(f'arr[{i}]', 7) for i in range(26)]

# New solver object
s = Solver()

# Add each evaluated condition to solver and check
for i in conditions:
    s.add(eval(i))

s.check()

# Create list of 26 0s to contain char values
arr = [0] * 26
# Add each value to the list
for i in str(s.model()).split(',\n'):
    if(i[-1] == ']'):
        exec(i[1:-1])
        break
    exec(i[1:])

# Print pass key
print("[+] PASS KEY: " + "".join([chr(c) for c in arr]))