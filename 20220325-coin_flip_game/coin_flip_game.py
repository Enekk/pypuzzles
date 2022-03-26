#! /usr/bin/env python3

from time import time

def solve_recursive(flips: int, initial_bet: int, bonus: float, penalty: float, games: int, one_percent: float, s_time: int) -> int:
    #        0:     1:           2:     3:       4:     5:           6:
    setup = (flips, initial_bet, bonus, penalty, games, one_percent, s_time)
    print(f'0% complete in {round(time()-setup[6])}s', end='\r')
    return solve_recursive_helper(setup, 1, initial_bet)


def solve_recursive_helper(setup: tuple, cur_flip: int, bpool: int, wins: int=0, comp: int=0) -> int:
    if cur_flip > setup[0]:
         return (wins + 1, comp+1) if bpool >= setup[1] else (wins, comp+1)

    # win
    wins, comp = solve_recursive_helper(setup, cur_flip+1, bpool + bpool*setup[2], wins=wins, comp=comp)

    if not comp % setup[5]:
        print(f'{round(100*comp/setup[4])}% complete in {round(time()-setup[6])}s', end='\r')

    # loss
    wins, comp = solve_recursive_helper(setup, cur_flip+1, bpool - bpool*setup[3], wins=wins, comp=comp)

    if not comp % setup[5]:
        print(f'{round(100*comp/setup[4])}% complete in {round(time()-setup[6])}s', end='\r')

    return (wins, comp)

def play_game(game_num: int, flips: int, initial_bet: int, bonus: float, penalty: float) -> tuple:
    bpool = initial_bet
    stop_point = (0, initial_bet)
    for pos, flip in enumerate(list(format(game_num, '0'+str(flips)+'b'))):
        bpool += bpool*bonus if flip == '1' else -1*(bpool*penalty)
        if bpool >= stop_point[1]:
            stop_point = (pos+1, bpool)

    return (bpool, stop_point[0], stop_point[1])

def main() -> None:
    initial_bet = 100
    flips = 100 
    win_bonus = .5
    lose_penalty = .4

    wins = 0
    games = pow(2, flips)
    one_p_games = round(.01*games)
    s_time = time()
    recur_answer, *_ = solve_recursive(flips, initial_bet, win_bonus, lose_penalty, games, one_p_games, s_time)
    print(f'{format(100*(recur_answer/games), ".2f")}% wins: {recur_answer} in {round(time()-s_time)}s')
    s_time = time()
    for game_num in range(0, games):
        if not game_num % one_p_games:
            print(f'{round(100*game_num/games)}% complete in {round(time()-s_time)}s', end='\r')
        my_game = play_game(game_num, flips, initial_bet, win_bonus, lose_penalty)
        if my_game[0] >= initial_bet:
            wins += 1
    print(f'{format(100*(wins/games), ".2f")}% wins: {wins} in {round(time()-s_time)}s')


if __name__ == '__main__':
    main()
