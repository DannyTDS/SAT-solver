#! /usr/bin/env python3

# Libraries
import sys
import time

class CNF:
    def __init__(self, problemID, maxNLiterals, nVars, nClauses, stdAnswer, wff):
        self.problemID = problemID
        self.maxNLiterals = maxNLiterals
        self.nVars = nVars
        self.nClauses = nClauses
        self.stdAnswer = stdAnswer
        self.wff = wff


def CNFObjectGenerator(filepath):
    try:
        with open(filepath) as f:
            wff = []
            for line in f:
                line = line.strip()
                if line.startswith('c'):
                    if wff:
                        yield CNF(int(problemID), int(maxNLiterals), int(nVars), int(nClauses), stdAnswer, wff)
                        wff = []
                    _, problemID, maxNLiterals, stdAnswer = line.split(" ")
                elif line.startswith('p'):
                    _, _, nVars, nClauses = line.split(" ")
                else:
                    literals = [int(x) for x in line.split(',')]
                    wff.append(literals[:-1])
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        exit()


def InputGenerator(cnf):
    for i in range(2 ** cnf.nVars):
        bin_str = bin(i)[2:].zfill(cnf.nVars)
        comb = []
        for n in bin_str:
            comb.append(1) if int(n)==1 else comb.append(-1)
        yield comb


def verify(wff, assignment):
    for clause in wff:
        clauseSatisfied = False
        for literal in clause:
            varIndex = abs(literal) - 1
            if assignment[varIndex] * literal > 0:       # ie, signs in literal and assignment makes positive result
                clauseSatisfied = True
                break
        if not clauseSatisfied:
            return False
    return True


def main():
    if len(sys.argv) <= 1:
        print("Too few arguments.")
        exit()
    filepath = sys.argv[1]
    cnfGen = CNFObjectGenerator(filepath)

    for cnf in cnfGen:
        inputGen = InputGenerator(cnf)
        print(f"\nVerifying {cnf.problemID}, with {cnf.nVars} vars...")
        startTime = time.time()
        for assignment in inputGen:
            if verify(cnf.wff, assignment):
                break
        endTime = time.time()
        timeElapsed = f"{(endTime - startTime)*1000000:.2f}"
        cnfStats = [cnf.problemID, cnf.nVars, cnf.nClauses, cnf.maxNLiterals, sum([len(wff) for wff in cnf.wff]), ]

if __name__ == "__main__":
    main()
