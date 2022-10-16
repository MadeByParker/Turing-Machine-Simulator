import unittest

def simulate(program, tape, head):
    # program is a list of tuples, (state, input, output, direction, new state)
    tape, state = list(tape), 0
    rules = {r[:2]: r[2:] for r in program}
    while state >= 0:
        output, direction, state = rules[(state, tape[head])]
        tape[head] = output
        if direction == "L":
            if head == 0:
                tape.insert(0, "_")
            head -= 1
        elif direction == "R":
            if head == len(tape) - 1:
                tape.append("_")
            head += 1
    # normalise tape and adjust head position
    tape_length = len(tape)
    tape = "".join(tape).lstrip("_")
    head = head - (tape_length - len(tape)) + 3
    tape = tape.rstrip("_")
    return "__" + tape + "__", head

class TuringMachineTest(unittest.TestCase):
    def test_add(self):
        program = [(0, "1", "1", "R", 0),
                   (0, "+", "1", "R", 1),
                   (1, "1", "1", "R", 1),
                   (1, "_", "_", "L", 2),
                   (2, "1", "_", "L", -1)]
        tape, head = "__111+11111__", 3
        self.assertEquals(simulate(program, tape, head), ("__11111111__", 10))

    def test_multiply(self):
        # only for numbers in Z+
        # basic idea: reduce to summation
        # for each 1 of the second operand, add a copy of the first operand, then sum up all the copies
        program = [(0, "1", "_", "R", 1),    # skip the first 1
                   (1, "*", "_", "R", 10),   # clean up and finish: the left operand reached 0
                   (1, "1", "_", "R", 2),    # decrease the left operand, add a copy of the right operand
                   (2, "1", "1", "R", 2),    # skip stuff
                   (2, "*", "*", "R", 2),
                   (2, "+", "+", "R", 2),
                   (2, "_", "+", "L", 3),    # mark start of the copy
                   (3, "1", "1", "L", 3),    # skip to the beginning of the right operand (or its last copy)
                   (3, "+", "+", "R", 4),    # start copy
                   (3, "*", "*", "R", 4),
                   (4, "1", "0", "R", 5),    # copy
                   (4, "+", "+", "L", 8),    # finish copy
                   (5, "1", "1", "R", 5),
                   (5, "+", "+", "R", 6),
                   (6, "1", "1", "R", 6),
                   (6, "_", "1", "L", 7),    # continue writing the copy at the end of the tape
                   (7, "1", "1", "L", 7),    # go back for another 1
                   (7, "+", "+", "L", 7),
                   (7, "0", "0", "R", 4),
                   (8, "0", "1", "L", 8),    # clean up: replace 0s with 1s
                   (8, "+", "+", "L", 9),    # restart the cycle
                   (8, "*", "*", "L", 9),
                   (9, "+", "+", "L", 9),    # go to the beginning of the left operand
                   (9, "*", "*", "L", 9),
                   (9, "1", "1", "L", 9),
                   (9, "_", "_", "R", 1),    # restart
                   (10, "1", "_", "R", 11),  # sum up everything and exit
                   (11, "1", "1", "R", 11),
                   (11, "+", "1", "L", 12),
                   (11, "_", "1", "S", -1),
                   (12, "1", "1", "L", 12),
                   (12, "_", "_", "R", 10)]
        tape, head = "__111*11111__", 3
        self.assertEquals(simulate(program, tape, head), ("__111*11111__", 14))

if __name__ == "__main__":
    unittest.main()