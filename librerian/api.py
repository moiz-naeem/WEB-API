from flask import Blueprint
from flask_restful import Api

from librerian.resources.user import UserCollection, UserItem
from librerian.resources.library import LibraryCollection, LibraryItem
from librerian.resources.book import BookCollection, BookItem
from librerian.resources.work import WorkCollection, WorkItem

from librerian.utils import UserConverter, LibraryConverter, BookConverter 

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(UserCollection, "/users/")
api.add_resource(UserItem, "/users/<user:user>/")

api.add_resource(LibraryCollection,
    "/libraries/",
    "/users/<user:user>/libraries/"
)

api.add_resource(LibraryItem,
    "/libraries/<library:library>/",
    "/users/<user:user>/libraries/<library:library>/"
)

api.add_resource(BookCollection,
    "/libraries/<library:library>/books/",
    "/users/<user:user>/libraries/<library:library>/books/"
)
api.add_resource(BookItem,
    "/libraries/<library:library>/books/<book:book>/",
    "/users/<user:user>/libraries/<library:library>/books/<book:book>/"
)

