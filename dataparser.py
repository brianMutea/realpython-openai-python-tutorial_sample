# data_parser.py

import csv
import json
import os


def read_csv(filepath):
    """Read a CSV file and return a list of rows as dictionaries."""
    rows = []
    f = open(filepath, "r")
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)
    f.close()
    return rows


def parse_json(data):
    """Parse a JSON string and return a Python dictionary."""
    result = json.loads(data)
    return result


def normalize_age(records):
    """Convert age field from string to integer in a list of records."""
    for record in records:
        record["age"] = int(record["age"])
    return records


def filter_by_country(records, country):
    """Return records where country field matches the given value."""
    filtered = []
    for record in records:
        if record["country"] == country:
            filtered.append(record)
    return filtered


def save_to_json(records, output_path):
    """Save a list of records to a JSON file."""
    f = open(output_path, "w")
    json.dump(records, f)
    f.close()


def get_average_age(records):
    """Calculate the average age from a list of records."""
    total = 0
    for record in records:
        total += record["age"]
    average = total / len(records)
    return average


def load_and_process(filepath, country):
    """
    Full pipeline: load CSV, normalize ages,
    filter by country, and return results.
    """
    records = read_csv(filepath)
    records = normalize_age(records)
    filtered = filter_by_country(records, country)
    return filtered


if __name__ == "__main__":
    data = load_and_process("users.csv", "Kenya")
    print(f"Matched records: {len(data)}")
    print(f"Average age: {get_average_age(data)}")