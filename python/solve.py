"""Solves an instance.

Modify this file to implement your own solvers.

For usage, run `python3 solve.py --help`.
"""

import argparse
from pathlib import Path
from typing import Callable, Dict

from instance import Instance
from solution import Solution
from point import Point 
from file_wrappers import StdinFileWrapper, StdoutFileWrapper


def solve_naive(instance: Instance) -> Solution:
    return Solution(
        instance=instance,
        towers=instance.cities,
    )

def solve_test(instance: Instance) -> Solution: 
    towers = []
    for i in range(2, instance.grid_side_length, 5):
        for j in range (2, instance.grid_side_length, 5):
            towers.append(Point(i, j))
    return Solution(
        instance=instance,
        towers=towers,
    )

def city_cover(instance: Instance, cities):
    tower_cover = [] #list of tuples of the form (POINT, ARRAY OF POINTS)
    for i in range(0, instance.grid_side_length):
        for j in range (0, instance.grid_side_length): 
            tow = Point(i, j)
            cities_covered = []
            for city in cities:
                if (tow.distance_obj(instance.cities[city]) <= instance.coverage_radius):
                    cities_covered.append(city)
            tower_cover.append((tow, cities_covered))
    tower_cover = sorted(tower_cover, key=lambda tup: len(tup[1]), reverse=True)
    return tower_cover

def solve_greedy(instance: Instance) -> Solution: 
    cities = list(range(len(instance.cities)))
    towers = []
    while cities:
        largest_cover = city_cover(instance, cities).pop(0)
        for city in largest_cover[1]:
            cities.remove(city)
        towers.append(largest_cover[0]) 
    return Solution(
        instance=instance, 
        towers=towers
    )

SOLVERS: Dict[str, Callable[[Instance], Solution]] = {
    "naive": solve_naive,
    "test": solve_test, 
    "greedy": solve_greedy
}

# You shouldn't need to modify anything below this line.
def infile(args):
    if args.input == "-":
        return StdinFileWrapper()

    return Path(args.input).open("r")


def outfile(args):
    if args.output == "-":
        return StdoutFileWrapper()

    return Path(args.output).open("w")


def main(args):
    with infile(args) as f:
        instance = Instance.parse(f.readlines())
        solver = SOLVERS[args.solver]
        solution = solver(instance)
        assert solution.valid()
        with outfile(args) as g:
            print("# Penalty: ", solution.penalty(), file=g)
            solution.serialize(g)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a problem instance.")
    parser.add_argument("input", type=str, help="The input instance file to "
                        "read an instance from. Use - for stdin.")
    parser.add_argument("--solver", required=True, type=str,
                        help="The solver type.", choices=SOLVERS.keys())
    parser.add_argument("output", type=str,
                        help="The output file. Use - for stdout.",
                        default="-")
    main(parser.parse_args())
