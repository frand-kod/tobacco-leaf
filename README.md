# Tobacco Leaf Prediction

Backend FastAPI + frontend Vue untuk mendeteksi penyakit daun tembakau
(Alternaria Leaf Spot, Cercospora Leaf Spot, Healthy Leaf) dengan model Keras.

## Struktur

```
app/        backend (api/v1 → services → repository → models)
  ml/       model_tembakau.keras + predictor
  uploads/  gambar hasil upload (dibuat otomatis, tidak di-commit)
frontend/   Vue 3 + Vite + Tailwind
create_admin.py   CLI untuk membuat user admin
```

## Menjalankan backend

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp app/.env.example app/.env        # isi SECRET_KEY
uvicorn app.main:app --reload --port 8010
python create_admin.py              # opsional: buat admin
```

Database SQLite (`database.db`) dibuat otomatis. Swagger: `http://localhost:8010/docs`.

Variabel `app/.env`:

| Nama | Default | Keterangan |
| --- | --- | --- |
| `SECRET_KEY` | wajib | kunci JWT |
| `BASE_URL` | `http://localhost:8010` | dipakai untuk membentuk URL gambar |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | origin frontend yang diizinkan (JSON list) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | masa berlaku token |

## Menjalankan frontend

```bash
cd frontend
bun install
bun dev          # http://localhost:5173
```

API base URL diatur di `frontend/src/api.js`.

## Endpoint (prefix `/api/v1`)

Semua endpoint butuh `Authorization: Bearer <token>` kecuali `/auth/*`.

| Method | Path | Akses |
| --- | --- | --- |
| POST | `/auth/register` | publik |
| POST | `/auth/login` | publik |
| POST | `/model/predict` | user (upload gambar, maks 5 MB) |
| GET | `/reports/` | user (riwayat milik sendiri) |
| GET / DELETE | `/reports/{id}` | pemilik |
| GET | `/user/list` | admin |
| POST | `/user/` | admin |
| GET / PUT / DELETE | `/user/{id}` | pemilik akun atau admin (ubah role: admin) |

## Catatan

- Gambar di-resize 224×224 dan disimpan lewat `app/utils/resizer_image.py`.
- Token tidak punya refresh; saat kedaluwarsa frontend diarahkan ke login.
