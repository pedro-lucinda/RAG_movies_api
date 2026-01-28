import csv

def read_csv(file_path: str) -> list[dict]:
    """Read a CSV file and return a list of dictionaries."""
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file, delimiter=",", quotechar='"')

        return [row for row in reader]