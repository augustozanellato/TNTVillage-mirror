from commons import *
from sqlalchemy import or_


engine, session = get_database()

def search(what):
    return session.query(Record).filter(or_(Record.title.ilike(f"%{'%'.join(what.split())}%"), Record.description.ilike(f"%{what}%"))).order_by(Record.seeds.desc())

if __name__ == "__main__":
    import sys
    for result in search(sys.argv[1]):
        print(result)