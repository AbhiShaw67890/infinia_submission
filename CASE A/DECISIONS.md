# DECISIONS.md — Architecture & Design Decisions

## Why Django over Flask?
Django ships with ORM, auth, admin, forms, CSRF — everything we need out of the box.
Flask would require many third-party packages and more boilerplate for the same result.

## Why Neon PostgreSQL?
- Free tier with 0.5GB storage, perfect for MVP
- Serverless — no cold-start issues for web connections
- Compatible with Render deployment and standard psycopg2

## Why Cloudinary?
- Free tier (25 credits/month) handles image upload, storage, CDN
- django-cloudinary-storage integrates cleanly as DEFAULT_FILE_STORAGE
- Images served via Cloudinary CDN — fast globally

## Why AbstractUser over AbstractBaseUser?
AbstractUser extends the default Django user with all fields (username, email, etc.).
AbstractBaseUser would require reimplementing everything from scratch.
Since we only needed to add avatar + college + phone + bio, AbstractUser was perfect.

## Why function-based views over class-based views?
FBVs are more readable and explicit for beginners.
The views are not complex enough to benefit from CBV mixins.
Django docs themselves recommend FBVs for simple cases.

## Why RapidFuzz over difflib?
RapidFuzz is significantly faster (C extension) and handles partial matches better.
difflib is pure Python and has worse fuzzy matching quality.
For a campus app where users might misspell or use partial names, RapidFuzz is superior.

## Why Tailwind CDN instead of compiled Tailwind?
For MVP speed — no Node.js build step needed.
CDN version supports all Tailwind utilities including arbitrary values.
Can be switched to compiled Tailwind later for production performance.

## Why split settings (base/dev/prod)?
- Prevents accidental use of production credentials locally
- Clean separation of concerns
- Industry standard Django pattern

## Matching Score Weights (40/30/20/10)
- Title (40%): Most important — a wallet is a wallet regardless of colour
- Description (30%): Contains identifying details
- Location (20%): Items lost near same place likely related
- Date (10%): Same day/week strengthens match but not critical

## Claim uniqueness constraint
`unique_together = [('item', 'claimant')]` prevents spam claiming.
A user can only claim the same item once.

## Item auto-resolution on claim approval
When a claim is approved:
1. The claim status → APPROVED
2. All other pending claims for that item → REJECTED
3. Item status → RESOLVED
This prevents multiple approvals and keeps the feed clean.
