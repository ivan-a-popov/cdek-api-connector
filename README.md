# CDEK API connector

FastAPI service that creates CDEK deliveries from orders stored in PostgreSQL, talks to RetailCRM, and uploads barcode PDFs to Yandex Disk.

Copy `.env.example` to `.env` and replace the placeholders before running. `.env` is gitignored and must not be committed.

```bash
cp .env.example .env
```

## Environment variables

| Variable | Default | Replace before use |
|---|---|---|
| `DATABASE_IP` | `127.0.0.1` | PostgreSQL host |
| `DATABASE_USER` | `app_user` | PostgreSQL user |
| `DATABASE_PSWD` | `changeme` | PostgreSQL password |
| `DATABASE_NAME` | `app_db` | PostgreSQL database name |
| `CDEK_URL` | `https://api.edu.cdek.ru/v2` | CDEK API base URL. Keep the default for the public sandbox. Use `https://api.cdek.ru/v2` in production |
| `CDEK_ID` | CDEK public sandbox account | Your CDEK account (client id). The default is CDEK’s documented demo account and is safe only against `api.edu.cdek.ru` |
| `CDEK_SECRET` | CDEK public sandbox secret | Your CDEK secret. Same sandbox caveat as `CDEK_ID` |
| `CRM_API` | `YOUR_CRM_API_KEY` | RetailCRM API key. Required |
| `CRM_URL` | `https://example.retailcrm.ru/api/v5` | RetailCRM API base, e.g. `https://your-shop.retailcrm.ru/api/v5` |
| `YADISK_TOKEN` | `YOUR_YADISK_TOKEN` | Yandex Disk OAuth token used to store barcode PDFs. Required if print-form upload is enabled |

`CDEK_ID` / `CDEK_SECRET` defaults are the official CDEK sandbox credentials from their API docs. They are not production keys. Set your own pair before pointing `CDEK_URL` at `https://api.cdek.ru/v2`.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Docker:

```bash
docker build -t cdek-api-connector .
docker run --env-file .env -p 8000:8000 cdek-api-connector
```
