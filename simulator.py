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


def parse_reveals(value):
    if value.lower() == "max":
        return "max"

    number = int(value)

    if number < 0:
        raise argparse.ArgumentTypeError("reveals cannot be negative")

    return number


def resolve_reveals(reveals, doors):
    if reveals == "max":
        return doors - 2

    if reveals > doors - 2:
        raise ValueError(
            f"With {doors} doors, --reveals must be between 0 and {doors - 2}, "
            "or use --reveals max."
        )

    return reveals


def simulate(
    n_games,
    n_doors,
    reveals,
    host_policy,
    seed,
    output_path,
):
    rng = random.Random(seed)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "Iteration",
                "Doors",
                "Reveals",
                "HostPolicy",
                "PrizeDoor",
                "InitialChoice",
                "RevealedDoors",
                "SwitchDoor",
                "HostRevealedPrize",
                "StayWin",
                "SwapWin",
            ]
        )

        for iteration in range(1, n_games + 1):
            prize = rng.randrange(n_doors)
            choice = rng.randrange(n_doors)

            available_to_host = [
                door
                for door in range(n_doors)
                if door != choice
            ]

            if host_policy == "informed":
                host_candidates = [
                    door
                    for door in available_to_host
                    if door != prize
                ]

                revealed = rng.sample(
                    host_candidates,
                    reveals,
                )

                host_revealed_prize = False

            else:
                revealed = rng.sample(
                    available_to_host,
                    reveals,
                )

                host_revealed_prize = prize in revealed

            switch_options = [
                door
                for door in range(n_doors)
                if door != choice and door not in revealed
            ]

            stay_win = choice == prize

            if host_revealed_prize:
                switch_door = None
                swap_win = None
            else:
                switch_door = rng.choice(switch_options)
                swap_win = switch_door == prize

            writer.writerow(
                [
                    iteration,
                    n_doors,
                    reveals,
                    host_policy,
                    prize + 1,
                    choice + 1,
                    ";".join(str(door + 1) for door in revealed),
                    "" if switch_door is None else switch_door + 1,
                    host_revealed_prize,
                    stay_win,
                    "" if swap_win is None else swap_win,
                ]
            )

    return output_path


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Simulate Monty Hall variants and export every trial to CSV."
        )
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
        "--reveals",
        type=parse_reveals,
        default=1,
        help=(
            "number of doors the host reveals, or 'max' "
            "(default: 1)"
        ),
    )

    parser.add_argument(
        "--host",
        choices=["informed", "uninformed"],
        default="informed",
        help=(
            "whether the host knows the prize location "
            "(default: informed)"
        ),
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="optional random seed for reproducibility",
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

    try:
        reveals = resolve_reveals(
            args.reveals,
            args.doors,
        )
    except ValueError as error:
        parser.error(str(error))

    output_path = simulate(
        n_games=args.games,
        n_doors=args.doors,
        reveals=reveals,
        host_policy=args.host,
        seed=args.seed,
        output_path=args.output,
    )

    print(
        f"Saved {args.games:,} trials with "
        f"{args.doors} doors and {reveals} reveals "
        f"({args.host} host) to {output_path.resolve()}"
    )

    if args.seed is not None:
        print(f"Random seed: {args.seed}")


if __name__ == "__main__":
    main()
