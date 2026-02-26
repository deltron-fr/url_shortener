# URL Shortener

A simple URL shortener API with user registration, login, and password reset flows.

## Running the project

1. I used uv to set up the project, installation [steps](https://docs.astral.sh/uv/getting-started/installation/). Inside your repo:

```bash
uv sync
source .venv/bin/activate
```

2. Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## Endpoints

- `POST /urls/shorten/`
  - Body: `{ "original_url": "https://example.com" }`
  - Returns: `original_url`, `short_code`, `short_url`, `created_at`

- `GET /urls/<int:pk>`
  - Returns: `original_url`, `short_code`, `short_url`, `created_at`

- `PUT/PATCH /urls/<int:pk>`
  - Body: fields from `ShortURL` (e.g., `original_url`)
  - Returns: updated `original_url`, `short_code`, `short_url`, `created_at`

- `DELETE /urls/<int:pk>`
  - Returns: `204 No Content`

- `POST /register/`
  - Body: `{ "username": "name", "email": "you@example.com", "password": "...", "plan": "FREE"|"PRO" }`
  - Returns: `id`, `username`, `email`, `plan`

- `POST /login/`
  - Body: `{ "email": "you@example.com", "password": "..." }`
  - Returns: `{ "message": "login successful" }` (session-based login)

- `POST /logout/`
  - Returns: `{ "message": "Logged out successfully" }`

- `POST /forgot-password/`
  - Body: `{ "email": "you@example.com" }`
  - Returns: `200` with a generic message indicating a reset token was sent if the email is registered

- `POST /reset-password/`
  - Body: `{ "email": "you@example.com", "token": "<token>", "new_password": "..." }`
  - Returns: `{ "message": "Password reset successful" }`

- `GET /<short_code>/`
  - Redirects (302) to the original URL
  - Throttled per user plan

- `GET /health/`
  - Returns: `{ "status": "ok" }`

## Notes

- Password reset tokens are emailed to the user and expire after 10 minutes. The mail will be delivered to your running server on your terminal.
