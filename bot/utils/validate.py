"""School name validation"""
import os
import logging
from datetime import datetime
import aiohttp
import pandas as pd

log = logging.getLogger("bot")


async def update_list(bot, download: bool = False) -> None:
    """
    Update list

    Update the school list
    :param bot: The bot class to update the dataframe for
    :param download: Download the list
    :return: None
    """
    if download:
        log.info("Downloading new list")
        try:
            os.replace("school_list.csv", "school_list.csv.bak")
        except OSError:
            log.debug("School list did not exist")
        csv_url = "https://raw.githubusercontent.com/Competitive-Cyber-Clubs/School-List/master/school_list.csv"  # noqa: E501 pylint: disable=line-too-long
        with open("school_list.csv", mode="w", encoding="utf-8") as new_list:
            async with aiohttp.ClientSession() as session, session.get(csv_url) as resp:
                new_list.write("\n".join((await resp.text(encoding="utf-8")).splitlines()))
    bot.list_updated = datetime.utcnow()
    bot.school_list = pd.read_csv("school_list.csv", encoding="utf-8")


async def school_check(school_list: pd.DataFrame, name: str) -> bool:
    """
    School check

    Checks to see if the name is in school_list.csv

    :param school_list: Dataframe of lists
    :type school_list: pandas.DataFrame
    :param name: Name of the school that the member wants to check against the list.
    :type name: str
    :return: Name is in school_list
    """
    return name in school_list.Institution_Name.values


async def region_select(school_list: pd.DataFrame, name: str) -> str:
    """
    Region select

    Maps a regions for a school, :refs:`name`. Looks school name in the 'Institution_Name' column,
        if it finds a match then pulls from 'Regions' column.

    :param school_list: Dataframe of schools
    :type school_list: pandas.DataFrame
    :param name: Name of the school that needs a region.
    :type name: str
    :return:
    """
    return school_list.Regions.values[school_list.Institution_Name == name][0]


async def school_search(school_list: pd.DataFrame, name: str) -> list:
    """
    School Search

    Searches for part of a school name in the 'Institution_Name' column in school_list.
    Turns the 'Institution_Name' into a series then gets all names using pandas.Series.str.contains.

    :param school_list: Dataframe of schools
    :type school_list: pandas.DataFrame
    :param name: Part of the name the member wants to search for.
    :type name: str
    :return: All possible matches
    :rtype: list
    """
    return school_list.Institution_Name.values[
        school_list["Institution_Name"].str.contains(name, case=False)
    ]


async def state_list(school_list: pd.DataFrame, state: str) -> list:
    """
    State List
    Get a list of all schools in state.
    :param school_list: Dataframe of schools
    :type school_list: pandas.DataFrame
    :param state: State to get all schools from.
    :return: Schools in the state
    :rtype: list
    """
    return school_list.Institution_Name.values[school_list.States == state]
