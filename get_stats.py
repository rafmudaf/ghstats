import github_stats as ghs
import database as dbc

# This script will retrieve github stats via their API and store in a postgres database

db = dbc.Database()

traffic = ghs.RepoTraffic()
views = traffic.get_views()
clones = traffic.get_clones()

if clones['clones']:
    db.addClones(clones['clones'])

if views['views']:
    db.addViews(views['views'])
