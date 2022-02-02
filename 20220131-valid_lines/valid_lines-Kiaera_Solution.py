#! /usr/bin/env python3
# Valid Lines Puzzle Solver - Kiaera's Solution
# Author: Kiaera, included with permission
# Translated from R to Python: Zachary Braun <pypuzzles@enekk.xyz>
# Date: 2022-02-01
#
# Description:
#   Attempt to find out how likely it is that C (originally 3)
# random points chosen from a MxN (originally 20x20) Matrix are all in a line
#
# Translation Note:
#   I have attempted to preserve comments and stylelistic flair where possible.
# Some style changes have been implemented to make the code slightly more
# Pythonic.

from itertools import chain, combinations
from math import comb, factorial, floor, isclose
import os
import sys

###########################################
## Why Dox, why?
############################################

#MxN grid
#C collinear centers

def WhyDox(M, N, C):
    if C == 1 or C == 2 or C > max(M,N):
        print("I hate you")
        #opt = options(show.error.messages = FALSE)
        sys.exit(1)

    #this will be easier if I know that M >= N, so let's just do that
    if N > M:
        M1 = M
        M = N
        N = M1

    ############################################
    ## Horizontal and Vertical
    ############################################

    #M lines of length N and N lines of length M

    horizontal = M*comb(N,C)
    vertical = N*comb(M,C)

    ############################################
    ## Diagonal
    ############################################

    #big diagonals
    diagonal = 2*(1+M-N)*comb(N,C)

    #4 of length (N-1), (N-2), etc out to length C if
    if min(M,N) > C:
        for i in range(N-1, C-1, -1):
            diagonal = diagonal + 4*comb(i,C)

    ############################################
    ## Bricks
    ############################################

    #initialize some empty data frames
    bricks = list()
    bricksnew = list()
    brickstotal = list()

    #looping through bricks of various ixj sizes
    for i in range(1, floor(((M-1)/(C-1))) + 1):
        for j in range(1, floor(((N-1)/(C-1))) + 1):
            #taking care of the 2-1 and 4-2 type duplicate problem
            # Translator's note, Python is zero based
            # R is 1 based
            tagsall = list()
            tag = False
            for dup in range(1, floor(((M-1)/(C-1))) + 1):
                tagsall.append( i%(dup+1) == 0 and j%(dup+1) == 0 )
                tag = any(tagsall)

            if not tag and i != j:
                #k is number of "centers" in a line
                for k in range(M, C-1, -1):
                    #don't count bricks that can't happen
                    if (M-i*(k-1)) > 0 and (N-j*(k-1)) > 0:
                        #Number of lines that fit brick with k centers
                        length = (M-i*(k-1))*(N-j*(k-1))
                        bricksnew = [i, j, k, length]
                        bricks.append(bricksnew)

                #taking care of 2-1 w/ 5 centers also being counted in 2-1 w/ 4 or 3 centers
                if len(bricks) > 1:
                    for a in range(1,len(bricks)):
                        for b in range(0,a):
                            print(f'a: {a}, b: {b}')
                            bricks[a][3] = bricks[a][3] - (bricks[b][2]-bricks[a][2] + 1)*bricks[b][3]

                brickstotal = brickstotal + bricks
                bricks = list()
            
    #added this condition because I broke everything with WhyDox(5,5,4)
    if len(brickstotal) > 0:
        #add a k choose C column for number of ways C points can be chosen in those lines
        brickstotal = [x + [comb(x[2], C)] for x in brickstotal]
        #length is number of lines for that i,j,k.  x2 to account for \ vs /
        brickstotal = [x[:3] + [2*x[3]*x[4]] + x[4:] for x in brickstotal]

        #add the thing
        bricksfinal = sum(list(zip(*brickstotal))[3])
    else:
        bricksfinal = 0

    ############################################
    ## The End
    ############################################

    #yay
    total = comb(M*N,C)
    print(bricksfinal)
    result = round(100*(horizontal + vertical + diagonal + bricksfinal)/total,2)
    return(result)

def main():
    M = 20
    N = 20
    C = 3
    print(WhyDox(M, N, C))

if __name__ == '__main__':
    main()
