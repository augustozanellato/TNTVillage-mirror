import csv
import enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Enum, create_engine
from sqlalchemy.orm import sessionmaker
from humanfriendly import format_size
from urllib.parse import quote as url_quote
from urllib.parse import urlencode
from urllib.request import urlopen
from random import sample
import scraper
import socket

Base = declarative_base()
trackers = []

class RecordCategory(enum.Enum):
    FILM_TV = 1
    MUSICA = 2
    EBOOKS = 3
    FILM = 4
    LINUX = 6
    ANIME = 7
    CARTONI = 8
    MACINTOSH = 9
    WINDOWS_SOFTWARE = 10
    PC_GAME = 11
    PLAYSTATION = 12
    STUDENTS_RELEASES = 13
    DOCUMENTARI = 14
    VIDEO_MUSICALI = 21
    SPORT = 22
    TEATRO = 23
    WRESTLING = 24
    VARIE = 25
    XBOX = 26
    IMMAGINI_SFONDI = 27
    ALTRI_GIOCHI = 28
    SERIE_TV = 29
    FUMETTERIA = 30
    TRASH = 31
    NINTENDO = 32
    A_BOOK = 34
    PODCAST = 35
    EDICOLA = 36
    MOBILE = 37
    NON_CATEGORIZZATO = 38

    def pretty_name(self):
        return " ".join([x.capitalize() for x in self.name.split("_")])


def update_trackers():
    global trackers
    print("Updating trackers...")
    update_url = "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best_ip.txt"
    trackers = [x.decode("utf-8")  for x in urlopen(update_url).read().splitlines() if x]
    return trackers

class Record(Base):
    __tablename__ = "records"
    
    id = Column(Integer, Sequence('record_id_seq'), primary_key=True)
    date_time = Column(DateTime)
    hash = Column(String(40))
    title = Column(String(150))
    description = Column(String(150))
    size = Column(Integer)
    category = Column(Enum(RecordCategory))
    seeds = Column(Integer, default=-1)
    leechers = Column(Integer, default=-1)

    def __repr__(self):
        return f"<Record(id={self.id}, hash={self.hash}, title={self.title}, description={self.description}, size={self.size}, human_readable_size={self.human_readable_size}, category={self.category})>"
    
    @property
    def human_readable_size(self):
        return format_size(self.size)

    @property
    def magnet_link(self):
        if (len(trackers) == 0):
            update_trackers()
        magnet_params = urlencode({'dn': self.title,
            'tr': trackers,
            'xl': self.size}, quote_via=url_quote)
        return f'magnet:?xt=urn:btih:{self.hash}&{magnet_params}'
    
    def scrape(self, trackers_list, num_trackers=5):
        _, session = get_database()
        session.add(self)
        self.seeds = 0
        self.leechers = 0
        for tracker in sample(trackers_list, num_trackers):
            try:
                data = scraper.scrape(tracker, [self.hash])
                self.seeds += int(data[self.hash]["seeds"])
                self.leechers += int(data[self.hash]["peers"])
            except socket.timeout:
                pass
        session.commit()

engine = create_engine('sqlite:///tntvillage.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)

def get_database():
    session = sessionmaker(bind=engine)()
    return engine, session