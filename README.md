# MSiA423 - NCAA Tournament Predictor

<!-- toc -->
- [Project Charter](#project-charter)
  * [Vision](#vision)
  * [Mission](#mission)
  * [Success Criteria](success-criteria)
- [Backlog](#backlog)
  * [Planning](#planning)
  * [Backlog](#backlog)
  * [Icebox](#icebox)
- [Final Repo Instructions](#final-repo-instructions)


<!-- tocstop -->

## Project Charter

### Vision

The inspiration for this project comes from the unfortunate cancellation of the 2020 NCAA Division I Men’s Basketball Tournament due to the Covid-19 pandemic. Many die-hard college basketball fans lost the opportunity to watch their favorite team play in March Madness. We will never know exactly which 64 teams would have made the exciting tournament, nor how they would have fared in it. This app aims to uncover the truth to these unknowns by providing fans a predictive tool. This tool will not only be able to predict the outcomes of this year’s cancelled tournament, but can also be used in the future, even while the sport’s season is ongoing.

### Mission

The mission is to build an app that allows a user to predict which round their favorite team will make it in the NCAA tournament based on historical data. The Kaggle dataset used for this project contains various statistics for every D1 team in each year from 2015 to 2019 (the data is scraped from a website which contains data as early as 2008; I may scrape the data from 2008-2014 myself). These statistics include the team’s win percentage, the strength of the team’s conference, and other various offensive and defensive metrics. The data also contains the response variable: which round the team lost in the tournament in that given year. The user will enter their favorite team, and using the current date, the app will scrape that team’s statistics from the beginning of the current season to date from the website, and use this to predict the team’s outcome in the tournament. Because this approach relies on the website, perhaps the app will simply require the user to enter their team’s statistics which involves no scraping while the app is in use.

### Success criteria

*Machine learning performance metric:*
Average cross-validation F1-score will be used to access the performance of the model. We will aim to achieve an F1-score of 0.7. This may have to be altered due to the multiclass nature of the model. Another success criterion will be to predict outcomes for all teams in 2020, and see if the number of teams predicted to reach each round closely matches the actual format of the tournament (i.e. a perfect model would predict 64 teams to make the first round, 32 to make the second round, etc.). A sum of differences less than 15 will be considered successful (ex. if the model predicts 67 teams to make the tournament, 30 teams to make the second round, etc. then this metric will be calculated like so: |64-67|+|32-30|+…).

*Business outcome metric:*
Ideally, users will use this app on a continuous basis as the NCAA basketball season progresses. As their favorite team racks up wins and losses, they can use the app to see how well their team would fare in the tournament assuming they continue along a similar trajectory for the remainder of the season. The metric used will be % of users retained from one month to the next.

## Backlog

### Planning

Initiative 1: Build a model to predict which round a team will make it to in the tournament.
- Epic 1: Gather data
  *	Story 1: Scrape data from website to obtain data in 2008-2014
    + http://barttorvik.com/trank.php?year=2020&sort=&lastx=0&hteam=&t2value=&conlimit=All&state=All&begin=20191101&end=20200201&top=0&quad=5&venue=All&type=All&mingames=0#
  *	Story 2: Combine scraped data with data already available (2015-2019)
    + https://www.kaggle.com/andrewsundberg/college-basketball-dataset
- Epic 2: Feature engineering
  *	Story 1: Ensure all features are proportions rather than aggregates so that a team’s statistics midseason can be used to predict tournament outcome
    + Ex. win % rather than total wins
  *	Story 2: Ensure that none of the predictors can alone capture the response variable
    + Ex. average power rating of a team’s conference rather than the team’s power rating
- Epic 3: Test different types of models
  *	Story 1: Tune random forest models using CV
    + Upsample minority classes within CV-folds
  *	Story 2: Tune boosted tree models using CV
    + Upsample minority classes within CV-folds
  *	Story 3: Tune neural network models using CV
    + Upsample minority classes within CV-folds
- Epic 4: Choose best model
  *	Story 1: Compare best random forest v. best boosted tree v. best neural network v. any other model attempted

Initiative 2: Build an app to allow a user to use the model.
- Epic 1: Build frontend
  *	Story 1: Create first home page option
    + User inputs their team name to initiate website scraping (alternatively, user must enter team name along with all statistics)
  *	Story 2: Create second home page option
    + Allow user to enter whatever statistics they please, rather than being forced to use a team’s current statistics
    + If user is not satisfied with how their team is predicted to perform, this will allow user to see if their team has potential to perform better by testing out new statistics
  *	Story 3: Building off Story 2, suggest areas for a team’s improvement
    + Develop an unsupervised model (PCA or clustering or a combination) to see what predictors are most important in predicting a more successful tournament run, and based on a set of statistics, suggest which statistics, if they were higher, would propel a team to the next round 
  *	Story 4: Create results page
    + Results page will reveal prediction
    + Option to alter statistics
    + Option to return to home page
- Epic 2: Integrate app with model

Initiative 3: Test the app
- Epic 1: Build local tests
  *	Story 1: Build local unit tests
  *	Story 2: Build local model reproducibility tests
- Epic 2: Integration testing
- Epic 3: A/B testing

Initiative 4: Sell app to NCAA and profit

### Backlog:

- Initiative1.Epic1.Story1 (4) - PLANNED
- Initiative1.Epic1.Story2 (0) - PLANNED
- Initiative1.Epic2.Story1 (0) - PLANNED
- Initiative1.Epic2.Story2 (0) - PLANNED
- Initiative1.Epic3.Story1 (2) - PLANNED
- Initiative1.Epic3.Story2 (2) - PLANNED
- Initiative1.Epic3.Story3 (2) - PLANNED
- Initiative1.Epic4.Story1 (4) - PLANNED

### Icebox:

- Initiative2.Epic1.Story1
- Initiative2.Epic1.Story2
- Initiative2.Epic1.Story3 (lowest priority)
- Initiative2.Epic1.Story4
- Initiative2.Epic2
- Initiative3.Epic1.Story1
- Initiative3.Epic1.Story2
- Initiative3.Epic2
- Initiative3.Epic3
- Initiative4

## Final Repo Instructions

### Step 1: Configuration

1. Set the following environment variables from the command line: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.

2. _(OPTIONAL)_ Set the environment variable S3_BUCKET to something else, if you don't want to use jjk555.

3. Decide if you want Cross validation to run or not. CV is a step in the model pipeline that takes 5-10 minutes and outputs a performance metric; it will run by default. Set the env variable GET_PERFORMANCE to False if you don't care to see this step in the pipeline or unit testing, otherwise do nothing.

4. _(OPTIONAL)_ Set SQLALCHEMY environment variables if you want to use an alternative engine string: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE. If you choose to do this, you will also need to set an additional three environment variables to True for the app to run; all three are outlined in step 5.

5. _(OPTIONAL)_ Set INCLUDE_INGESTION and/or INCLUDE_WRITING_PREDS_TO_DB if you want to see these steps conducted in the pipeline. If you set INCLUDE_INGESTION to True, it will do an example scrape (5 minutes), unless you set EXAMPLE_SCRAPE to True (then it will do the full 2-hour scrape).

6. Decide if you want to use RDS or local SQLite for app (or pipeline, if you choose to complete step 5). If you want local, set environment variable LOCAL_DB to True.

###Step 2: Running pipeline and tests.

1. Run this in command line to build docker image:

`docker build -t pipeline .` 

2. Run this in command line to run pipeline:

`winpty docker run --rm -it --mount type=bind,source="$(pwd)"/data/,target=/data/ --env AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY pipeline run.py`

Note: winpty is a Windows thing and may need to be removed.

Note: Any environment variables set other than AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY also need to be flagged. Insert the following into the command above directly before the word "pipeline": `--env <whatever env var you set>`. Do this for each additional environment variable you set.

3. Run this in command line to conduct unit tests:

`winpty docker run --rm -it --mount type=bind,source="$(pwd)"/data/,target=/data/ --env AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY pipeline test.py`

Note: If you set GET_PERFORMANCE to False, you should add `--env GET_PERFORMANCE` to the command above before the word pipeline.

###Step 2: Running app.

1. Run this in command line to build app image:

`docker build -f app/Dockerfile -t app .`    

2. Run this in command line to run app:

`docker run --rm --mount type=bind,source="$(pwd)",target=/app/ --mount type=bind,source="$(pwd)"/data/,target=/data/ --env LOCAL_DB -p 5000:5000 --name test app`

Note: If you set any environment variables in step 4 (SQLAlchemy env vars), they must be flagged in the command above. Insert the following into the command above directly after the word "LOCAL_DB": `--env <whatever env var you set>`. Do this for each additional environment variable you set.

Note: Sometimes you may need to run `docker container kill $(docker ps -q)` first.


