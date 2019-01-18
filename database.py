# import stuff
import os
import json
import datetime
import pandas as pd

# database connection
import models as mod
from models import Stats
from sqlalchemy.orm import sessionmaker


class Database(object):

    """Database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Create tables
        """

        # this is weird, sorry.
        # allows access to file from this level and notebooks level
        fname = "authentication.json"
        if os.path.isfile(fname):
            with open(fname) as f:
                auth = json.load(f)
        else:
            with open("../" + fname) as f:
                auth = json.load(f)

        self.engine = mod.db_connect(auth["database"])
        mod.create_tables(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def delete_and_recreate_all(self):
        # be careful with this one, it'll wipe out everything
        mod.recreate_all(self.engine)

    def addClones(self, records):
        for record in records:
            print(record)
            ts = record['timestamp'].split("T")[0]
            stat = self.session.query(Stats).filter_by(timestamp=ts).first()
            if stat is None:
                # insert
                stat = Stats(timestamp=record['timestamp'].split("T")[0], clones_total=record['count'], clones_uniques=record['uniques'])
            else:
                # update
                stat.clones_total = record['count']
                stat.clones_uniques = record['uniques']

            self.session.add(stat)

        self.session.commit()

    def addViews(self, records):
        for record in records:
            print(record)
            ts = record['timestamp'].split("T")[0]
            stat = self.session.query(Stats).filter_by(timestamp=ts).first()
            if stat is None:
                # insert
                stat = Stats(timestamp=record['timestamp'].split("T")[0], views_total=record['count'], views_uniques=record['uniques'])
            else:
                # update
                stat.views_total = record['count']
                stat.views_uniques = record['uniques']

            self.session.add(stat)

        self.session.commit()

    def getResults(self, from_date, to_date):
        if from_date is None:
            stat = self.session.query(Stats).order_by(Stats.timestamp).first()
            if stat is not None:
                from_date = stat.timestamp.strftime('%Y-%m-%d')
            else:
                from_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if to_date is None:
            to_date = datetime.datetime.today().strftime('%Y-%m-%d')
        # records = self.session.query(Stats).all()
        query = self.session.query(Stats).filter(Stats.timestamp <= to_date).filter(Stats.timestamp >= from_date)
        # convert to list of dicts
        results = [u.__dict__ for u in query.all()]
        # remove unnecessary "sa_instance_state" and convert timestamp
        for u in results:
            del u["_sa_instance_state"]
            u["timestamp"] = u["timestamp"].strftime('%Y-%m-%d')
        # print("RESULTS:")
        # print(results)
        return results

    def getTotals(self):
        print("GETTING TOTAL UNIQUE VIEWS AND CLONES")
        results = pd.read_sql_query("Select sum(clones_uniques) as total_unique_clones, sum(views_uniques) as total_unique_views, min(timestamp) as from_date, max(timestamp) as to_date from  stats;", self.engine)
        return results
