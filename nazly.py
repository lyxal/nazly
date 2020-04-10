# naz but it's python -> naz.ly (no points for guessing why it's called that)
# credit to sporeball for original js interpreter
# ported by Lyxal, because transilteration programs just don't cut it
# also, this isn't a direct port because JS is weird. Like really weird.
# I spelled weird correctly, didn't I?

import string
import textwrap
import re
import sys



filename = ""
opcode = register = 0

num = fnum = vnum = 0

jnum = 0
cnum = None

i = 0
line = col = 1

prog_input = input()

halt = func = False

def run_step(letter):
    global prog_input
    global register
    global num, fnum, vnum, jnum, cnum
    global halt, func, opcode

    # WARNING: Always read the entire program before porting

    if letter == "a":
        register += num

    elif letter == "d":
        register //= num

    elif letter == "m":
        register *= num

    elif letter == "s":
        register -= num

    elif letter == "p":
        register %= num

    elif letter == "f":
        fnum = num
        if opcode in [0, 3]:
            if not functions[fnum]:
                raise SyntaxError("Use of undeclared function")

            for i in range(0, len(functions[fnum]) + 1, 2):
                val = functions[fnum][i:i+2]
                num, instruction = val
                num = int(num)
                run_step(letter)
        elif opcode == 1:
            func = True


    elif letter == "h":
        halt = True # I woulda exit()'d, but I didn't
        return

    elif letter == "o":
        for _ in range(num):
            print(chr(register) if chr(register) in string.printable\
        else register, end="")

        # Because who uses output variables anyway?

    elif letter == "v":
        vnum = num
        if opcode == 0:
            if variables[vnum] is None:
                # None, because -999 is valid in naz.ly
                raise NameError("Variable is not defined")
                # Because python has proper errors.

            register = variables[vnum]
        elif opcode == 2:
            variables[vnum] = register
            opcode = 0

        elif opcode == 3:
            if variables[vnum] is None:
                # None, because -999 is valid in naz.ly
                raise NameError("Variable is not defined")
                # Because python has proper errors.

            cnum = variables[vnum]

    if letter in "leg":
        if opcode != 3:
            raise SyntaxError("Conditionals must be run in opcode 3")

        if cnum is None:
            raise ValueError("Number to check against must be defined")

        jnum = num

    elif letter == "l":
        if register < cnum: conditional()

    elif letter == "e":
        if reigster == cnum: conditional()

    elif letter == "g":
        if register > cnum: conditional()

    elif letter == "n":
        if variables[num] is None:
            raise NameError("Variable is not defined")

        variables[num] *= -1 # Hehe.

    elif letter == "r":
        if not prog_input:
            raise EOFError("EOI when reading input")

        if len(prog_input) < num:
            raise EOFError("EOI when reading input")
            # Because indexing too far raises an error. :'(

        register = ord(prog_input[num - 1]) # Hooray for built-ins!
        prog_input = prog_input[:num - 1] + prog_input[num:]

    elif letter == "x":
        if num > 3:
            raise SyntaxError("Invalid opcode")

        opcode = num

functions = dict(zip(range(0, 10), ["" for n in range(0,10)]))
variables = dict(zip(range(0, 10), [None for n in range(0,10)]))
# I'm lazy and I didn't want to write two 10 line dictionaries.

def conditional():
    global opcode
    global num
    global cnum

    opcode = 0
    num = jnum
    run_step("f")
    cnum = None

if __name__ == "__main__":
    sys.setrecursionlimit(10000) # Because 1000 calls is for the weak

    command_pobj = re.compile(r"\d[admspfhovlegnrx]") #o.o Regex!

    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("file", help="The location of the naz file to open")
        # Yes, stolen right from Keg. Shuddup about it.

        # Place flags here using the good 'ol parser.add_argument chain

        args = parser.parse_args()
        loc = args.file

    else:
        loc = input("Enter the file location of the naz program: ")

    code = open(loc).read().replace("\n", "")

    code = textwrap.wrap(code, 2)

    while i < len(code):
        if code[i] == "\r\n":
            func = False
            line += 1
            col = 1

            if opcode == 1: opcode = 0

        if code[i] == "0x":
            func = False

        if not command_pobj.findall(code[i]):
            print(code[i])
            raise SyntaxError("Invalid command")

        num = int(code[i][0])
        col += 1

        run_step(code[i][1])
        col += 1

        if halt: break
        i += 1
