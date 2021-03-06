import json
import arrow
from dateutil import tz

with open("data/dataset.json") as fp:
    dataset = json.load(fp)

for item in dataset:
    if item["raw_version"] != "4.0": continue

    date = arrow.get(item["raw_data"]["date_string"], "[Last updated:] MMMM D, YYYY | h:mma", tzinfo=tz.gettz('US/Eastern'))

    item["timestr"] = str(date)
    item["timestamp"] = date.timestamp

    print(item)

with open("data/dataset.json", "w") as fp:
    json.dump(dataset, fp, indent=2)