from typing import Any
from typing import Dict

from appwrite.services.databases import Databases


def create_attribute(
    attribute: str,
    attr_type: str,
    metadata: Dict,
    db: Databases,
    context: Dict,
) -> Any:
    """
    Create an attribute for a collection
    :param attribute: attribute name
    :param attr_type: attribute type
    :param metadata: attribute metadata
    :param db: appwrite database instance
    :param context: context dictionary
    """
    # do not pass default parameter for required attributes
    if attr_type == "datetime":
        if metadata["required"] or metadata["array"]:
            return db.create_datetime_attribute(
                database_id=context["database_id"],
                collection_id=context["collection_id"],
                key=attribute,
                required=metadata["required"],
                array=metadata["array"],
            )
        else:
            return db.create_datetime_attribute(
                database_id=context["database_id"],
                collection_id=context["collection_id"],
                key=attribute,
                required=metadata["required"],
                default=metadata["default"],
                array=metadata["array"],
            )

    elif attr_type == "integer":
        if metadata["required"] or metadata["array"]:
            return db.create_integer_attribute(
                database_id=context["database_id"],
                collection_id=context["collection_id"],
                key=attribute,
                required=metadata["required"],
                min=metadata["min"],
                max=metadata["max"],
                array=metadata["array"],
            )
        else:
            return db.create_integer_attribute(
                database_id=context["database_id"],
                collection_id=context["collection_id"],
                key=attribute,
                required=metadata["required"],
                min=metadata["min"],
                max=metadata["max"],
                default=metadata["default"],
                array=metadata["array"],
            )

    elif attr_type == "float":
        if metadata["required"] or metadata["array"]:
            return db.create_float_attribute(
                database_id=context["database_id"],
                collection_id=context["collection_id"],
                key=attribute,
                required=metadata["required"],
                min=metadata["min"],
                max=metadata["max"],
                array=metadata["array"],
            )
        else:
            return db.create_float_attribute(
                database_id=context["database_id"],
                collection_id=context["collection_id"],
                key=attribute,
                required=metadata["required"],
                min=metadata["min"],
                max=metadata["max"],
                default=metadata["default"],
                array=metadata["array"],
            )

    elif attr_type == "boolean":
        if metadata["required"] or metadata["array"]:
            return db.create_boolean_attribute(
                database_id=context["database_id"],
                collection_id=context["collection_id"],
                key=attribute,
                required=metadata["required"],
                array=metadata["array"],
            )
        else:
            return db.create_boolean_attribute(
                database_id=context["database_id"],
                collection_id=context["collection_id"],
                key=attribute,
                required=metadata["required"],
                default=metadata["default"],
                array=metadata["array"],
            )

    elif attr_type == "string":
        if metadata["required"] or metadata["array"]:
            return db.create_string_attribute(
                database_id=context["database_id"],
                collection_id=context["collection_id"],
                key=attribute,
                size=metadata["size"],
                required=metadata["required"],
                array=metadata["array"],
            )
        else:
            return db.create_string_attribute(
                database_id=context["database_id"],
                collection_id=context["collection_id"],
                key=attribute,
                size=metadata["size"],
                required=metadata["required"],
                default=metadata["default"],
                array=metadata["array"],
            )
    else:
        raise ValueError(f"Invalid attribute type: {attr_type}")
