"""
--- Day 14: Docking Data ---
As your ferry approaches the sea port, the captain asks for your help again. The computer system that runs this port isn't compatible with the docking program on the ferry, so the docking parameters aren't being correctly initialized in the docking program's memory.

After a brief inspection, you discover that the sea port's computer system uses a strange bitmask system in its initialization program. Although you don't have the correct decoder chip handy, you can emulate it in software!

The initialization program (your puzzle input) can either update the bitmask or write a value to memory. Values and memory addresses are both 36-bit unsigned integers. For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory address 8.

The bitmask is always given as a string of 36 bits, written with the most significant bit (representing 2^35) on the left and the least significant bit (2^0, that is, the 1s bit) on the right. The current bitmask is applied to values immediately before they are written to memory: a 0 or 1 overwrites the corresponding bit in the value, while an X leaves the bit in the value unchanged.

For example, consider the following program:

mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
This program starts by specifying a bitmask (mask = ....). The mask it specifies will overwrite two bits in every written value: the 2s bit is overwritten with 0, and the 64s bit is overwritten with 1.

The program then attempts to write the value 11 to memory address 8. By expanding everything out to individual bits, the mask is applied as follows:

value:  000000000000000000000000000000001011  (decimal 11)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001001001  (decimal 73)
So, because of the mask, the value 73 is written to memory address 8 instead. Then, the program tries to write 101 to address 7:

value:  000000000000000000000000000001100101  (decimal 101)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001100101  (decimal 101)
This time, the mask has no effect, as the bits it overwrote were already the values the mask tried to set. Finally, the program tries to write 0 to address 8:

value:  000000000000000000000000000000000000  (decimal 0)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001000000  (decimal 64)
64 is written to address 8 instead, overwriting the value that was there previously.

To initialize your ferry's docking program, you need the sum of all values left in memory after the initialization program completes. (The entire 36-bit address space begins initialized to the value 0 at every address.) In the above example, only two values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.

Execute the initialization program. What is the sum of all values left in memory after it completes?

"""
import re

memory = {}

def to_bit_str(i, l):
    i_bin = format(i, f"0{l}b")
    return i_bin

if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]

    # print(lines)

    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
            # print(mask)
            mask = [(i, bit) for i, bit in enumerate(mask) if bit != "X"]
            # print(mask)

        if line.startswith("mem"):
            m = re.match(r"^mem\[(\d+)\] = (\d+)$", line)
            loc = int(m.group(1))
            val = int(m.group(2))
            val_bin = to_bit_str(val, 36)
            # print(val)
            # print(val_bin)
            val_bin = list(val_bin)
            for i, bit in mask:
                val_bin[i] = bit
            val_bin = "".join(val_bin)
            val = int(val_bin, 2)
            memory[loc] = val

    print(sum(memory.values()))
    # part 2

    memory = {}
    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
            print(mask)
            mask_1 = [(i, bit) for i, bit in enumerate(mask) if bit == "1"]
            mask_x = [(i, bit) for i, bit in enumerate(mask) if bit == "X"]
            print(mask)


        if line.startswith("mem"):
            m = re.match(r"^mem\[(\d+)\] = (\d+)$", line)
            loc = int(m.group(1))
            val = int(m.group(2))
            loc_bin = to_bit_str(loc, 36)
            # print(loc_bin)
            loc_bin = list(loc_bin)
            for i, bit in mask_1:
                loc_bin[i] = bit
            # print(mask_x, len(mask_x))
            for i in range(0, 2**len(mask_x)):
                loc_new = loc_bin.copy()
                bits = to_bit_str(i, len(mask_x))
                bits = list(bits)
                # print("bits", i, bits)
                for j in range(0, len(bits)):
                    k, _ = mask_x[j]
                    loc_new[k] = bits[j]
                loc_new = "".join(loc_new)
                loc_new = int(loc_new, 2)
                memory[loc_new] = val
                # print("\t", loc_new)

    print(sum(memory.values()))