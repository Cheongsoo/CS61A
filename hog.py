"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    k, score = 1, 0
    boo = True
    while k <= num_rolls:
        dice_num = dice()
        if dice_num==1 and boo:
            score = 1 
            boo = False
        elif boo: 
            score += dice_num
        k += 1
    return score
    

    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2


    if opponent_score < 10:
        myScore = opponent_score + 1
    else:
        myScore = max(opponent_score//10, opponent_score%10) + 1

    if is_prime(myScore):
        return next_prime(myScore)

    return myScore
# END PROBLEM 2


# Write your prime functions here!
def is_prime(n):
    if n==1:
        return False
    k=2    
    while k<n:
        if n%k==0:
            return False
        k+=1
    return True 

def next_prime(n):
    while n < 2*n:
        n+=1
        if(is_prime(n)==True):
            return n


        

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    if num_rolls==0:
        return free_bacon(opponent_score)

    score = roll_dice(num_rolls, dice)

    if is_prime(score) :
        return next_prime(score)
    else :
        return score

        
    # END PROBLEM 2


def select_dice(dice_swapped):

    """Return a six-sided dice unless four-sided dice have been swapped in due
    to Perfect Piggy. DICE_SWAPPED is True if and only if four-sided dice are in
    play.
    """
    # BEGIN PROBLEM 3
    if dice_swapped :
        return four_sided
    return six_sided  # Replace this statement
    # END PROBLEM 3


# Write additional helper functions here!
from math import sqrt
from math import floor

def is_perfect_square(n):
    if n==1:
        return False
    if sqrt(n)==floor(sqrt(n)):
        return True
    return False



def is_perfect_cube(n):
    if n==8 or n==27 or n==64:
        return True
    return False
    

def is_perfect_piggy(turn_score):
    """Returns whether the Perfect Piggy dice-swapping rule should occur."""
    # BEGIN PROBLEM 4
    if is_perfect_square(turn_score) and turn_score != 1:
        return True 
    elif is_perfect_cube(turn_score) and turn_score != 1:
        return True
    else:
        return False
    # END PROBLEM 4


def is_swap(score0, score1):
    """Returns whether one of the scores is double the other."""
    # BEGIN PROBLEM 5
    if score0 == (score1/2) or score1 == (score0/2) :
        return True
    return False
    # END PROBLEM 5


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player
def changeScore(score0, score1): # 점수변경함수
    return score1, score0
def changeBoolean(boo): # 다이스 상태변경을 위한 함수 boo가 True면 False리턴해서 6면체 돌리는거?ㅇㅋ 
    return not boo

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0:     The starting score for Player 0
    score1:     The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    #
    dice_swapped = False # Whether 4-sided dice have been swapped for 6-sided
    
    
    thisPyScr = score0  # 턴 실행플레이어 (최초 0)
    otherPyScr = score1 # 다른 플레이어

    while True:

        """턴 시작"""

        if player==0 : # 실행플레이어가 0 일경우 
            stg = strategy0(thisPyScr, otherPyScr) # 0의 전략 실행
        else:
            stg = strategy1(thisPyScr, otherPyScr) # 아닐경우 1의 전략실

        thisScore = take_turn( stg, otherPyScr, select_dice(dice_swapped))
        # 턴을 진행하고 진행점수를 받음
        thisPyScr = thisScore + thisPyScr
        # 진행한 점수를 턴플레이어에게 

        """턴 종료"""

        if is_swap(thisPyScr, otherPyScr): #만약 스왑 조건이라면 스코어 변
            thisPyScr, otherPyScr = changeScore(thisPyScr, otherPyScr)

        # 이거는 0번이나 1번 점수가 목표한거 다을떄 나오는거제? ㅇㅋ이건스키
        if player==0 and (thisPyScr>=goal or otherPyScr>=goal):
            return thisPyScr, otherPyScr
        elif player==1 and (thisPyScr>=goal or otherPyScr>=goal):
            return otherPyScr, thisPyScr

        # 만약 두사람중 승리 조건이 만족하지 않을경우 (위 분기 실행 x) 퍼팩트피기를 검사해서 다이스스왑 
        if is_perfect_piggy(thisScore):# 여기는 턴종료후 안하고 하는거?
            dice_swapped = changeBoolean(dice_swapped)
            
        # 다음 턴을 진행하기 위해 플레이어를 바꾼다
        # 1. 점수를 바꿈
        # 2. 플레이어를 변경 (0->1 || 1->0)
        thisPyScr, otherPyScr = changeScore(thisPyScr, otherPyScr)
        player = other(player) 

    # 얘는 걍 디폴트

    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n): 
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n 
    return strategy




def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)' 



def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the strategy
    returns a valid input. Use `check_strategy_roll` to raise an error with a
    helpful message if the strategy returns an invalid output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 7
    
    
    score0, score1 = 0,0

    while score0<goal:
        score1 = 0
        while score1<goal:
            check_strategy_roll( score0,score1,strategy(score0,score1) )
            score1 += 1
        score0 += 1

    return


    # END PROBLEM 7


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8

    def print_and_return(*args):
        result, count = 0, 1
        while count<=num_samples:
            result += fn(*args)
            count += 1
        return result/num_samples

    return print_and_return
 
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    
    max_avg=0
    highest, num_rolls = 0,1

    while 1<=num_rolls<=10:
        this_avg = make_averaged( roll_dice, num_samples )( num_rolls,dice )
        if max_avg<this_avg:
            highest = num_rolls
            max_avg = this_avg
        num_rolls += 1

    return highest


    

    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"
    if True:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if free_bacon(opponent_score) < margin:
        return num_rolls
    else:
        return 0
    #return 4  # Replace this statement
    # END PROBLEM 10
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 11

    if score/2 == opponent_score:
        return num_rolls
    if opponent_score * 2 == score:
        return 0 
    if (100-score) <= opponent_score:
        return 0    
    
    if (opponent_score - score) > 33:
        return 0

    if free_bacon(opponent_score) < margin:
        return num_rolls
    else:
        return bacon_strategy(score, opponent_score)

    
    

    # END PROBLEM 11
check_strategy(swap_strategy)


def is_Myswap(score, opponent_score):
   if score==(opponent_score*2) :
      return True
   return False




def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    a strategy that returns winning rate below 73.5
    *** YOUR DESCRIPTION HERE ***
    """

    return swap_strategy(score, opponent_score)
    if (score - opponent_score) > 30:
        return 10

    if opponent_score < 10:
        opp_max = opponent_score + 1
    else:
        opp_max = max(opponent_score//10, opponent_score%10) + 1
        
    if is_Myswap(score, opponent_score):
        return 10
    elif is_prime(opp_max) and not is_Myswap( score+next_prime(opp_max), opponent_score ):
        return 0
    elif not is_Myswap(score+opp_max, opponent_score ):
        return 0

    return 6
      # Replace this statement
    # END PROBLEM 12
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

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