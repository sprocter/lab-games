import time 

def time_remaining():
    for i in range (1, num_players+1):
        print('Player ' + str(i) + ' has ' + str(bank[i]) + 's remaining')

num_players = int(input('Number of players? '))
delay = int(input('Delay? (in seconds) '))
bankSize = int(input('Reserve time? (in minutes) '))
cur_player_num = 1
turn = 1
bank = [bankSize * 60 for i in range(num_players+1)]

command = input('Commands: [s]tart, [e]nd, [j#]ump to player ')

while(True):
    if command == 's' or command == 'start':
        pass # Default action, do nothing
    elif command == 'e' or command == 'end':
        exit()
    elif command[0:1] == 'j':
        if command[1:2] == 'u': # someone really typed this all out smh
            new_player_num = int(command[14:])
        else: 
            new_player_num = int(command[1:])
        cur_player_num = new_player_num
    elif command == 'p' or command == 'pause':
        print('Play paused')
        command = input('Commands: [e]nd, [j#]ump to player ')
        continue
    elif command == 'n' or command == 'next':
        pass # Default action, do nothing
    else:
        print('Syntax error, please try again')
        command = input('Commands: [p]ause, [e]nd, [n]ext, [j#]ump to player ')
        continue

    start_time = time.time()
    print('It\'s Player ' + str(cur_player_num) + '\'s turn, after ' + str(delay) + 's they will start using their reserve, which has ' + str(bank[cur_player_num]) + 's left.')

    command = input('Commands: [p]ause, [e]nd, [n]ext, [j#]ump to player ')
    end_time = time.time()
    turn_time = int(end_time - start_time)
    bank[cur_player_num] -= turn_time - delay if turn_time > delay else 0
    print('Player ' + str(cur_player_num) + '\'s turn is over after ' + str(turn_time) + 's. Their reserve has ' + str(bank[cur_player_num]) + 's left.')
    cur_player_num = cur_player_num + 1 if cur_player_num < num_players else 1