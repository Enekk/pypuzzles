#! /usr/bin/env python3

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
    for game_num in range(0, games):
        if not game_num % one_p_games:
            print(f'{round(100*game_num/games)}% complete', end='\r')
        my_game = play_game(game_num, flips, initial_bet, win_bonus, lose_penalty)
        if my_game[0] >= initial_bet:
            wins += 1
    print(f'{format(100*(wins/games), ".2f")}% wins: {wins}') 


if __name__ == '__main__':
    main()
