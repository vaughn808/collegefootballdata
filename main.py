import cfbd
import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

import csv

def getRecruitPlayers(configuration):
    '''Used to get player recruits by team and year'''
    school_types = ['HighSchool', 'JUCO', 'PrepSchool']
    years = [2010, 2011]

    api_instance = cfbd.RecruitingApi(cfbd.ApiClient(configuration))
    
    # name of csv file 
    filename = "./data/playersByTeam.csv"
    fieldnames = ['year','committed_to', 'recruit_type', 'ranking','stars']

    # writing to csv file 
    with open(filename, 'a') as csvfile:
        player_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if os.path.exists(filename):
            player_writer.writeheader()

        for school_type in school_types:
            for year in years:
                year = year # int | Recruiting class year (required if team no specified) (optional)
                classification = school_type # 'HighSchool' # str | Type of recruit (HighSchool, JUCO, PrepSchool) (optional) (default to HighSchool)
                position = '' # 'position_example' # str | Position abbreviation filter (optional)
                state = '' # 'state_example' # str | State or province abbreviation filter (optional)
                team = 'Texas' #'Alabama' # str | Committed team filter (required if year not specified) (optional)

                # try:
                # Player recruiting ratings and rankings
                api_response = api_instance.get_recruiting_players(year=year, classification=classification, position=position, state=state, team=team)

                if len(api_response) > 0:
                    for item in api_response:
                        player_writer.writerow({'year': item.year, 'committed_to': item.committed_to, 'recruit_type': item.recruit_type, 'ranking': item.ranking, 'stars': item.stars})

def main():
    load_dotenv(find_dotenv())

    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = os.environ.get("API_KEY")
    configuration.api_key_prefix['Authorization'] = 'Bearer'

    getRecruitPlayers(configuration)

if __name__ == "__main__":
    main()
