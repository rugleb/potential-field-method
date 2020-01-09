from pfm import settings, Space, PotentialFieldMethod


def main() -> None:
    input_path = settings.DATA_DIR / "normally.json"
    space = Space.form_file(input_path)
    algorithm = PotentialFieldMethod()
    plain = algorithm.solve(space)
    output_path = settings.ROOT_DIR / "solution.json"
    plain.dump(output_path)


if __name__ == "__main__":
    main()
