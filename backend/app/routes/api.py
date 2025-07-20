from flask import Blueprint, jsonify, request
from app.models import FoodPost
from datetime import datetime

api_bp = Blueprint("api", __name__)

@api_bp.route("/food-items")
def get_food_items():
    now = datetime.utcnow()
    location_query = request.args.get("location", "").lower()
    keyword_query = request.args.get("keyword", "").lower()
    expires_after = request.args.get("expires_after")

    base_query = FoodPost.query.filter(
        FoodPost.is_claimed == False,
        FoodPost.is_expired == False,
        FoodPost.expiration_date > now,
        FoodPost.latitude.isnot(None),
        FoodPost.longitude.isnot(None)
    )

    if location_query:
        base_query = base_query.filter(FoodPost.location_name.ilike(f"%{location_query}%"))

    if keyword_query:
        base_query = base_query.filter(
            (FoodPost.name.ilike(f"%{keyword_query}%")) |
            (FoodPost.description.ilike(f"%{keyword_query}%"))
        )

    if expires_after:
        try:
            expires_dt = datetime.strptime(expires_after, "%Y-%m-%d")
            base_query = base_query.filter(FoodPost.expiration_date >= expires_dt)
        except ValueError:
            pass  # Ignore invalid date

    food_items = base_query.all()

    result = []
    for item in food_items:
        result.append({
            "id": item.id,
            "name": item.name,
            "quantity": item.quantity,
            "location_name": item.location_name,
            "expiration_date": item.expiration_date.strftime('%Y-%m-%d %H:%M'),
            "description": item.description,
            "latitude": item.latitude,
            "longitude": item.longitude
        })

    return jsonify(result)
