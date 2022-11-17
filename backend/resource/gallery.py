from flask import jsonify
from flask_restful import Resource, reqparse

import backend.utils as utils
from backend import db_models as dbm


def get_query_with_medium_filter(curr_query, medium_filter):
    medium_query = curr_query.filter(
        dbm.ArtworkModel.medium.contains(medium_filter[0])
    )

    for i in range(1, len(medium_filter)):
        medium_query = medium_query.union(
            curr_query.filter(
                dbm.ArtworkModel.medium.contains(medium_filter[i])
            )
        )

    return medium_query


def get_query_with_created_date_filter(curr_query, created_date_filter):
    min_date, max_date = sorted(
        [date.strip() for date in created_date_filter.split("-")]
    )

    curr_query = curr_query.filter(dbm.ArtworkModel.created_date >= min_date)
    curr_query = curr_query.filter(dbm.ArtworkModel.created_date <= max_date)

    return curr_query


def get_query_with_minmax_filter(curr_query, db_col_name, minmax_filter):
    min_val, max_val = sorted(
        [int(value.strip()) for value in minmax_filter.split("-")]
    )

    curr_query = curr_query.filter(db_col_name >= min_val)
    curr_query = curr_query.filter(db_col_name <= max_val)

    return curr_query


def get_query_with_filter_args(curr_query, filter_args):
    if "artist_filter" in filter_args and filter_args["artist_filter"]:
        curr_query = curr_query.filter(
            dbm.ArtworkModel.artist.in_(filter_args["artist_filter"])
        )

    if "medium_filter" in filter_args and filter_args["medium_filter"]:
        curr_query = get_query_with_medium_filter(
            curr_query=curr_query,
            medium_filter=filter_args["medium_filter"],
        )

    if (
        "created_date_filter" in filter_args
        and filter_args["created_date_filter"]
    ):
        curr_query = get_query_with_created_date_filter(
            curr_query=curr_query,
            created_date_filter=filter_args["created_date_filter"],
        )

    if "min_value_filter" in filter_args and filter_args["min_value_filter"]:
        curr_query = get_query_with_minmax_filter(
            curr_query=curr_query,
            db_col_name=dbm.ArtworkModel.min_value,
            minmax_filter=filter_args["min_value_filter"],
        )

    if "width_filter" in filter_args and filter_args["width_filter"]:
        curr_query = get_query_with_minmax_filter(
            curr_query=curr_query,
            db_col_name=dbm.ArtworkModel.width,
            minmax_filter=filter_args["width_filter"],
        )

    if "height_filter" in filter_args and filter_args["height_filter"]:
        curr_query = get_query_with_minmax_filter(
            curr_query=curr_query,
            db_col_name=dbm.ArtworkModel.height,
            minmax_filter=filter_args["height_filter"],
        )

    return curr_query


def get_ordered_query(curr_query, order_by, order_decrease):
    db_col_name = str()

    if order_by == "genre":
        db_col_name = dbm.ArtworkModel.genre

    elif order_by == "medium":
        db_col_name = dbm.ArtworkModel.medium

    elif order_by == "surface":
        db_col_name = dbm.ArtworkModel.surface

    elif order_by == "artist":
        db_col_name = dbm.ArtworkModel.artist

    elif order_by == "created_date":
        db_col_name = dbm.ArtworkModel.created_date

    elif order_by == "min_value":
        db_col_name = dbm.ArtworkModel.min_value

    return curr_query.order_by(
        db_col_name.desc() if order_decrease else db_col_name
    )


def get_artworks_by_query(curr_query):
    """
    get the artwork data using the giving query, then format them to list of
    dictionary

    :param curr_query: the query will be used to get the artwork data from the
        database
    :return: list of dict. each dict repr an artwork data.
        [
            {
                "info": {
                    "uid": <int>,
                    "name": <str>,
                    "genre": <str>,
                    "medium": <str>,
                    ...
                    # fields list can be seen at db_models.ArtworkModel
                },
                "artpic": <base64 str repr the picture of the art>
            },
            {...},
            {...},
        ]
    """
    artworks = curr_query.all()

    for i in range(len(artworks)):
        item = dict()

        item["info"] = artworks[i].to_dict()
        item["artpic"] = utils.get_bytestr_artpic(
            artwork_uid=item["info"]["uid"]
        )

        artworks[i] = item

    return artworks


class Gallery(Resource):
    get_args = reqparse.RequestParser()
    get_args.add_argument(
        name="artwork_num",
        type=int,
        help="Number of artwork will be return for this request.",
        location="values",
    )
    get_args.add_argument(
        name="artist_filter",
        type=str,
        action="append",
        help="List of str, each str is an artist name "
        "that the search will filter by",
        location="values",
    )
    get_args.add_argument(
        name="medium_filter",
        type=str,
        action="append",
        help="List of str, each str is a medium name "
        "that the search will filter by",
        location="values",
    )
    get_args.add_argument(
        name="created_date_filter",
        type=str,
        help="A string repr the earliest date and latest date for the creation"
        " of the artwork. Format: <min_date>-<max-date>, and any artwork "
        "created within this range will be returned.",
        location="values",
    )
    get_args.add_argument(
        name="min_value_filter",
        type=str,
        help="A string repr the lowest value of min_value and highest value of"
        " min_value of the artwork. Format: <lowest min_value>-<highest "
        "min_value>, and any artwork have min_value within this range "
        "will be returned.",
        location="values",
    )
    get_args.add_argument(
        name="width_filter",
        type=str,
        help="A string repr the lowest width and highest width of the artwork."
        " Format: <lowest width>-<highest width, and any artwork have "
        "its width within this range will be returned.",
        location="values",
    )
    get_args.add_argument(
        name="height_filter",
        type=str,
        help="A string repr the lowest height and highest height of the "
        "artwork. Format: <lowest height>-<highest height, and any "
        "artwork have its height within this range will be returned.",
        location="values",
    )
    get_args.add_argument(
        name="order_by",
        choices=[
            "genre",
            "medium",
            "surface",
            "artist",
            "created_date",
            "min_value",
        ],
        default="created_date",
        type=str,
        help="A string repr the criteria that the artworks will be sort by. "
        "The only available value can be seen at the choices kwarg for "
        "this query argument.",
        location="values",
    )
    get_args.add_argument(
        name="order_decrease",
        choices=[True, False],
        default=False,
        type=bool,
        help="A boolean repr if the order be increasing or decreasing. This "
        "query argument is intended to be used with the order_by query "
        "argument.",
        location="values",
    )

    def get(self):
        """
        get artworks that fit with all the filter given through query argument,
        ordered them if required and return a list of artwork data. List of
        query argument can be seen at get_args var above.

        :return: list (before jsonify) of artwork data
            [
                {
                    "info": {
                        "uid": <int>,
                        "name": <str>,
                        "genre": <str>,
                        "medium": <str>,
                        ...
                        # fields list can be seen at db_models.ArtworkModel
                    },
                    "artpic": <base64 str repr the picture of the art>
                },
                {...},
                {...},
            ]
        """
        query = dbm.ArtworkModel.query.filter(dbm.ArtworkModel.is_sold == 0)

        endpoint_args = self.get_args.parse_args()
        query = get_query_with_filter_args(
            curr_query=query,
            filter_args=endpoint_args,
        )

        query = get_ordered_query(
            curr_query=query,
            order_by=endpoint_args["order_by"],
            order_decrease=endpoint_args["order_decrease"],
        )

        if endpoint_args["artwork_num"]:
            query = query.limit(endpoint_args["artwork_num"])

        artworks = get_artworks_by_query(query)
        return jsonify(artworks)
