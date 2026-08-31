import random
import time

prize_index = random.randrange(0,3)
doors = [0, 0, 0]
doors[prize_index] = 1 

print("Welcome to the Monty Hall Game!")
time.sleep(1)

print("Before you are three doors. Behind one of them lies a brilliant prize for you!")
time.sleep(1.5)

print("Guess correctly, and you'll be rewarded greatly!")
time.sleep(1)

print("Will it be Door Number 1, Door Number 2, or Door Number 3?")

print(r"""
     _______       _______       _______
    |       |     |       |     |       |
    |   1   |     |   2   |     |   3   |
    |       |     |       |     |       |
    |     o |     |     o |     |     o |
    |       |     |       |     |       |
    |_______|     |_______|     |_______|
""")

print()

choice_index = int(input("Pick a door: ")) - 1

reveal_index = random.choice([i for i in range(0,3) if i not in [prize_index, choice_index]])

print()
time.sleep(1)

print("Before we let you know if you've won, we will reveal what is behind one of the doors...")
time.sleep(2)

print(f"Let's take a look behind Door Number {reveal_index + 1}...")
time.sleep(1.5)

print(f"It looks like Door {reveal_index + 1} is empty. Lucky you!")
time.sleep(1.5)

print()

swap_index = [idx for idx, _ in enumerate(doors) if idx not in [choice_index, reveal_index]][0]

print(f"Now you have a choice. Would you like to change your answer to Door Number {swap_index + 1}, or stay where you are?")
time.sleep(3)

swap_choice = input("Would you like to swap doors? (y/n): ")

while swap_choice.lower() != "y" and swap_choice.lower() != "n":
    swap_choice = input("Would you like to swap doors? (y/n): ")

print()
time.sleep(1)

if swap_choice.lower() == "y":
    choice_index = swap_index

    print(f"Alright, it looks like you want to swap to Door {swap_index + 1}.")
    time.sleep(1.5)

    print("Let's see if that's the correct choice...")
else:
    print("You trust your first instinct. I like it! Let's see if you're right...")

time.sleep(1.5)

print(f"Behind Door {choice_index + 1} is...")
time.sleep(5)

if int(choice_index) == (prize_index):
    print("THE GLORIOUS PRIZE! CONGRATULATIONS!")
    print(r"""
     .-.-.
    (  |  )
     \ | /
   .--\|/--.
  /____+____\
  |    |    |
  |----+----|
  |    |    |
  |____|____|
""")
else:
    print("NOTHING! Better luck next time! :(")

