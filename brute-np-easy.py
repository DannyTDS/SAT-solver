#! /usr/bin/env python3

# Libraries
import os
import sys
import csv
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
        # "0" maps to -1, "1" maps to 1
        yield [int(n) * 2 - 1 for n in bin_str]


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
    outputFilepath = filepath[:filepath.find(".")] + "-opt.csv"
    cnfGen = CNFObjectGenerator(filepath)

    if os.path.exists(outputFilepath):
        choice = input(f"Are you sure you want to overwrite results for {outputFilepath} (Y/N)? ")
        if choice not in ("Y", "y"):
            print("Program terminated.")
            exit()

    opt = open(outputFilepath, "w")
    optWriter = csv.writer(opt, delimiter=",")

    for cnf in cnfGen:
        # fetch assignments
        inputGen = InputGenerator(cnf)
        os.system('clear')
        print(f"Verifying problem #{cnf.problemID}, with {cnf.nVars} vars...")

        # start verifying
        startTime = time.time()
        prediction = "U"
        for assignment in inputGen:
            if verify(cnf.wff, assignment):
                prediction = "S"
                satisfiedAssignment = assignment
                break
        endTime = time.time()

        # construct the output stats
        timeElapsed = f"{(endTime - startTime)*1000000:.2f}"
        totalNLiterals = sum([len(w) for w in cnf.wff])
        if cnf.stdAnswer in ("S", "U"):
            agreed = 1 if cnf.stdAnswer == prediction else -1
        else:
            agreed = 0
        
        cnfStats = [cnf.problemID, cnf.nVars, cnf.nClauses, cnf.maxNLiterals, totalNLiterals, prediction, agreed, timeElapsed]
        
        if prediction == "S":
            # -1 maps to 0, 1 maps to 1, then turn whole thing into a string
            satisfiedAssignment = ",".join([str((v + 1) // 2) for v in satisfiedAssignment])
            cnfStats.append(satisfiedAssignment)
        
        # write stats to csv file
        optWriter.writerow(cnfStats)
    
    opt.close()
    print("Output completed.")

if __name__ == "__main__":
    main()
