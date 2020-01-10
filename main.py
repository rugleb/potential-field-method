from argparse import ArgumentParser
from pathlib import Path

from pfm import PotentialFieldMethod, Space

DIR = Path(__file__).parent


def main() -> None:
    parser = ArgumentParser(
        prog="python main.py",
        description="Potential field method runner"
    )
    parser.add_argument(
        "--space",
        dest="space",
        help=(
            "Path to the JSON file describing the configuration space, "
            "default: %(default)r"
        ),
        default=DIR / "data" / "normally.json",
    )
    parser.add_argument(
        "--solution",
        dest="solution",
        help=(
            "The path to the file where the solution will be written, "
            "default: %(default)r"
        ),
        default=DIR / "solution.json",
    )
    args = parser.parse_args()

    input_path = Path(args.space).resolve()
    output_path = Path(args.solution).resolve()

    space = Space.form_file(input_path)
    algorithm = PotentialFieldMethod()

    plan = algorithm.solve(space)
    plan.dump(output_path)

    parser.exit()


if __name__ == "__main__":
    main()
