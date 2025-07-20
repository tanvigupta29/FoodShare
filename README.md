
# Food Share Platform

## Overview

The Food Share Platform is a community-driven web application that connects donors with recipients to reduce food waste and address hunger. It enables individuals, restaurants, caterers, and organizations to donate surplus food, while allowing those in need to view, claim, and receive food efficiently and safely.

## Objectives

* Reduce food wastage in communities.
* Provide surplus food to individuals or families in need.
* Encourage local collaboration between donors and recipients.
* Ensure transparency, traceability, and accountability in food distribution.

## User Roles

* **Donor** – Posts food items available for donation.
* **Recipient** – Views and claims available food items.
* **Admin/Moderator (optional)** – Oversees activity, resolves disputes, and ensures compliance.

## Features

### Authentication & User Management

* Secure registration and login with session-based authentication.
* Users choose a role (Donor or Recipient) during registration.
* Access control ensures only logged-in users can post or claim food.

### Food Posting & Discovery

* Donors post food by entering description, quantity, category, pickup time, expiry date, and optionally upload an image.
* Pickup location is pinned using a map interface.
* Recipients can filter and view food near them in real time.

### Map Integration

* Leaflet.js map for interactive location pinning.
* Donors tag food location during posting.
* Recipients view available food on the map and can click to see details and claim.

### Claim Management

* Recipients claim food with quantity limits (if set).
* Donors can track claimed vs unclaimed items and manage claim requests.
* Recipients have a dashboard for tracking their claimed items.

### Notifications & Updates

* Donors are notified when their food is claimed.
* Recipients receive updates for new food posts and upcoming expiry.
* Dashboards reflect real-time food and claim statuses.

### Dashboards

* **Donor Dashboard**: Manage posted food, track claims.
* **Recipient Dashboard**: View available and claimed items.


## Smart Features (Optional / Future Enhancements)

* AI-powered expiry prediction using image and text input.
* Fraud detection using anomaly detection algorithms.
* Gamification with reward badges for frequent donors and recipients.
* SMS notifications using Twilio when new food is posted nearby.
* Voice command integration for ease of access.

## Tech Stack

* **Frontend**: HTML, CSS, JavaScript, Leaflet.js
* **Backend**: Python (Flask)
* **Database**: SQLite or PostgreSQL
* **Authentication**: Flask-Login (Session-based)
* **Maps/Geolocation**: Leaflet.js, geopy
* **Optional**: TensorFlow/Keras for AI features, Twilio for SMS alerts

## Security & Privacy

* Input validation to prevent XSS and CSRF attacks.
* Role-based access control for actions and views.
* Geolocation data is securely handled and only shown to authorized users.

## Impact

This platform provides a scalable and practical solution to food insecurity while addressing food wastage. It empowers local communities to engage in circular food sharing, ensuring surplus food reaches those in need through a secure, tech-driven, and human-centric platform.

