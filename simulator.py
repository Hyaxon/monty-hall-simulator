import random
import csv

f = open('results.csv','w')
f.write("Iteration, Swapped?, Win\n")
for iteration in range(1, 1001):
    prize_index = random.randrange(0,3)

    doors = [0, 0, 0]
    doors[prize_index] = 1 

    choice_index = random.randrange(0,3)

    reveal_index = random.choice([i for i in range(0,3) if i not in [prize_index, choice_index]])

    swap_index = [idx for idx, _ in enumerate(doors) if idx not in [choice_index, reveal_index]][0]

    swap_choice = iteration >= 500

    if swap_choice: choice_index = swap_index

    win = choice_index == prize_index
    f.write(f"{iteration}, {swap_choice}, {win}\n") 


