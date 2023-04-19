from typing import Any

from appwrite.services.databases import Databases


def create_document(
    db: Databases,
    data: dict,
    document_id: Any,
    context: dict,
) -> bool:
    """
    Create a document in the database.
    :param db: appwrite database instance
    :param data: data to upload
    :param document_id: id of document
    :param context: context dictionary
    :return: True if document already exists, False otherwise
    """
    document_exists = False
    try:
        db.create_document(
            database_id=context["database_id"],
            collection_id=context["collection_id"],
            document_id=document_id,
            data=data,
        )
    except Exception as e:
        if "requested ID already exists" in str(e):
            document_exists = True
        else:
            raise e

    return document_exists


def update_document(
    db: Databases,
    data: dict,
    document_id: Any,
    context: dict,
) -> None:
    """
    Update a document in the database.
    :param db: appwrite database instance
    :param data: data to upload
    :param document_id: id of document
    :param context: context dictionary
    :return: None
    """
    db.update_document(
        database_id=context["database_id"],
        collection_id=context["collection_id"],
        document_id=document_id,
        data=data,
    )
