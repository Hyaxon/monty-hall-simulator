#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path
import random


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("value must be at least 1")
    return number


def door_count(value):
    number = int(value)
    if number < 3:
        raise argparse.ArgumentTypeError("there must be at least 3 doors")
    return number


def simulate(n_games, n_doors, seed, output_path):
    rng = random.Random(seed)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "Iteration",
                "Doors",
                "PrizeDoor",
                "InitialChoice",
                "SwitchDoor",
                "StayWin",
                "SwapWin",
            ]
        )

        for iteration in range(1, n_games + 1):
            prize_index = rng.randrange(n_doors)
            choice_index = rng.randrange(n_doors)

            if choice_index == prize_index:
                offset = rng.randrange(n_doors - 1)
                swap_index = offset if offset < choice_index else offset + 1
            else:
                swap_index = prize_index

            stay_win = choice_index == prize_index
            swap_win = swap_index == prize_index

            writer.writerow(
                [
                    iteration,
                    n_doors,
                    prize_index + 1,
                    choice_index + 1,
                    swap_index + 1,
                    stay_win,
                    swap_win,
                ]
            )

    return output_path


def build_parser():
    parser = argparse.ArgumentParser(
        description="Simulate Monty Hall and export every trial to CSV."
    )

    parser.add_argument(
        "--games",
        type=positive_int,
        default=1000,
        help="number of simulated trials (default: 1000)",
    )

    parser.add_argument(
        "--doors",
        type=door_count,
        default=3,
        help="number of doors (default: 3)",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="optional random seed for reproducible results",
    )

    parser.add_argument(
        "--output",
        default="results.csv",
        help="CSV output path (default: results.csv)",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    output_path = simulate(
        n_games=args.games,
        n_doors=args.doors,
        seed=args.seed,
        output_path=args.output,
    )

    print(
        f"Saved {args.games:,} trials with {args.doors} doors to "
        f"{output_path.resolve()}"
    )

    if args.seed is not None:
        print(f"Random seed: {args.seed}")


if __name__ == "__main__":
    main()
