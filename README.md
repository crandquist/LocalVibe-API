[![GCP Deploy](https://img.shields.io/badge/Deployed-Google%20Cloud-blue)](https://assignment-2-spring25.uc.r.appspot.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Built%20with-Python-blue)](https://www.python.org/)

# LocalVibe API

A cloud-native RESTful API for managing businesses, owners, and user reviews.  
Built with Flask, deployed on Google App Engine, and powered by Google Cloud Datastore.

---

## 🚀 Live Deployment

You can access the live API here:

> [https://assignment-2-spring25.uw.r.appspot.com/](https://assignment-2-spring25.uw.r.appspot.com/)

---

## 📚 API Overview

**Business Routes:**

- `POST /businesses` — Create a business
- `GET /businesses` — List all businesses
- `GET /businesses/:business_id` — Retrieve a business
- `PUT /businesses/:business_id` — Update a business
- `DELETE /businesses/:business_id` — Delete a business and associated reviews
- `GET /owners/:owner_id/businesses` — List all businesses by an owner

**Review Routes:**

- `POST /reviews` — Submit a review for a business
- `GET /reviews/:review_id` — Retrieve a review
- `PUT /reviews/:review_id` — Edit a review
- `DELETE /reviews/:review_id` — Delete a review
- `GET /users/:user_id/reviews` — List all reviews by a user

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask
- **Database**: Google Cloud Datastore (Firestore in Datastore mode)
- **Deployment**: Google App Engine (Standard Environment)
- **Testing**: Postman + Newman (Full API Test Suite)

---

## 🧪 Local Development Setup

To run this project locally:

1. Clone this repository:

```bash
git clone https://github.com/crandquist/LocalVibe-API
cd localvibe-api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set your Google Cloud credentials (for local Datastore access)

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-keyfile.json"
```

5. Run the app:

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8080/`

---

## 📦 Deployment Instructions

To deploy to Google Cloud Platform:

```bash
gcloud app deploy
```

(Requires Google Cloud SDK and authenticated account.)

---

## 📜 License

This project is released under the MIT License.

---

## 📫 Contact

Created by Cat Randquist —
Feel free to connect with me on LinkedIn or check out my portfolio at catrandquist.com.