# https://www.hackerrank.com/challenges/crush/problem

import os


def arrayManipulationFirst(n, queries):
    """
    First solution, compact but not optimized,
    get correct results but some tests throw runtime error
    """
    current_list = [0] * n
    for start, end, to_add in queries:
        current_list = current_list[:start-1] + [_ + to_add for _ in current_list[start-1:end]] + current_list[end:]
    return max(current_list)


def arrayManipulation(n, queries):
    """Final solution"""
    current_list = [0 for _ in range(n+1)]

    for start, end, to_add in queries:
        current_list[start - 1] += to_add
        current_list[end] += -to_add

    current_value = max_value = current_list[0]
    for n in current_list[1:]:
        current_value = n + current_value
        max_value = current_value if current_value > max_value else max_value

    return max_value


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    m = int(first_multiple_input[1])

    queries = []

    for _ in range(m):
        queries.append(list(map(int, input().rstrip().split())))

    result = arrayManipulation(n, queries)

    fptr.write(str(result) + '\n')

    fptr.close()