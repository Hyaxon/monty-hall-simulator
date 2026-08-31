import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

win_rates = df.groupby("Swapped?")["Win"].mean() * 100

plt.bar(["Kept their choice", "Changed answers"], win_rates)

plt.ylabel("Win Rate (%)")
plt.title("Monty Hall Simulation Results")

plt.savefig("results.png")

plt.show()