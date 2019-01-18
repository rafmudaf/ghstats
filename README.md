# GitHub Stats
This is a start to tracking github repository views and clones over time. Github lets you see the activity for the last 2 weeks via the Traffic tab or their API.  This code allows you to store the activity to analyze over longer periods of time.

Functionality is made up of the following components:
1. A postgres database
1. A server that can run scheduled tasks / cron jobs
1. The code in this repository
1. A jupyter notebook with examples for retrieving data from the database and visualizating it.

## Installation
* Setup a postgres database.  You will only need to:
    * create the database
    * create a user
    * grant privileges to the user on the database.  

    The database tables will be created automatically the first time that the code is run.

* Clone this repository on a server that can run scheduled tasks.  
* Generate a GitHub [personal access token](https://github.com/settings/tokens)
* Copy the `authentication_template.json` file and rename the copy `authentication.json`.  Do not commit the new `authentication.json` file as it will contain credentials for accessing GitHub and the postgres database.
* Fill out `authentication.json` with the repo that you want to track, your personal access token, and the credentials for the postgres database
* Configure a cron task or scheduled task to run the python script called `get_stats.py`, which will get repo statistics from GitHub and store them in the postgres database.  The statistics are:
    * Total Unique Clones of the repo per day
    * Total Unique Views of the repo per day
        
   Once the task is scheduled, statistics will be stored to the database everyday 

## Data Visualization
The `notebooks` folder contains a jupyter notebook named `githubStats` that can be used as a starting point for visualizing the data stored in the database.
