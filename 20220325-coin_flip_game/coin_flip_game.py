#! /usr/bin/env python3

from  math import comb, factorial as fac
from time import time

def sol1_binary_counting(flips: int, initial_bet: int, bonus: float, penalty: float, games: int, p_games: float, s_time: float) -> int:
    wins = 0
    for game_num in range(0, games):
        if not game_num % p_games:
            print(f'{format(100*game_num/games, ".4f")}% complete in {round(time()-s_time)}s', end='\r')
        my_game = sol1_helper(game_num, flips, initial_bet, bonus, penalty)
        if my_game[0] >= initial_bet:
            wins += 1

    print(f'Binary Counting: {format(100*(wins/games), ".4f")}% wins: {wins} in {round(time()-s_time)}s')
    return wins

def sol1_helper(game_num: int, flips: int, initial_bet: int, bonus: float, penalty: float) -> tuple:
    bpool = initial_bet
    stop_point = (0, initial_bet)
    for pos, flip in enumerate(list(format(game_num, '0'+str(flips)+'b'))):
        bpool += bpool*bonus if flip == '1' else -1*(bpool*penalty)
        if bpool >= stop_point[1]:
            stop_point = (pos+1, bpool)

    return (bpool, stop_point[0], stop_point[1])


def sol2_recursive(flips: int, initial_bet: int, bonus: float, penalty: float, games: int, p_games: float, s_time: float) -> int:
    #        0:     1:           2:     3:       4:     5:           6:
    setup = (flips, initial_bet, bonus, penalty, games, p_games, s_time)
    print(f'0.0000% complete in {round(time()-setup[6])}s', end='\r')
    wins, *_ = sol2_recursive_helper(setup, 1, initial_bet)

    print(f'Depth-First Recursion: {format(100*(wins/games), ".4f")}% wins: {wins} in {round(time()-s_time)}s')
    return wins

def sol2_recursive_helper(setup: tuple, cur_flip: int, bpool: int, wins: int=0, comp: int=0) -> int:
    if cur_flip > setup[0]:
         return (wins + 1, comp+1) if bpool >= setup[1] else (wins, comp+1)

    # win
    wins, comp = sol2_recursive_helper(setup, cur_flip+1, bpool + bpool*setup[2], wins=wins, comp=comp)

    if not comp % setup[5]:
        print(f'{format(100*comp/setup[4], ".4f")}% complete in {round(time()-setup[6])}s', end='\r')

    # loss
    wins, comp = sol2_recursive_helper(setup, cur_flip+1, bpool - bpool*setup[3], wins=wins, comp=comp)

    if not comp % setup[5]:
        print(f'{format(100*comp/setup[4], ".4f")}% complete in {round(time()-setup[6])}s', end='\r')

    return (wins, comp)


def sol3_commutative(flips: int, initial_bet: int, bonus: float, penalty: float, games: int, p: float, s_time: float) -> int:
    wins = 0
    m_bonus   = 1+bonus
    m_penalty = 1-penalty
    my_games = sum(range(0,flips+1))
    p_games = p*my_games

    for game in range(0, flips+1):
        if not game % p_games:
            print(f'{format(100*game/my_games, ".4f")}% complete in {round(time()-s_time)}s', end='\r')
        if initial_bet * pow(m_bonus, game) * pow(m_penalty, flips - game) >= initial_bet:
            wins += comb(flips, game)

    print(f'Commutative: {format(100*(wins/games), ".4f")}% wins: {wins} in {round(time()-s_time)}s')
    return wins


def main() -> None:
    initial_bet = 100
    flips = 100 
    win_bonus = .5
    lose_penalty = .4

    games = pow(2, flips)
    p = .0001
    p_games = round(p*games) or 1

    print(f'Total Possible Games: 2^{flips} or {pow(2,flips)}')

    # Solution 3: Commutative Solution
    sol3_commutative(flips, initial_bet, win_bonus, lose_penalty, games, p, time())

    # Solution 2: Depth-First Recursive
    sol2_recursive(flips, initial_bet, win_bonus, lose_penalty, games, p_games, time())

    # Solution 1: Binary Counting
    sol1_binary_counting(flips, initial_bet, win_bonus, lose_penalty, games, p_games, time())


if __name__ == '__main__':
    main()
