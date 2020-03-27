"""Imports cogs"""
from .admin import AdminCog
from .regions import RegionCog
from .rank import RankCog
from .misc import MiscCog
from .events import EventsCog
from .schools import SchoolCog
from .health import HealthCog
from .contact import ContactCog
__all__ = ["AdminCog", "RegionCog", "RankCog", "MiscCog",
           "EventsCog", "SchoolCog", "HealthCog", "ContactCog"]
