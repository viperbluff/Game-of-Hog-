"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 

"""SIMULATOR"""

def roll_dice(num_rolls, dice=six_sided):
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    pig=0
    outcomes=0
    sum=0
    s=[]
    for i in range(0,num_rolls):
    	outcomes=dice()
    	s.append(outcomes)
    if(1 not in s):
        for i in s:
        	sum=sum+i
        return sum
    else:
        for i in s:
            if i==1:
            	pig=pig+1
        sum=sum+pig
        return sum
        
def take_turn(num_rolls,opponent_score,dice=six_sided):
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    if(num_rolls==0):

        one,last=opponent_score//10,opponent_score%10
        score=1+max(one,last)
        return score 
    else:
        score=roll_dice(num_rolls,dice)
        return score 
        
def select_dice(score, opponent_score):
    total=0
    total=score+opponent_score
    if(total%7==0):
        return four_sided
    else:
        return six_sided
def is_prime(n):
    assert type(n) == int, 'n must be an integer.'
    assert n >= 0, 'n must be non-negative.'
    k = 1
    while k < n:
        if n % k == 0:
            return False
        else:
            k=k+1
    return True


def other(who):
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    who = 0 #player 1 turn first
    tmp0=0
    tmp1=0 
    while(score0<100 and score1<100):
        if(who==0):
            if(select_dice==four_sided):
                dice=four_sided 
            else:
                dice=six_sided
            num_rolls=strategy0(score0,score1)
            if(num_rolls==0):
                score0=take_turn(num_rolls,score0,dice)
                tmp0=tmp0+score0
            else:
                score0=roll_dice(num_rolls,dice)
                tmp0=tmp0+score0
            while(is_prime(tmp0+tmp1)):
                if(tmp0<tmp1):
                    tmp1=tmp1+score0 
                else:
                    tmp0=tmp0+score0 
            who=1-who
        else:
            if(select_dice==four_sided):
                dice=four_sided 
            else:
                dice=six_sided
            num_rolls=strategy1(score1,score0)
            if(num_rolls==0):
                score1=take_turn(num_rolls,score1,dice)
                tmp1=tmp1+score1
            else:
                score1=roll_dice(num_rolls,dice)
                tmp1=tmp1+score1 
            while(is_prime(tmp0+tmp1)):
                if(tmp1<tmp0):
                    tmp0=tmp0+score1
                else:
                    tmp1=tmp1+score1          
            who=1-who
    return tmp0,tmp1  
    

#######################
# Phase 2: Strategies #
#######################
def always_roll(n):
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    def function(*args):
        i=1
        while(i<=num_samples):
            result=result+fn(*args)
            sum=sum+result
            i=i+1
        average=sum/num_samples
        return average
    return function     


def max_scoring_num_rolls(dice=six_sided):
    x=[]
    avg=[]
    same=[]
    for num_rolls in range(1,11):
            x[num_rolls]=roll_dice(num_rolls,dice)
            avg[num_rolls]=x[num_rolls]/num_rolls
            m=max(avg)
            same=[c for c in enumerate(avg) if c == m]
            while(same):
                return min(same)+1
            y=avg.index(max(avg))+1
            return y
            
def winner(strategy0, strategy1):
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test prime_strategy
        print('prime_strategy win rate:', average_win_rate(prime_strategy))

    if False: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    beacon_point=max(opponent_score//10,opponent_score%10)+1
    if(beacon_point>=margin):
        return 0
    else:
        return num_rolls    

def prime_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial boost and
    rolls NUM_ROLLS if rolling 0 dice gives the opponent a boost. It also
    rolls 0 dice if that gives at least MARGIN points and rolls NUM_ROLLS
    otherwise.
    """
    beacon_point=max(opponent_score//10,opponent_score%10)+1
    if(is_prime(score+opponent_score)):
                if(score>opponent_score):
                    return 0
                else:
                    num_rolls
    else:
        if(beacon_point>=margin):
            return 0
        else:
            return num_rolls

def final_strategy(score, opponent_score):
    rolls=5
    dice=select_dice(score, opponent_score)
    if score<40 and dice==six_sided:
        rolls=6
    if score<40 and dice==four_sided:
        rolls=3
    if score>90:
        rolls=4
    return prime_strategy(score, opponent_score, (100-score), rolls)



##########################
# Command Line Interface #
##########################


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
