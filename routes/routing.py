from flask import Blueprint, request, jsonify
from services.routing_service import dijkstra_route
from flask_jwt_extended import jwt_required

bp = Blueprint("routing", __name__, url_prefix="/route")

@bp.route("/dijkstra", methods=["POST"])
@jwt_required()
def route_dijkstra():
    data = request.json

    result = dijkstra_route(
        data["start_lon"],
        data["start_lat"],
        data["end_lon"],
        data["end_lat"]
    )

    return jsonify(result)
