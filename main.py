import re
import sys

from datetime import datetime, timedelta
from typing import List

MATCH_TIMEDELTA = re.compile(r"^\d\d:\d\d-\d\d:\d\d")
TIME_LEN = 5

def map_to_timedelta(line):
    if len(line) < 2*TIME_LEN+1:
        return None
    delta_str = line[:2*TIME_LEN+1]
    if not re.match(MATCH_TIMEDELTA, delta_str):
        return None
    start = datetime.strptime(delta_str[:TIME_LEN], "%H:%M")
    end = datetime.strptime(delta_str[TIME_LEN+1:], "%H:%M")
    # we went through 00:00
    if end < start:
        print("WENT THROUGH THE NIGHT: ", start, end)
        end += timedelta(days=1)
    return end-start

def main(argv: List[str]):
    if len(argv) != 2:
        print("NOT ENOUGH ARGS", file=sys.stderr)
        return
    with open(argv[1], 'r') as fp:
        lines = fp.readlines()
        deltas = [map_to_timedelta(line) for line in lines]
        total_time = sum([d for d in deltas if d is not None], start=timedelta())
        print(f"Worked so far: {total_time} ({round(total_time.total_seconds()/60/60, 2)}h)")

if __name__ == "__main__":
    main(sys.argv)
