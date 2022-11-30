# NFL Predictions Dashboard

## Description
 
Project which aims to build a dashboard that predicts scores for each NFL team weekly, as well as team and individual player statistics.

## Design

- scrape data from [footballdb.com](https://www.footballdb.com/) starting from 1978
- scrape NFL player report data
- build and load data into a SQL database
- create machine learning models to predict future scores and stats
- display weekly predictions in a dashboard

## Entity Relationship Diagram

![Split into the tables, team, stadium, player, report, and game, with connecting tables inbetween. Please use the erd.drawio file for the XML version.](https://raw.githubusercontent.com/ColeBallard/nfl-predictions-dashboard/main/res/erd.drawio.png)

## Scrape

Here are the steps to replicate the scrape.

1. Clone the repository.

```shell
git clone https://github.com/ColeBallard/cybersecurity-jobs-analysis
```

2. Install the latest version of python. [Downloads.](https://www.python.org/downloads/)

3. Install dependencies (depends on your version of pip).

```shell
pip install pandas
pip install requests-html
pip install dataclasses
```

4. Run the getAllGames() function in the scrape.py file.

```shell
python -c "from scrape import *;getAllGames()"
```

## Contribution

If you have an idea or want to report a bug, please create an issue.

## **[Contact](https://coleb.io/contact)**
