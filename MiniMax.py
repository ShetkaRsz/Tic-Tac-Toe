######################################################################
#                             Libraries                              #
######################################################################


from copy import deepcopy
from numba import prange


######################################################################
#                           Game Functions                           #
######################################################################


def best_variant(input_array: list, turn: int, length: int) -> int:
    all_positions, continue_array = [], []

    for n in prange(length * length):
        i, j = divmod(n, length)

        if input_array[i][j]:
            continue

        input_array[i][j] = turn
        all_positions.append([position[:] for position in input_array])
        input_array[i][j] = 0


    for position in all_positions:
        result = move_checking(position, length)

        if result is None:
            continue_array.append(position)
        
        if result == -1:
            return -1
        if result == 0:
            return 0
        if result == 1: 
            return 1  

    if not continue_array:
        return None
    
    if turn == -1:
        return min([best_variant(deepcopy(position), {1: -1, -1: 1}[turn], length) for position in continue_array])
    return max([best_variant(deepcopy(position), {1: -1, -1: 1}[turn], length) for position in continue_array])
         

def move_checking(input_array: list[list[int, int, int]], length: int = 3) -> int or None:
    first_diagonal  = set([input_array[index][index] for index in prange(length)])
    second_diagonal = set([input_array[index][-(index + 1)] for index in prange(length)])

    if len(first_diagonal) == 1 and first_diagonal != {0}:
        return first_diagonal.pop()
    if len(second_diagonal) == 1 and second_diagonal != {0}:
        return second_diagonal.pop()

    for line in input_array:
        if len(set(line)) == 1 and set(line) != {0}:
            return line[0]
    
    for i in prange(len(input_array)):
        columns_array = []
        for j in prange(len(input_array)):
            columns_array.append(input_array[j][i])
        
        if len(set(columns_array)) == 1 and set(columns_array) != {0}:
            return columns_array[0]
        
    return None if sum(input_array, []).count(0) else 0


def minimum_maximum_algoritm(input_array: list[list[int]]) -> list:
    all_variants = []
    length = 3

    if not(move_checking(input_array, length) is None):
        return input_array

    for i in prange(length):
        for j in prange(length):
            if input_array[i][j]:
                continue

            input_array[i][j] = 1

            if move_checking(input_array) == 1:
                return input_array
            all_variants.append(deepcopy(input_array))

            input_array[i][j] = 0

    results = [(best_variant(deepcopy(position), -1, length), position) for position in all_variants]
    best_score_result = max(results, key=lambda x: x[0])[0]

    results = [answer[1] for answer in results if answer[0] == best_score_result]
    squares = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)]

    for i, j in squares:
        if input_array[i][j] == 0:
            input_array[i][j] = 1
            if input_array in results:
                answer = deepcopy(input_array)
                input_array[i][j] = 0
                return answer
            
            input_array[i][j] = 0
    
    return results[0] if results else input_array


######################################################################
#                  Made by: @Ice_Lightning_Strike                    #
######################################################################