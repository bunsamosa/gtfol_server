import logging

from appwrite.services.databases import Databases

from utils.attribute_builder import create_attribute


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
        collection["name"] == context["collection_name"]
        for collection in collections["collections"]
    )


def setup_collection(attributes: dict, db: Databases, context: dict) -> None:
    """
    Setup tweets collection and document attributes
    :param db: appwrite database instance
    :param context: context dictionary
    """
    # check if collection exists
    if check_collection(db, context):
        logging.info(f"Collection {context['collection_name']} already exists")
        return

    logging.info(f"Creating collection {context['collection_name']}")
    # create collection
    db.create_collection(
        database_id=context["database_id"],
        collection_id=context["collection_id"],
        name=context["collection_name"],
        document_security=False,
    )

    # create attributes
    for attribute, metadata in attributes.items():
        create_attribute(
            attribute=attribute,
            attr_type=metadata["type"],
            metadata=metadata,
            db=db,
            context=context,
        )
    logging.info(f"Collection {context['collection_name']} created")
