# Simple brute force sudoku solver
#
# author: huqa (pikkuhukka@gmail.com)

S_NUMBERS = [1,2,3,4,5,6,7,8,9]


def change_zeroes_to_nones(grid):
    '''Changes zeroes to None in grid'''
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            if grid[i][j] == 0:
                grid[i][j] = None
    return grid

def bf_solution(grid_to_solve):
    '''A brute force solution for solving sudokus'''
    # spot is tuple with (y,x,number)
    spots = []
    grid = list(grid_to_solve)
    last_spot = ()
    nx = 0
    ny = 0
    while not is_solved(grid):
        if grid[ny][nx] == None or last_spot:
            is_good = False
            i = 1
            if last_spot:
                i = last_spot[2]
                ny = last_spot[0]
                nx = last_spot[1]
                i += 1
            while not is_good_candidate(nx, ny, i, grid):
                i += 1
                if i > 9:
                    grid[ny][nx] = None
                    last_spot = spots.pop()
                    break
            else:
                spots.append((ny,nx,i))
                last_spot = ()
                grid[ny][nx] = i
                is_good = True
                nx += 1
                if nx >= 9:
                    ny += 1
                    nx = 0
        else:
            nx += 1
            if nx >= 9:
                ny += 1
                nx = 0

    return grid


def is_legal_for_row(num, y, grid):
    '''Checks if num is legal for the row'''
    for rx in range(0,9):
        if grid[y][rx] == num:
            return False
    return True

def is_legal_for_column(num, x, grid):
    '''Checks if num is legal for the column'''
    for ry in range(0,9):
        if grid[ry][x] == num:
            return False
    return True

def is_good_candidate(x, y, num, grid):
    '''Checks if num is a legal candidate for spot x,y'''
    sx, sy = find_zone(x,y)
    tbt = threebythree_candidates(sy, sx, grid)
    if num in tbt:
        if is_legal_for_column(num, x, grid) and is_legal_for_row(num, y, grid):
            return True
        else:
            return False
    else:
        return False

def find_zone(x,y):
    '''Finds a zone (3x3) for a position'''
    spot_x = 0
    spot_y = 0

    if x >= 0 and x <= 2:
        spot_x = 1
    elif x >= 3 and x <= 5:
        spot_x = 2
    elif x >= 6 and x <= 8:
        spot_x = 3

    if y >= 0 and y <= 2:
        spot_y = 1
    elif y >= 3 and y <= 5:
        spot_y = 2
    elif y >= 6 and y <= 8:
        spot_y = 3

    return spot_x, spot_y

def find_start_pos(sx,sy):
    '''Finds a starting position in the grid for a zone'''
    start_x = 0
    start_y = 0
    if sy == 1:
        start_y = 0
    elif sy == 2:
        start_y = 3
    elif sy == 3:
        start_y = 6

    if sx == 1:
        start_x = 0
    elif sx == 2:
        start_x = 3
    elif sx == 3:
        start_x = 6

    return start_x, start_y

def threebythree_candidates(sy, sx, grid):
    '''Finds all legal candidates for a zone (3x3)'''
    start_x, start_y = find_start_pos(sx,sy)
    possible_numbers = []

    for y in range(start_y, start_y+3):
        for x in range(start_x, start_x+3):
            if grid[y][x] != None:
                possible_numbers.append(grid[y][x])

    return list(set(S_NUMBERS) - set(possible_numbers))

def is_solved(grid):
    '''Checks if a grid is solved completely'''
    if grid == None:
        return False
    for row in grid:
        if set(row) != set(S_NUMBERS):
            return False

    for row in range(0,9):
        column = []
        for c in range(0,9):
            column.append(grid[row][c])
        if set(column) != set(S_NUMBERS):
            return False

    for i in range(1,4):
        for j in range(1,4):
            sx, sy = find_start_pos(i,j)
            if threebythree_candidates(sy, sx, grid):
                return False
        
    return True

def print_grid(grid):
    '''Ugly print given grid'''
    k = 1
    l = 0
    print("|===|===|===|===|===|===|===|===|===|")
    for i in grid:
        for j in i:
            if j == None:
                j = 0
            if l % 3 == 0:
                print "# %d" % j,
            else:
                print "| %d" % j,
            l += 1
        if l % 3 == 0:
            print "#"
        else:
            print "|"
        if k % 3 == 0:
            print("|===|===|===|===|===|===|===|===|===|")
        else:
            if l % 3 == 0:
                print("#   |   |   #   |   |   #   |   |   #")
            else:
                print("|   |   |   |   |   |   |   |   |   |")
        k += 1
    print("")


if __name__ == '__main__':

    sudoku = [[0,0,7,4,0,0,0,0,9], 
             [3,9,0,0,8,0,0,4,1], 
             [0,0,5,2,0,0,0,3,0],
             [0,0,4,6,2,3,0,0,0], 
             [0,2,9,8,0,4,6,7,0], 
             [0,0,0,9,7,1,8,0,0],
             [0,3,0,0,0,7,1,0,0], 
             [9,7,0,0,6,0,0,5,8], 
             [5,0,0,0,0,8,3,0,0]]

    print_grid(sudoku)
    sudoku = change_zeroes_to_nones(sudoku)

    print_grid(bf_solution(sudoku))

