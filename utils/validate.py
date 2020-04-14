"""School name validation"""
import os
import asyncio
import pandas as pd

school_list = pd.read_csv(os.path.join(os.path.dirname(__file__), 'schools.csv'))


@asyncio.coroutine
async def school_check(name: str):
    """school_check
    ---
    Asynchronous Function

    Checks to see if the name is in schools.csv

    Arguments:
    ---
        name {str} -- Name of the school that the user wants to check against the list.

    Returns:
    ---
        bool -- Returns true if :ref:`name` is in :ref:`schools.csv`
    """
    return name in school_list.Institution_Name.values


@asyncio.coroutine
async def region_select(name: str):
    """region_select
    ---
    Asynchronous Function

    Maps a regions for a school, :refs:`name`. Looks school name in the 'Institution_Name' column,
        if it finds a match then pulls from 'Regions' column.

    Arguments:
    ---
        name {str} -- Name of the school that needs a region.

    Returns:
    ---
        str -- The region which the school has been mapped to.
    """
    return school_list.Regions.values[school_list.Institution_Name == name][0]


@asyncio.coroutine
async def school_search(name: str):
    """school_search
    ---
    Asynchronous Function

    Searchs for part of a school name in the 'Institution_Name' column in schools.csv.
    Turns the 'Instituion_Name' into a series then gets all names using pandas.Series.str.contains.

    Arguments:
    ---
        name {str} -- Part of the name the user wants to search for.

    Returns:
    ---
        list -- Schools which had :ref:`name` in them.
    """

    return school_list.Institution_Name.values[
                school_list["Institution_Name"].str.contains(name, case=False)]


@asyncio.coroutine
async def state_list(state: str):
    """state_list
    ---
    Asynchronous Function

    Get a list of all schools in :ref:`state`.

    Arguments:
    ---
        state {str} -- The state to get all schools from.

    Returns:
    ---
        list -- List of all the schools in :ref:`state`.
    """
    return school_list.Institution_Name.values[school_list.States == state]