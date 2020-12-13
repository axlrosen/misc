import dataclasses
import sys
from collections import defaultdict, Counter
from typing import Optional, Set, Mapping

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

@dataclass
class Graduation:
    date: Optional[str] = None
    school: Optional[str] = None
    majors: Set[str] = dataclasses.field(default_factory=set)
    ids: Set[int] = dataclasses.field(default_factory=set)
    count: int = 0

def pct2(graduations: Mapping[str, Graduation], graduation_date: str, attr: str, value: str):
    all_graduations = [g for g in graduations if g.graduation_date == graduation_date]
    similar_graduations = [g for g in graduations if g.graduation_date == graduation_date and getattr(attr, g) == value]
    total_uses = sum(g.count for g in all_graduations)



with open("/Users/alex.rosen/Downloads/career.csv", encoding="latin-1") as file:
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
    graduations = defaultdict(Graduation)
    for line in lines:
        graduation_date = field(line, "graduation_date")
        app_id = field(line, "candidate_card_id")
        graduation = graduations[graduation_date + app_id]
        graduation.date = graduation_date
        graduation.school = field(line, "school_name")
        graduation.majors.add(field(line, "degree_major"))
        graduation.ids.add(field(line, "degree_id"))
        graduation.count += 1
    for line in lines:
        graduation_date = field(line, "graduation_date")
        app_id = field(line, "candidate_card_id")
        graduation = graduations[graduation_date + app_id]
        if not graduation_date:
            line.extend(["","",""])
        else:
            similar_graduations = [g for g in graduations if g.graduation_date == graduation_date]
            total_uses = sum(g.count for g in similar_graduations)
            line.append(str(pct(schools_map, graduation_date, field(line, "school_name"))))
            line.append(str(pct(majors_map, graduation_date, field(line, "degree_major"))))
            line.append(str(pct(degrees_map, graduation_date, field(line, "degree_id"))))
        sys.stdout.buffer.write("\t".join(line).encode('iso8859-1'))
        sys.stdout.write("\n")
        sys.stdout.flush()
