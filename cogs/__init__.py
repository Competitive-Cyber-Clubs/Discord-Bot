"""
Imports cogs


* AdminCog commands: list-admin, am-admin, add-admin

* ContactCog commands: contact-admin

* EventCog has an event for members joining
* HealthCog has command check-heath which checks the make sure that role names match in the tables.
     Also updates the table if role names change or are removed.
* MiscCog commands: ping
* RankCog commands: add-rank
* RegionsCog commands: add-region, list-region
* SchoolCog commands: add-school, join-school, list-schools, validate-school, state-search,
    import-school
"""
from .admin import AdminCog
from .contact import ContactCog
from .events import EventsCog
from .health import HealthCog
from .misc import MiscCog
from .rank import RankCog
from .regions import RegionCog
from .schools import SchoolCog
__all__ = ["AdminCog", "RegionCog", "RankCog", "MiscCog",
           "EventsCog", "SchoolCog", "HealthCog", "ContactCog"]
