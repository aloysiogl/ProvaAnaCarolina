import os
import sys
from time import sleep


class TuringMachine:
    def __init__(self, init, final, act, tape):
        self.index = 0
        self.state = init
        self.final = final
        self.actions = act
        self.tape = tape

    def compute(self):
        os.system('clear')
        while self.state is not self.final:
            tup = self.actions[self.state][self.tape[self.index]]
            if tup is None:
                break
            print("============================================================")
            print("Current state: ", self.state)
            print("Next state:", tup[1], "Print:", tup[0], "Direction:", tup[2], "Head:", self.index)
            print(" "*(17 + 5*self.index)+ "Y")
            print("Current tape: ", self.tape)
            print("============================================================")
            self.state = tup[1]
            self.tape[self.index] = tup[0]
            if tup[2] == "R":
                self.index += 1
            else:
                self.index -= 1
            sleep(0.5)
            os.system('clear')
        print("Final state", self.state)
        if self.state == self.final:
            print("Accepted =)")
        else:
            print("Denied   =(")


if __name__ == "__main__":
    actions = {"0": {"0": ("0", "0", "R"), "1": ("1", "1", "R"), "B": ("B", 2, "R")}, "1": {"0": ("0", "1", "R"), "1": ("1", "1", "R"),
                                                                            "B": ("B", "2", "R")}}

    machine = TuringMachine("0", "2", actions, list(sys.argv[1]))
    machine.compute()

    actions = {"A": {"0": ("X", "B", "R"), "1": ("X", "C", "R"), "X": ("X", "Z", "R"), "B": ("B", "Z", "R")},
               "B": {"0": ("0", "B", "R"), "1": ("1", "B", "R"), "X": ("X", "D", "L"), "B": ("B", "D", "L")},
               "C": {"0": ("0", "C", "R"), "1": ("1", "C", "R"), "X": ("X", "F", "L"), "B": ("B", "F", "L")},
               "D": {"0": ("X", "E", "L"), "1": None, "X": ("X", "Z", "R"), "B": None},
               "E": {"0": ("0", "E", "L"), "1": ("1", "E", "L"), "X": ("X", "A", "R"), "B": None},
               "F": {"0": None, "1": ("X", "E", "L"), "X": ("X", "Z", "R"), "B": None}}

    # machine = TuringMachine("A", "Z", actions, list(sys.argv[1]))
    # machine.compute()
    # machine = TuringMachine("A", "Z", actions, ["1", "0", "0", "1", "B", "B", "B"])
    # machine.compute()
    # Printing table
    # print("      =========== Printing table =========")
    # print("           0           1           X           B")
    # for state in actions:
    #     print(state, "-> ", actions[state][0], "||", actions[state][1], "||", actions[state]["X"],"||", actions[state]["B"])
