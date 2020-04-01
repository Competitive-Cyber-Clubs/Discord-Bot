"""Cogs
---
    All cogs responsible for commands.

    * :ref:`AdminCog` commands: list-admin, am-admin, add-admin.

    * :ref:`EventCog` has an event for members joining.

    * :ref:`HealthCog` has command check-heath which checks the make sure that role names match in
        the tables.Also updates the table if role names change or are removed.

    * :ref:`MiscCog` commands: ping, contact-admin.

    * :ref:`RankCog` commands: add-rank.

    * :ref:`RegionsCog` commands: add-region, list-region.

    * :ref:`SchoolCog` commands: add-school, join-school, list-schools, validate-school,
        state-search, import-school.
"""
from .admin import AdminCog
from .events import EventsCog
from .health import HealthCog
from .misc import MiscCog
from .rank import RankCog
from .regions import RegionCog
from .schools import SchoolCog
__all__ = ["AdminCog",
           "RegionCog",
           "RankCog",
           "MiscCog",
           "EventsCog",
           "SchoolCog",
           "HealthCog"]
