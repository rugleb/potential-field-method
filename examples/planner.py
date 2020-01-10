from pathlib import Path

from pfm import PotentialFieldMethod, Space

DIR = Path(__file__).parent


def main() -> None:
    input_path = DIR.joinpath("space.json")
    space = Space.form_file(input_path)
    algorithm = PotentialFieldMethod()
    plan = algorithm.solve(space)
    output_path = DIR.joinpath("solution.json")
    plan.dump(output_path)


if __name__ == "__main__":
    main()
