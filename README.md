# QR Service
FastAPI microservice for QR code generation using amzqr.

## Endpoints
- `GET /health` — health check
- `GET /qr?url=https://example.com` — generate QR code (PNG)
  - `colorized` (bool) — colorful QR
  - `contrast` (float) — contrast adjustment
  - `brightness` (float) — brightness adjustment
  - `picture` (URL) — background image
