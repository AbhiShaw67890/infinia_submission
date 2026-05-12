# Case 1: FindIt — Campus Lost & Found Portal

**Live demo:** https://your-render-url.onrender.com <br>
**Repo:** https://findit-xgpm.onrender.com <br>
**Demo video:** unavailabe

---

## What this is

FindIt is a modern campus Lost & Found portal designed to replace cluttered notice boards with a clean, mobile-friendly digital experience. Students can post lost or found items, upload images, search for matches, and securely claim belongings through an approval workflow.

The platform focuses on usability and fast interaction, inspired by social-media-style feeds rather than traditional college portals.

---

## Core Features

* Post LOST / FOUND items with image uploads
* Instagram-style responsive card feed
* Smart item matching using RapidFuzz similarity scoring
* Search and filtering by keyword, category, location, and type
* Claim request workflow with approval/rejection
* User authentication and profile management
* Mobile-first responsive UI
* Cloudinary-based media storage
* PostgreSQL persistence using Neon DB

---

## Demo Credentials

```text
Username: alice
Password: demo1234

Username: bob
Password: demo1234

Username: charlie
Password: demo1234
```

---

## How to run locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/findit.git
cd findit
```

### 2. Create and activate virtual environment

#### Windows (PowerShell)

```powershell
python -m venv winv
.\winv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://your-neon-url

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 5. Apply migrations

```bash
python manage.py migrate --settings=lostfound.settings.development
```

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser --settings=lostfound.settings.development
```

### 7. Seed demo data

```bash
python seed_data.py
```

### 8. Run development server

```bash
python manage.py runserver --settings=lostfound.settings.development
```

### 9. Open browser

```text
http://127.0.0.1:8000
```

---

## Stack

| Layer           | Technology                      | Why it was chosen                                     |
| --------------- | ------------------------------- | ----------------------------------------------------- |
| Backend         | Django 5.2                      | Fast development, built-in auth, clean ORM            |
| Database        | PostgreSQL (Neon)               | Reliable relational database with cloud hosting       |
| Frontend        | Django Templates + Tailwind CSS | Rapid UI development with responsive design           |
| Media Storage   | Cloudinary                      | Simplifies image hosting and deployment               |
| Matching Engine | RapidFuzz                       | Lightweight fuzzy matching for LOST↔FOUND suggestions |
| Authentication  | Django Auth                     | Secure and production-ready auth system               |
| Deployment      | Render                          | Easy free-tier deployment for Django apps             |

---

## Project Structure

```text
findit/
├── .env
├── manage.py
├── requirements.txt
├── Procfile
├── seed_data.py
│
├── lostfound/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
├── items/
├── claims/
├── core/
│
├── templates/
├── static/
└── media/
```

---

## Matching Logic

The matching system suggests possible LOST↔FOUND item pairs using weighted similarity scoring.

Scoring strategy:

* 40% → title similarity
* 30% → description similarity
* 20% → location similarity
* 10% → date proximity

RapidFuzz is used for fuzzy text comparison.

---

## Deployment

The application is deployed using:

* Render → Django hosting
* Neon → PostgreSQL database
* Cloudinary → media storage

### Production Environment Variables

```env
DEBUG=False
DJANGO_SETTINGS_MODULE=lostfound.settings.production
DATABASE_URL=your-neon-url

CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

---

## What's NOT done

* Real-time notifications
* Email verification
* Advanced AI-based image similarity
* WebSocket live updates
* Multi-factor authentication

These were intentionally de-scoped to prioritize a polished MVP within the project time constraints.

---

## In production, I would also add

* Email and push notifications
* Image-based similarity matching
* Item moderation and abuse reporting
* Rate limiting and spam protection
* Activity analytics dashboard
* QR-code based item recovery
* Redis caching for search and feed performance

---

## Key Product Decisions

* Prioritized mobile-first UX because judges are expected to test on phones
* Chose Django templates over React to maximize shipping speed and maintainability
* Used Cloudinary to avoid deployment-related media persistence issues
* Implemented approval-based claim flow to reduce fake ownership claims
* Focused on a clean social-style feed instead of a traditional CRUD interface

---

## Author

Built for the “Campus Lost & Found Portal” full-stack case study challenge.
