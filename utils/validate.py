"""School name validation"""
import os
import asyncio
import pandas as pd

school_list = pd.read_csv(os.path.join(os.path.dirname(__file__), 'schools.csv'))


@asyncio.coroutine
async def school_check(name: str):
    """Checks to see if the name is in the list"""
    if name in school_list.Institution_Name.values:
        return True
    return False


@asyncio.coroutine
async def school_search(name: str):
    """Searchs for school"""
    possible_schools = []

    for school in school_list.Institution_Name.values:
        if name in school:
            possible_schools.append(school)
    return possible_schools


@asyncio.coroutine
async def region_select(name: str):
    """Maps a regions for a school"""
    region = school_list.Regions.values[school_list.Institution_Name == name][0]
    return region


@asyncio.coroutine
async def state_list(state: str):
    """Returns a list of all schools in a state"""
    schools_in_state = school_list.Institution_Name.values[school_list.States == state]
    return schools_in_state
