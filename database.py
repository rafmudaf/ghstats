# import stuff
import os
import json
import datetime
import pandas as pd

# database connection
import models as mod
from models import Stats, StatsNRELFloris, StatswfcTools
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

    def addClones(self, records, repo_code=None):
        if (repo_code is None) or (repo_code is'wisdem_floris'):
            repo_class = Stats
        elif repo_code is 'nrel_floris':
            repo_class = StatsNRELFloris
        elif repo_code is 'wfc_tools':
            repo_class = StatswfcTools


        for record in records:
            print(record)
            ts = record['timestamp'].split("T")[0]
            stat = self.session.query(repo_class).filter_by(timestamp=ts).first()
            if stat is None:
                # insert
                stat = repo_class(timestamp=record['timestamp'].split("T")[0], clones_total=record['count'], clones_uniques=record['uniques'])
            else:
                # update
                stat.clones_total = record['count']
                stat.clones_uniques = record['uniques']

            self.session.add(stat)

        self.session.commit()

    def addViews(self, records, repo_code=None):
        if (repo_code is None) or (repo_code is'wisdem_floris'):
            repo_class = Stats
        elif repo_code is 'nrel_floris':
            repo_class = StatsNRELFloris
        elif repo_code is 'wfc_tools':
            repo_class = StatswfcTools

        for record in records:
            print(record)
            ts = record['timestamp'].split("T")[0]
            stat = self.session.query(repo_class).filter_by(timestamp=ts).first()
            if stat is None:
                # insert
                stat = repo_class(timestamp=record['timestamp'].split("T")[0], views_total=record['count'], views_uniques=record['uniques'])
            else:
                # update
                stat.views_total = record['count']
                stat.views_uniques = record['uniques']

            self.session.add(stat)

        self.session.commit()

    def getResults(self, from_date, to_date, repo_code=None):

        if (repo_code is None) or (repo_code is'wisdem_floris'):
            repo_class = Stats
        elif repo_code is 'nrel_floris':
            repo_class = StatsNRELFloris
        elif repo_code is 'wfc_tools':
            repo_class = StatswfcTools

        if from_date is None:
            stat = self.session.query(repo_class).order_by(repo_class.timestamp).first()
            if stat is not None:
                from_date = stat.timestamp.strftime('%Y-%m-%d')
            else:
                from_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if to_date is None:
            to_date = datetime.datetime.today().strftime('%Y-%m-%d')
        # records = self.session.query(repo_class).all()
        query = self.session.query(repo_class).filter(repo_class.timestamp <= to_date).filter(repo_class.timestamp >= from_date)
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
        results_wisdem = pd.read_sql_query("Select sum(clones_uniques) as total_unique_clones, sum(views_uniques) as total_unique_views, min(timestamp) as from_date, max(timestamp) as to_date from  stats;", self.engine)
        results_floris = pd.read_sql_query("Select sum(clones_uniques) as total_unique_clones, sum(views_uniques) as total_unique_views, min(timestamp) as from_date, max(timestamp) as to_date from  statsnrelfloris;", self.engine)
        results_wfctools = pd.read_sql_query("Select sum(clones_uniques) as total_unique_clones, sum(views_uniques) as total_unique_views, min(timestamp) as from_date, max(timestamp) as to_date from  statswfctools;", self.engine)
        return results_wisdem, results_floris, results_wfctools
