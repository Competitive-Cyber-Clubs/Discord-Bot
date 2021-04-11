"""School name validation"""
import os
import logging
from datetime import datetime
import aiohttp
import pandas as pd


log = logging.getLogger("bot")


async def update_list(bot, download: bool = False):
    """update_list
    ---
    Updates the school_list
    """
    if download:
        log.info("Downloading new list")
        os.replace("school_list.csv", "school_list.csv.bak")
        csv_url = "https://raw.githubusercontent.com/Competitive-Cyber-Clubs/School-List/master/school_list.csv"  # noqa: E501 pylint: disable=line-too-long
        new_list = open("school_list.csv", mode="w", encoding="utf-8")
        async with aiohttp.ClientSession() as session:
            async with session.get(csv_url) as resp:
                new_list.write(await resp.text(encoding="utf-8"))
        new_list.close()
        bot.list_updated = datetime.utcnow()
    bot.school_list = pd.read_csv("school_list.csv", encoding="utf-8")


async def school_check(school_list, name: str) -> bool:
    """school_check
    ---
    Asynchronous Function

    Checks to see if the name is in school_list.csv

    Arguments:
    ---
        name {str} -- Name of the school that the user wants to check against the list.

    Returns:
    ---
        bool -- Returns true if :ref:`name` is in :ref:`school_list.csv`
    """
    return name in school_list.Institution_Name.values


async def region_select(school_list, name: str) -> str:
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


async def school_search(school_list: pd.DataFrame, name: str) -> list:
    """school_search
    ---
    Asynchronous Function

    Searches for part of a school name in the 'Institution_Name' column in school_list.csv.
    Turns the 'Institution_Name' into a series then gets all names using pandas.Series.str.contains.

    Arguments:
    ---
        name {str} -- Part of the name the user wants to search for.

    Returns:
    ---
        list -- Schools which had :ref:`name` in them.
    """
    return school_list.Institution_Name.values[
        school_list["Institution_Name"].str.contains(name, case=False)
    ]


async def state_list(school_list, state: str) -> list:
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
