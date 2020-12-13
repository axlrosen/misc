import re
import sys
from collections import defaultdict, Counter

from dataclasses import dataclass

headers = None
headers_map = None
people = defaultdict(list)

STOPWORDS = set(["&", "/", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"])

def field(parts, field_name):
    index = headers_map[field_name]
    return parts[index].lower()

def pct(map, positions_dates, value):
    this_value = map[positions_dates][value]
    total = sum(map[positions_dates].values())
    return this_value / total

def sp(words):
    return set(re.split("\W+", words)).difference(STOPWORDS)

def similarity(line):
    job_title = sp(field(line, "job_title"))
    title_short = sp(field(line, "title_short"))
    if not job_title or not title_short:
        return 0
    return len(job_title.intersection(title_short)) / len(job_title.union(title_short))

def is_founder(line):
    return "founder" in sp(field(line, "title_short"))

with open("/Users/alex.rosen/Downloads/emp.csv", encoding="latin-1") as file:
    for line in file.readlines():
        parts = line.rstrip().split("\t")
        if not headers:
            headers = parts
            headers_map = {header: i for i, header in enumerate(parts)}
        else:
            people[field(parts, "candidate_id")].append(parts)

headers.extend(["employer_freq", "title_freq", "is_founder_freq", "title_similarity"])
print("\t".join(headers))

for lines in people.values():
    employer_map = defaultdict(Counter)
    title_map = defaultdict(Counter)
    founder_map = defaultdict(Counter)
    for line in lines:
        positions_dates = field(line, "position_start_date") + field(line, "position_end_date")
        employer_map[positions_dates][field(line, "employer_short")] += 1
        title_map[positions_dates][field(line, "title_short")] += 1
        founder_map[positions_dates][is_founder(line)] += 1
    for line in lines:
        positions_dates = field(line, "position_start_date") + field(line, "position_end_date")
        if not positions_dates:
            line.extend(["","","",""])
        else:
            line.append(str(pct(employer_map, positions_dates, field(line, "employer_short"))))
            line.append(str(pct(title_map, positions_dates, field(line, "title_short"))))
            line.append(str(pct(founder_map, positions_dates, is_founder(line))))
            line.append(str(similarity(line)))
        sys.stdout.buffer.write("\t".join(line).encode('iso8859-1'))
        sys.stdout.write("\n")
        sys.stdout.flush()
