#! /usr/bin/env python3
# Valid Lines Puzzle Solver: Brute Force Edition
# Author: Zachary Braun <pypuzzles@enekk.xyz>
# Date: 2022-02-01
#
# Description:
#   If you have a 20*20 finite, discrete, square grid, and you randomly light up three squares anywhere on the grid (uniform distribution), what is the probability that all three squares are collinear?
# Collinear meaning if you connect the center of the three squares, they fall on the same straight line.
#
# Solution:
#  Calculate all possible sets of points and see if they are in a line

from itertools import chain, combinations
import os
from math import comb, factorial, floor, isclose

# Find the Slope (m) and Y-Intercept (b) of two points to
# use in slope-intercept form `y = mx + b`, returns (None, None)
# if the points are in a vertical line, otherwise (m, b)
def calc_line(point1, point2):
    if point1[0] == point2[0]: # Vertical Line
        return (None, None)

    slope = (point1[1] - point2[1])/(point1[0] - point2[0])
    y_intercept = point1[1] - slope*point1[0]
    return (slope, y_intercept)

# Check to see if a potential solution set is in a line
# using various methods.
def line_check(points):

    # Create a dictionary that stores the judgement of each method
    method_keys = ["Floor of SI", "Same SIs", "Solution of SI"]
    methods = dict.fromkeys(method_keys, True)

    # Find the slope-intercept form of the first two points
    slope, y_intercept = calc_line(points[0], points[1])
    if slope == None or y_intercept == None:
        if all([points[0][0] == x[0] for x in points[2:]]):
            return(methods)

    # Lambda function to find y given an x and a slope-intercept
    slope_intercept = lambda x: slope*x + y_intercept
    for point in points[2:]:
        # Bail if all methods are False
        if not any(methods.values()):
            return(methods)

        # Find the slope-intercept of the first point and the current point
        our_slope, our_y_intercept = calc_line(points[0], point)

        if slope == None or y_intercept == None: # Our line fails vertical line test
            methods = dict.fromkeys(method_keys, False)
        if methods["Floor of SI"] and not point[1] == floor(slope_intercept(point[0])): # Line touches a box at all
            methods["Floor of SI"] = False
        if methods["Solution of SI"] and not isclose(point[1], slope_intercept(point[0])): # Solve slope-intercept
            methods["Solution of SI"] = False
        if methods["Same SIs"] and not (isclose(our_slope, slope) and isclose(our_y_intercept, y_intercept)): # Are slope-intercepts always equal
            methods["Same SIs"] = False

    return(methods)


def main():
    # Size of board (M x N) and desired number of points in a line
    M = 20
    N = 20
    C = 3
    log_points = False # Log all valid points from each method?

    if C < 2:
        print(f'C value must be >= 2')
        return()

    # Initialize various methods of recording results
    method_keys = ["Floor of SI", "Same SIs", "Solution of SI"]
    valid_points = dict.fromkeys(method_keys, set())
    valid_choices = dict.fromkeys(method_keys, 0)
    fhs = {"Floor of SI": [None, './brute_solutions/solutions_floor.txt'],
           "Same SIs": [None, './brute_solutions/solutions_same_sis.txt'],
           "Solution of SI": [None, './brute_solutions/solutions_sis.txt']}

    # Open files to log solutions to
    if log_points:
        for method in method_keys:
            os.makedirs(os.path.dirname(fhs[method][1]), exist_ok=True)
            fhs[method][0] = open(fhs[method][1], 'w')

    # Generate a list of points
    all_points = [(x,y) for x in range(0, M) for y in range(0,N)]

    # Size of valid point space
    total_choices = comb(M*N,C) 

    # A progress counter
    p_percent = .05 * total_choices
    progress = 0
    for possible_soln in combinations(all_points, C):
        # Update and possibly print progress
        progress += 1
        if not progress % p_percent:
            print(f'Progress: {progress} of {total_choices} or {100*progress/total_choices}%', end='\r')

        # Check possible solution
        line_results = line_check(possible_soln)
        for k,v in line_results.items():
            if v:
                valid_choices[k] += 1
                valid_points[k].add(frozenset(possible_soln))
                if log_points:
                    print(*possible_soln, sep=", ", file=fhs[k][0])

    # Be a good kid and close open files
    if log_points:
        for method in method_keys:
            fhs[method][0].close()

    # Print results
    for method in method_keys:
        print(f'{method}: {valid_choices[method]} vs Total Choices: {total_choices} or {100*(valid_choices[method]/total_choices)}%')

if __name__ == '__main__':
    main()
