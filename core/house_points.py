from appwrite.services.databases import Databases

from dbsetup.common import setup_collection
from dbsetup.house_points import HOUSE_POINTS_ATTRIBUTES


def setup(db: Databases, context: dict) -> None:
    """
    Setup house points collection.
    :param db: appwrite database instance
    :param context: context dictionary
    """
    setup_collection(
        attributes=HOUSE_POINTS_ATTRIBUTES,
        db=db,
        context=context,
    )
