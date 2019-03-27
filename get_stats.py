import github_stats as ghs
import database as dbc

# This script will retrieve github stats via their API and store in a postgres database

db = dbc.Database()

# WISDEM first
traffic = ghs.RepoTraffic()
views = traffic.get_views()
clones = traffic.get_clones()

if clones['clones']:
    db.addClones(clones['clones'])

if views['views']:
    db.addViews(views['views'])

# NREL/FLORIS 
traffic = ghs.RepoTraffic(owner='NREL', repository='floris')
views = traffic.get_views()
clones = traffic.get_clones()

if clones['clones']:
    db.addClones(clones['clones'],repo_code='nrel_floris')

if views['views']:
    db.addViews(views['views'],repo_code='nrel_floris')

# wfc_tools 
traffic = ghs.RepoTraffic(owner='NREL', repository='wfc_tools')
views = traffic.get_views()
clones = traffic.get_clones()

if clones['clones']:
    db.addClones(clones['clones'],repo_code='wfc_tools')

if views['views']:
    db.addViews(views['views'],repo_code='wfc_tools')