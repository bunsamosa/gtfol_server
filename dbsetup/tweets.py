from appwrite.services.databases import Databases

from utils.attribute_builder import create_attribute

TWEETS_CID = "tweets"
TWEETS_ATTRIBUTES = {
    "created_on": {
        "type": "datetime",
        "required": True,
        "default": None,
        "array": False,
    },
    "text": {
        "type": "string",
        "size": 500,
        "required": True,
        "default": None,
        "array": False,
    },
    "bookmark_count": {
        "type": "integer",
        "required": True,
        "min": 0,
        "max": 100000000,
        "default": 0,
        "array": False,
    },
    "quote_counts": {
        "type": "integer",
        "required": True,
        "min": 0,
        "max": 100000000,
        "default": 0,
        "array": False,
    },
    "likes": {
        "type": "integer",
        "required": True,
        "min": 0,
        "max": 100000000,
        "default": 0,
        "array": False,
    },
    "reply_counts": {
        "type": "integer",
        "required": True,
        "min": 0,
        "max": 100000000,
        "default": 0,
        "array": False,
    },
    "retweet_counts": {
        "type": "integer",
        "required": True,
        "min": 0,
        "max": 100000000,
        "default": 0,
        "array": False,
    },
    "language": {
        "type": "string",
        "size": 10,
        "required": True,
        "default": None,
        "array": False,
    },
    "vibe": {
        "type": "string",
        "size": 10,
        "required": False,
        "default": None,
        "array": False,
    },
    "place": {
        "type": "string",
        "size": 1000,
        "required": False,
        "default": None,
        "array": False,
    },
    "media": {
        "type": "string",
        "size": 1000,
        "required": False,
        "default": None,
        "array": True,
    },
    "hashtags": {
        "type": "string",
        "size": 1000,
        "required": False,
        "default": None,
        "array": True,
    },
    "symbols": {
        "type": "string",
        "size": 1000,
        "required": False,
        "default": None,
        "array": True,
    },
}


def check_collection(db: Databases, context: dict) -> bool:
    """
    Check if tweets collection exists
    :param db: appwrite database instance
    :param context: context dictionary
    """
    collections = db.list_collections(database_id=context["database_id"])

    if not collections:
        return False

    return any(
        collection["name"] == "tweets"
        for collection in collections["collections"]
    )


def setup_collection(db: Databases, context: dict) -> None:
    """
    Setup tweets collection and document attributes
    :param db: appwrite database instance
    :param context: context dictionary
    """
    # check if collection exists
    if check_collection(db, context):
        return

    # create collection
    db.create_collection(
        database_id=context["database_id"],
        collection_id=context["collection_id"],
        name=context["collection_name"],
        document_security=False,
    )

    # create attributes
    for attribute, metadata in TWEETS_ATTRIBUTES.items():
        create_attribute(
            attribute=attribute,
            attr_type=metadata["type"],
            metadata=metadata,
            db=db,
            context=context,
        )
