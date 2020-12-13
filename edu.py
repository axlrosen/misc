
import sys
from collections import defaultdict, Counter

from dataclasses import dataclass

headers = None
headers_map = None
people = defaultdict(list)

def field(parts, field_name):
    index = headers_map[field_name]
    return parts[index]

def pct(map, graduation_date, value):
    this_value = map[graduation_date][value]
    total = sum(map[graduation_date].values())
    return this_value / total

with open("/Users/alex.rosen/Downloads/edu.csv", encoding="latin-1") as file:
    for line in file.readlines():
        parts = line.rstrip().split("\t")
        if not headers:
            headers = parts
            headers_map = {header: i for i, header in enumerate(parts)}
        else:
            people[field(parts, "candidate_id")].append(parts)

headers.extend(["school_freq", "major_freq", "degree_freq"])
print("\t".join(headers))

for lines in people.values():
    schools_map = defaultdict(Counter)
    majors_map = defaultdict(Counter)
    degrees_map = defaultdict(Counter)
    for line in lines:
        graduation_date = field(line, "graduation_date")
        schools_map[graduation_date][field(line, "school_name")] += 1
        majors_map[graduation_date][field(line, "degree_major")] += 1
        degrees_map[graduation_date][field(line, "degree_id")] += 1
    for line in lines:
        graduation_date = field(line, "graduation_date")
        if not graduation_date:
            line.extend(["","",""])
        else:
            line.append(str(pct(schools_map, graduation_date, field(line, "school_name"))))
            line.append(str(pct(majors_map, graduation_date, field(line, "degree_major"))))
            line.append(str(pct(degrees_map, graduation_date, field(line, "degree_id"))))
        sys.stdout.buffer.write("\t".join(line).encode('iso8859-1'))
        sys.stdout.write("\n")
        sys.stdout.flush()
