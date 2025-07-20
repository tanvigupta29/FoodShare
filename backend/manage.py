from flask.cli import FlaskGroup
import os

from app import create_app, db
from app.models import User, FoodPost, Claim, Notification  # Register models for migrations

app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    app.run(debug=True)

