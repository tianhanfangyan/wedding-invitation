from . import main

from app import get_logger

logger = get_logger(__name__)


@main.route("/", methods=["GET"])
def index():
    return "hello world"

