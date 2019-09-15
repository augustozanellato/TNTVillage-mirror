import csv
from commons import *
import datetime

engine, session = get_database()
session.query(Record).delete()
session.commit()
with open("dump_release_tntvillage_2019-08-30.csv", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    reader.__next__()
    for row in reader:
        try:
            session.add(Record(date_time=datetime.datetime.fromisoformat(row[0]), hash=row[1], title=row[5], description=row[6], size=row[7], category=RecordCategory(int(row[8])))) 
        except Exception:
            print(row)
            raise

session.commit()