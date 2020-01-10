from pfm import settings, Space, PotentialFieldMethod


def main() -> None:
    input_path = settings.DATA_DIR / "normally.json"
    space = Space.form_file(input_path)
    algorithm = PotentialFieldMethod()
    plan = algorithm.solve(space)
    output_path = settings.ROOT_DIR / "solution.json"
    plan.dump(output_path)


if __name__ == "__main__":
    main()
