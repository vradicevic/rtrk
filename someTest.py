

testString = "[HOST ] BMA:Frame=1 Time=2"

words = testString.split()

worden = words[2].split("=")
print(worden[1])