import re
import sys
from collections import defaultdict, Counter
from typing import Set, List, Dict

import dataclasses
from dataclasses import dataclass

headers = None
headers_map = None

def field(parts, field_name):
    index = headers_map[field_name]
    return parts[index]

def pct(map, graduation_date, value):
    this_value = map[graduation_date][value]
    total = sum(map[graduation_date].values())
    return this_value / total

nonletters = re.compile('[^a-zA-Z]')


@dataclass
class Application:
    date: str = ""
    schools: List = dataclasses.field(default_factory=list)

# candidate_id -> app_id -> Application
candidates = defaultdict(lambda: defaultdict(Application))

count = 0
with open("/Users/alex.rosen/Downloads/edu.csv", encoding="latin-1") as file:
    for line in file.readlines():
        parts = line.rstrip().split("\t")
        count += 1
        if not headers:
            headers = parts
            headers_map = {header: i for i, header in enumerate(parts)}
        else:
            app = candidates[field(parts, "candidate_id")][field(parts, "candidate_card_id")]
            app.date = field(parts, "occurred_on")
            app.schools.append(parts)

headers.extend(["changed_school"])
sys.stdout.buffer.write("\t".join(headers).encode('iso8859-1'))
sys.stdout.write("\n")

count = 0
for candidate in candidates.values():
    applications = list(candidate.values())
    applications.sort(key = lambda app: app.date)
    prev_schools = None
    prev_app_date = None
    for application in applications:
        schools = set()
        schools_all = set()
        for line in application.schools:
            if not field(line, "graduation_date"):
                continue
            school_name = nonletters.sub('', field(line, "school_name")).lower()
            schools_all.add(school_name)
            if prev_app_date and field(line, "graduation_date") > prev_app_date:
                continue
            schools.add(school_name)
        # changed_school = prev_schools and prev_schools != schools and prev_schools != schools_all
        for line in application.schools:
            school_name = nonletters.sub('', field(line, "school_name")).lower()
            changed_school = prev_app_date and field(line, "graduation_date") and field(line, "graduation_date") <= prev_app_date and school_name not in prev_schools
            line.append("yes" if changed_school else "no")
            sys.stdout.buffer.write("\t".join(line).encode('iso8859-1'))
            sys.stdout.write("\n")
            sys.stdout.flush()
            count += 1
        prev_schools = schools_all
        prev_app_date = application.date

