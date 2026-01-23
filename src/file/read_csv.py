import csv

def get_data_from_csv(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file, delimiter=",", quotechar='"')

        # TODO: Remove the limiting of 10 rows
        return [row for row in reader][:10]


