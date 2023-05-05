import logging

import httpx
from appwrite.services.databases import Databases

from dbsetup.buildspace_leaderboard import LEADERBOARD_ATTRIBUTES
from dbsetup.common import setup_collection
from utils import docbuilder
from utils.prep_leaderboard_data import prep_data


async def load_leaderboard(url: str, token: str) -> list:
    """
    Fetch leader board data from the URL
    :param url: leader board url
    :param token: authorization token
    """
    logging.info("------------------------------------------------")
    logging.info("Starting leader board updater")

    # fetch leader board
    leaderboard_data = []
    async with httpx.AsyncClient() as client:
        fetch_next_page = True
        page_number = 0
        total_fetched = 0
        page_offset = None

        # api returns only 100 rows at a time
        # run until we have all rows
        base_url = current_page_url = url
        while fetch_next_page:
            # offset to next page
            if page_offset:
                current_page_url = f"{base_url}?offset={page_offset}"

            logging.info(f"Fetching page {page_number}...")
            # fetch page data
            response = await client.get(
                current_page_url,
                headers={"Authorization": token},
            )

            if response.status_code != 200:
                logging.error(f"Error fetching leader board: {response.text}")
                break

            response_data = response.json()
            page_offset = response_data.get("offset", None)
            records = response_data["records"]
            total_rows = len(records)
            leaderboard_data.extend(records)

            page_number += 1
            total_fetched += total_rows

            logging.info(f"Current page: {total_rows} Total: {total_fetched}")
            logging.info("------------------------------------------------")

            if not page_offset:
                fetch_next_page = False
                logging.info("Finished loading leaderboard")

    return leaderboard_data


async def update_leaderboard(
    url: str,
    token: str,
    db: Databases,
    context: dict,
) -> None:
    """
    Fetch leader board data and upload to appwrite database.
    :param url: leader board url
    :param token: authorization token
    :param db: appwrite database instance
    :param context: context dictionary
    """
    # setup collection
    setup_collection(attributes=LEADERBOARD_ATTRIBUTES, db=db, context=context)

    # fetch leader board
    leaderboard_data = await load_leaderboard(url=url, token=token)

    # ignore unverified data and sort by points
    leaderboard_data = [
        ele for ele in leaderboard_data if ele["fields"].get("verified", False)
    ]
    leaderboard_data = sorted(
        leaderboard_data,
        key=lambda x: x["fields"]["points"],
        reverse=True,
    )

    total_rows = len(leaderboard_data)
    total_errors = 0
    total_inserted = 0
    total_ignored = 0
    total_updated = 0
    houses = {}

    for rank, ele in enumerate(leaderboard_data):
        row_data = ele["fields"]
        row_id = ele["id"]
        row_data["rank"] = rank + 1

        # calculate sum of score for all houses
        house = row_data["house"]
        points = row_data["points"]
        houses[house] = houses.get(house, 0) + points

        processed_data = prep_data(row=row_data)
        if not processed_data:
            logging.info("------------------------------------------------")
            total_ignored += 1
            continue

        # create a document if it doesn't exist, otherwise update it
        try:
            document_exists = docbuilder.create_document(
                db=db,
                data=processed_data,
                document_id=row_id,
                context=context,
            )
            if document_exists:
                docbuilder.update_document(
                    db=db,
                    data=processed_data,
                    document_id=row_id,
                    context=context,
                )
                total_updated += 1
            else:
                total_inserted += 1
        except Exception as e:
            total_errors += 1
            logging.info("-----------------------------------------------")
            logging.info(processed_data)
            logging.info(e)
            logging.info("-----------------------------------------------")

    # Update house points
    points_context = context["points_context"]
    for house, points in houses.items():
        docbuilder.create_document(
            db=db,
            data={"house": house, "points": points},
            document_id=house,
            context=points_context,
        )
    logging.info("------------------------------------------------")
    logging.info(f"Total rows: {total_rows}")
    logging.info(f"Total inserted: {total_inserted}")
    logging.info(f"Total updated: {total_updated}")
    logging.info(f"Total ignored: {total_ignored}")
    logging.info(f"Total errors: {total_errors}")
    logging.info("------------------------------------------------")
