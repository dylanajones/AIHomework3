# AI Homework 3 - Sudoku Solver
# Dylan Jones

# TODO:

#   - Implement naked triple rule
#   - Comment code!

import re
import copy

# Function to read in sudoku puzzles from file
def file_read(flag):

    puzzles = []

    # The read in puzzle consists of a difficulty and a puzzle
    sudoku_puzzle = [[],[]]

    # Open test file with only two puzzles vs full puzzle list
    if flag == 0:
        f = open('test.txt')
    else:
        f = open('puzzles.txt')

    num_lines = 0

    # Loop through the file and extract the information
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

# Function to print a pattern in a visually pleasing way
def print_pattern(pattern):

    col_count = 0
    print pattern[0]
    print '    0 1 2   3 4 5   6 7 8'
    print '   ----------------------'
    for item in pattern[1]:
        row_count = 0
        print col_count, '|',
        for char in item:
            if char == 0:
                print '*',
            else:
                print char,
            row_count += 1
            if row_count % 3 == 0:
                print '|',
        print
        col_count += 1
        if col_count % 3 == 0:
            print "   ----------------------"

# Function to print out a puzzle in a visually pleasing way
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

def naked_double(puzzle):
    row = 0
    for row_l in puzzle[1]:
        col = 0
        for box in row_l:
            if not(box[0]):
                if len(box[1]) == 2:
                    # Looking through the row
                    col_count = 0
                    for item in row_l:
                        #print row, col, col_count
                        if col_count != col:
                            if not(item[0]):
                                if (len(set(box[1]+item[1])) == 2) and (len(box[1]) > 1) and (len(item[1]) > 1):

                                    double = list(set(box[1]+item[1]))
                                    for thing in row_l:
                                        if not(thing[0]):
                                            for guess in set(box[1]+item[1]):
                                                if thing[1].count(guess) > 0:
                                                    thing[1].remove(guess)
                                    box[1] = copy.deepcopy(double)
                                    item[1] = copy.deepcopy(double)
                        col_count += 1

                    # Looking through the column
                    for i in range(len(puzzle[1])):
                        if i != row:
                            if not(puzzle[1][i][col][0]):
                                if (len(set(box[1]+puzzle[1][i][col][1])) == 2) and (len(box[1]) > 1) and (len(puzzle[1][i][col][1]) > 1):
                                    double = list(set(box[1]+puzzle[1][i][col][1]))
                                    for j in range(len(puzzle[1])):
                                        if not(puzzle[1][j][col][0]):
                                            for guess in set(box[1]+puzzle[1][i][col][1]):
                                                if puzzle[1][j][col][1].count(guess) > 0:
                                                    puzzle[1][j][col][1].remove(guess)
                                    box[1] = copy.deepcopy(double)
                                    puzzle[1][i][col][1] = copy.deepcopy(double)

                    # Looking through the box
                    for i in range(int(row/3)*3,int(row/3)*3+3):
                        for j in range(int(col/3)*3,int(col/3)*3+3):
                            if (i != row) and (j != col):
                                if not(puzzle[1][i][j][0]):
                                    if (len(set(box[1]+puzzle[1][i][j][1])) == 2) and (len(box[1]) > 1) and (len(puzzle[1][i][j][1]) > 1):
                                        double = list(set(box[1]+puzzle[1][i][j][1]))
                                        for u in range(int(row/3)*3,int(row/3)*3+3):
                                            for v in range(int(col/3)*3,int(col/3)*3+3):
                                                if not(puzzle[1][u][v][0]):
                                                    for guess in set(box[1]+puzzle[1][i][j][1]):
                                                        if puzzle[1][u][v][1].count(guess) > 0:
                                                            puzzle[1][u][v][1].remove(guess)
                                        box[1] = copy.deepcopy(double)
                                        puzzle[1][i][j][1] = copy.deepcopy(double)
            col += 1
        row += 1

    return puzzle

def naked_triple(puzzle):
    #loop through every square
    #loop through every box in row / col / box twice
    # if the groups mkae a naked triple then remove
    row = 0

    for row_l in puzzle[1]:
        col = 0
        for box in row_l:
            if not(box[0]) and (len(box[0]) != 1) and (len(box[0]) <= 3):
                # Looking at the row for second box
                col_2 = 0
                for second_box in row_l:
                    if not(second_box[0]) and (len(second_box[1]) != 1) and (len(second_box[1]) <= 3) and (col_2 != col) and (len(set(box[1]+second_box[1])) <= 3):
                        col_3 = 0
                        for third_box in row_l:
                            if not(third_box[0]) and (len(third_box[0]) != 1) and (len(third_box[0]) <= 3) and (col_2 != col_3) and (col != col_3) and (len(set(box[0]+second_box[0]+third_box[0])) == 3):
                                three = list(set(box[0]+second_box[0]+third_box[0]))

                                guess_col = 0
                                for guess_box in row_l:
                                    if not(guess_box[0]) and (guess_col != col) and (guess_col != col_2) and (guess_col != col_3):
                                        for guess in three:
                                            if guess_box[1].count(guess) > 0:
                                                guess_box[1].remove(guess)
                                    guess_col += 1
                            col_3 += 1
                        # Looking for 3rd box in the row

                    col_2 += 1

                # Looking at the col for second box
                row_2 = 0
                for i in range(len(puzzle[1])):
                    if not(puzzle[1][i][col][0]) and (len(puzzle[1][i][col][1]) != 1) and (len(puzzle[1][i][col][1]) <= 3) and (row_2 != row) and (len(set(box[1]+puzzle[1][i][col][1])) <= 3):
                        row_3 = 0
                        for j in range(len(puzzle[1])):
                            if not(puzzle[1][j][col][0]) and (len(puzzle[1][j][col][1]) != 1) and (len(puzzle[1][j][col][1]) <= 3) and (row_3 != row_2) and (row_3 != row) and (len(set(box[1]+puzzle[1][i][col][1]+puzzle[1][j][col][1])) == 3):

                                three = list(set(box[1]+puzzle[1][i][col][1]+puzzle[1][j][col][1]))
                                guess_row = 0

                                for k in range(len(puzzle[1])):
                                    if not(puzzle[1][k][col][0]) and (guess_row != row) and (guess_row != row_2) and (guess_row != row_3):
                                        for guess in three:
                                            if puzzle[1][k][col][1].count(guess) > 0:
                                                puzzle[1][k][col][1].remove(guess)
                                    guess_row += 1

                        row_3 += 1
                    row_2 += 1

                # Looking at the box for second box
                for i in range(int(row/3)*3,int(row/3)*3+3):
                    for j in range(int(col/3)*3,int(col/3)*3+3):
                        if (i != row) and (j != col):
                            if not(puzzle[1][i][j][0]) and (len(puzzle[1][i][j][1]) != 1) and (len(puzzle[1][i][j][1]) <= 3) and (len(set(box[1]+puzzle[1][i][j][1])) <= 3):
                                for m in range(int(row/3)*3,int(row/3)*3+3):
                                    for n in range(int(col/3)*3,int(col/3)*3+3):
                                        if (m != row) and (n != col) and (m != i) and (n != j):
                                            if not(puzzle[1][m][n][0]) and (len(puzzle[1][m][n][1]) != 1) and (len(puzzle[1][m][n][1]) <= 3) and (len(set(box[1]+puzzle[1][i][j][1]+puzzle[1][m][n][1])) <= 3):

                                                three = list(set(box[1]+puzzle[1][i][j][1]+puzzle[1][m][n][1]))

                                                for x in range(int(row/3)*3,int(row/3)*3+3):
                                                    for y in range(int(col/3)*3,int(col/3)*3+3):
                                                        if (x != row) and (y != col) and (x != i) and (y != j) and (x != m) and (y != n):
                                                            if not(puzzle[1][x][y][0]):
                                                                for guess in three:
                                                                    if puzzle[1][x][y][1].count(guess) > 0:
                                                                        puzzle[1][x][y][1].remove(guess)

        col += 1
    row += 1

    return puzzle

def solve_puzzle(puzzle, depth):

    # if depth > 0:
    #     print "MADE A GUESS"

    global num_backtracks

    # Doing the simple inference until no new information is gained
    puzzle = inference_rule_1(copy.deepcopy(puzzle))
    puzzle = inference_rule_2(copy.deepcopy(puzzle))
    puzzle = naked_double(copy.deepcopy(puzzle))
    puzzle = naked_triple(copy.deepcopy(puzzle))
    while (simple_add(puzzle) > 0):
        puzzle = inference_rule_1(copy.deepcopy(puzzle))
        puzzle = inference_rule_2(copy.deepcopy(puzzle))
        puzzle = naked_double(copy.deepcopy(puzzle))
        puzzle = naked_triple(copy.deepcopy(puzzle))

    # recurse here on all possible values of some square
    if check_puzzle_done(puzzle):
        return puzzle
    else:

        # square = get_next_square(puzzle, 1)
        #
        # for guess in puzzle[1][square[0]][square[1]][1]:
        #     rec_puzzle = copy.deepcopy(puzzle)
        #     rec_puzzle[1][square[0]][square[1]][0] = guess
        #     rec_puzzle[1][square[0]][square[1]][1] = []
        #
        #     rec_puzzle = solve_puzzle(rec_puzzle,depth+1)
        #
        #     if check_puzzle_done(rec_puzzle):
        #         return rec_puzzle
        #     else:
        #         num_backtracks += 1

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
                col_c += 1
            row_c += 1


def simple_add(puzzle):
    num_change = 0
    #print puzzle
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



        p = solve_puzzle(build_puzzle(puzzle),0)



        for item in result_tracker:
            if item[0] == puzzle[0]:
                item[1] += 1

                if check_puzzle_done(p):
                    item[2] += 1
                else:
                    print_pattern(puzzle)
                    print "====================================="
                    print_puzzle(p)
                    print "====================================="
                    print "====================================="

                item[3] += num_backtracks

    print result_tracker

num_backtracks = 0
print "Starting"
main()
