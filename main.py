# AI Homework 3 - Sudoku Solver
# Dylan Jones

# TODO:
#   - Implement backtracking (ie trying a value and seeing how the puzzle goes)
#       - Implement based on which empty squre you see first
#       - Implement tracker for number of backtracks needed
#   - Implement naked triple rule
#   - Comment code!

import re
import copy

def file_read(flag):

    puzzles = []

    sudoku_puzzle = [[],[]]

    if flag == 0:
        f = open('test.txt')
    else:
        f = open('puzzles.txt')

    num_lines = 0

    for line in f:
        if re.match('\d{3}\s\d{3}\s\d{3}',line):
            line = line.replace(' ','')
            line = line.replace('\n','')
            line = line.replace('\t','')
            num_lines += 1

            row = []
            for i in range(len(line)):
                row.append(int(line[i]))

            sudoku_puzzle[1].append(row)

            if num_lines == 9:
                puzzles.append(copy.deepcopy(sudoku_puzzle))
                sudoku_puzzle = [[],[]]
                num_lines = 0
        elif re.match('\d{1,2}\s',line):
            line = re.split('\d{1,2}\s',line)[1]
            line = line.replace('\n','')
            sudoku_puzzle[0] = line


    return puzzles

def print_pattern(pattern):

    col_count = 0
    print pattern[0]
    for item in pattern[1]:
        row_count = 0
        for char in item:
            if char == 0:
                print '*',
            else:
                print char,
            row_count += 1
            if row_count % 3 == 0 and row_count != 9:
                print '|',
        print
        col_count += 1
        if col_count % 3 == 0 and col_count != 9:
            print "---------------------"

def print_puzzle(puzzle):
    col_count = 0
    print puzzle[0]
    print '    0 1 2   3 4 5   6 7 8'
    print '   ----------------------'
    for row in puzzle[1]:
        row_count = 0
        print col_count, '|',
        for box in row:
            if not(box[0]):
                print '*',
            else:
                print box[0],
            row_count += 1
            if row_count % 3 == 0:
                print '|',
        print
        col_count += 1
        if col_count % 3 == 0:
            print "   ----------------------"

def build_puzzle(pattern):
    puzzle = [[],[]]
    puzzle[0] = pattern[0]
    for item in pattern[1]:
        row = []
        for c in item:
            box = [[],[]]
            if c != 0:
                box[0] = c
            else:
                box[1] = range(1,10)
            row.append(copy.deepcopy(box))

        puzzle[1].append(row)

    return puzzle
# Function to infer about what are possible for a box
def inference_rule_1(puzzle):
    row = 0
    for row_l in puzzle[1]:
        col = 0
        for box in row_l:
            if not(box[0]):
                to_remove = []
                for boxes in row_l:
                    if boxes[0]:
                        to_remove.append(boxes[0])
                for i in range(len(puzzle[1])):
                    if puzzle[1][i][col][0]:
                        to_remove.append(puzzle[1][i][col][0])
                for i in range(int(row/3)*3,int(row/3)*3+3):
                    for j in range(int(col/3)*3,int(col/3)*3+3):
                        if puzzle[1][i][j][0]:
                            to_remove.append(puzzle[1][i][j][0])

                for item in to_remove:
                    try:
                        box[1].remove(item)
                    except ValueError:
                        pass

            col += 1
        row += 1

    return puzzle

def inference_rule_2(puzzle):
    row = 0
    for row_l in puzzle[1]:
        col = 0
        for box in row_l:
            if not(box[0]):
                # Checking for every guess if it is the only one in that r/c/b
                for guess in box[1]:
                    count_r = 0
                    count_c = 0
                    count_b = 0
                    # Checking the row
                    for item in row_l:
                        if not(item[0]):
                            if item[1].count(guess) > 0:
                                count_r += 1
                    #Checking the column
                    for i in range(len(puzzle[1])):
                        if not(puzzle[1][i][col][0]):
                            if puzzle[1][i][col][1].count(guess) > 0:
                                count_c += 1
                    #Checking the box
                    for i in range(int(row/3)*3,int(row/3)*3+3):
                        for j in range(int(col/3)*3,int(col/3)*3+3):
                            if not(puzzle[1][i][j][0]):
                                if puzzle[1][i][j][1].count(guess) > 0:
                                    count_b += 1

                    if count_r == 1 or count_c == 1 or count_b == 1:

                        # Update everyone else
                        for item in row_l:
                            if not(item[0]):
                                if item[1].count(guess) > 0:
                                    item[1].remove(guess)

                        for i in range(len(puzzle[1])):
                            if not(puzzle[1][i][col][0]):
                                if puzzle[1][i][col][1].count(guess) > 0:
                                    puzzle[1][i][col][1].remove(guess)

                        for i in range(int(row/3)*3,int(row/3)*3+3):
                            for j in range(int(col/3)*3,int(col/3)*3+3):
                                if not(puzzle[1][i][j][0]):
                                    if puzzle[1][i][j][1].count(guess) > 0:
                                        puzzle[1][i][j][1].remove(guess)

                        box[1] = [guess]
                        break
            col += 1
        row += 1
    return puzzle

def solve_puzzle(puzzle, depth):

    global num_backtracks

    puzzle = inference_rule_1(copy.deepcopy(puzzle))
    puzzle = inference_rule_2(copy.deepcopy(puzzle))
    while (simple_add(puzzle) > 0):
        puzzle = inference_rule_1(copy.deepcopy(puzzle))
        puzzle = inference_rule_2(copy.deepcopy(puzzle))
    # recurse here on all possible values of some square
    if check_puzzle_done(puzzle):
        return puzzle
    else:
        square = get_next_square(puzzle, 1)

        for guess in puzzle[1][square[0]][square[1]][1]:
            rec_puzzle = copy.deepcopy(puzzle)
            rec_puzzle[1][square[0]][square[1]][0] = guess
            rec_puzzle[1][square[0]][square[1]][1] = []

            rec_puzzle = solve_puzzle(rec_puzzle,depth+1)

            if check_puzzle_done(rec_puzzle):
                return rec_puzzle
            else:
                num_backtracks += 1

        return puzzle


def get_next_square(puzzle, flag):

    spot = [0,0]
    if flag == 0:

        min_amount = 10;
        row_c = 0
        for row in puzzle[1]:
            col_c = 0
            for box in row:
                if len(box[1]) < min_amount and not(box[0]):
                    spot[0] = row_c
                    spot[1] = col_c
                    min_amount = len(box[1])
                col_c += 1
            row_c += 1

        return spot
    else:
        row_c = 0
        for row in puzzle[1]:
            col_c = 0
            for box in row:
                if not(box[0]):
                    spot[0] = row_c
                    spot[1] = col_c
                    return spot


def simple_add(puzzle):
    num_change = 0

    for row in puzzle[1]:
        for box in row:
            if len(box[1]) == 1:
                box[0] = box[1][0]
                box[1] = []
                num_change += 1



    return num_change

def check_puzzle(puzzle):

    for row in puzzle[1]:
        for box in row:
            if not(box[0]) and len(box[1]) == 0:
                return False

    return puzzle

def check_puzzle_done(puzzle):

    for row in puzzle[1]:
        for box in row:
            if not(box[0]):
                return False

    return True

def main():
    global num_backtracks
    problems = file_read(1)
    result_tracker = [['Easy',0,0,0],['Medium',0,0,0],['Hard',0,0,0],['Evil',0,0,0]]

    for puzzle in problems:
        num_backtracks = 0
        print_pattern(puzzle)
        print "====================================="
        p = solve_puzzle(build_puzzle(puzzle),0)

        print_puzzle(p)
        print check_puzzle_done(p)

        print "====================================="
        print "====================================="

        for item in result_tracker:
            if item[0] == puzzle[0]:
                item[1] += 1

                if check_puzzle_done(p):
                    item[2] += 1

                item[3] += num_backtracks

    print result_tracker

num_backtracks = 0
print "Starting"
main()
