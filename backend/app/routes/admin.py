from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import DeliveryPartner
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint("admin", __name__, template_folder="../templates")

@admin_bp.route("/add-partner", methods=["GET", "POST"])
def add_partner():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")

        # ✅ Check for existing email (prevent duplicates)
        existing = DeliveryPartner.query.filter_by(email=email).first()
        if existing:
            flash("A delivery partner with this email already exists.", "danger")
            return redirect(url_for("admin.add_partner"))

        new_partner = DeliveryPartner(name=name, email=email, phone=phone)
        try:
            db.session.add(new_partner)
            db.session.commit()
            flash("Delivery Partner added successfully!", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Error: Email must be unique.", "danger")

        return redirect(url_for("admin.add_partner"))

    # Show list of current delivery partners (Optional)
    partners = DeliveryPartner.query.order_by(DeliveryPartner.name).all()
    return render_template("add_partner.html", partners=partners)

@admin_bp.route("/assign-partner", methods=["GET", "POST"])
def assign_partner():
    from app.models import Claim, DeliveryPartner

    claims = Claim.query.filter_by(status="confirmed").all()
    partners = DeliveryPartner.query.all()

    if request.method == "POST":
        claim_id = request.form["claim_id"]
        partner_id = request.form["partner_id"]

        claim = Claim.query.get(claim_id)
        partner = DeliveryPartner.query.get(partner_id)

        if claim and partner:
            claim.delivery_partner = partner
            db.session.commit()
            flash("Delivery partner assigned successfully!", "success")
        else:
            flash("Invalid claim or partner selected.", "danger")

        return redirect(url_for("admin.assign_partner"))

    return render_template("assign_partner.html", claims=claims, partners=partners)
