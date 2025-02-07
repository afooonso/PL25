import fileinput

stdin = "".join(fileinput.input())
total = 0 
i = 0
value = 0
active = 0  # Start inactive to allow summing numbers by default

while i < len(stdin):
    if stdin[i] in "0123456789" and active == 1:
        while i < len(stdin) and stdin[i] in "0123456789":
            value = value * 10 + int(stdin[i])
            i += 1
        total += value
        value = 0
        continue 

    else:
        
        if i + 3 <= len(stdin) and stdin[i:i+3].lower() == "off" and (i == 0 or not stdin[i - 1].isalnum()) and (i + 3 == len(stdin) or not stdin[i + 3].isalnum()):
            active = 0
            i += 2

        elif i + 2 <= len(stdin) and stdin[i:i+2].lower() == "on" and (i == 0 or not stdin[i - 1].isalnum()) and (i + 2 == len(stdin) or not stdin[i + 2].isalnum()):
            active = 1
            i += 1

        elif stdin[i] == '=':
            print(f"Total: {total}")

        value = 0 

    i += 1 