# Tobacco Leaf Prediction

Aplikasi web untuk mendeteksi penyakit daun tembakau dari foto. Model Keras mengenali tiga kelas:
**Alternaria Leaf Spot**, **Cercospora Leaf Spot**, dan **Healthy Leaf**.

- **Backend**: FastAPI + SQLite (folder `app/`)
- **Frontend**: Vue 3 + Vite + Tailwind (folder `frontend/`)

---

## Daftar isi

1. [Yang perlu diinstal](#1-yang-perlu-diinstal)
2. [Mengambil kode](#2-mengambil-kode)
3. [Menjalankan backend](#3-menjalankan-backend)
4. [Menjalankan frontend](#4-menjalankan-frontend)
5. [Memakai aplikasi](#5-memakai-aplikasi)
6. [Masalah umum](#6-masalah-umum)
7. [Referensi](#7-referensi)

---

## 1. Yang perlu diinstal

Anda butuh tiga program. Pasang sekali saja.

| Program | Versi | Fungsi |
| --- | --- | --- |
| Python | **3.11, 3.12, atau 3.13** (jangan 3.14, TensorFlow belum mendukung) | menjalankan backend |
| Node.js | **20.19 ke atas** (pilih versi LTS) | menjalankan frontend |
| Git | terbaru | mengunduh kode (opsional, lihat langkah 2) |

Ruang disk: sekitar **2 GB** (TensorFlow besar). Koneksi internet dibutuhkan saat instalasi.

### Windows

1. **Python**: unduh dari <https://www.python.org/downloads/windows/>.
   Saat installer terbuka, **centang "Add python.exe to PATH"** di bawah jendela, lalu klik *Install Now*.
2. **Node.js**: unduh versi **LTS** dari <https://nodejs.org/> dan instal dengan semua pilihan bawaan.
3. **Git** (opsional): unduh dari <https://git-scm.com/download/win> dan instal dengan pilihan bawaan.
4. **Tutup semua jendela terminal lalu buka lagi** supaya PATH terbaca. Buka **PowerShell** (cari "PowerShell" di menu Start).
5. Cek instalasi:
   ```powershell
   python --version
   node --version
   npm --version
   ```
   Ketiganya harus menampilkan nomor versi. Kalau `python` tidak dikenali, coba `py --version`, dan pakai `py` sebagai pengganti `python` di semua perintah di bawah.

### Linux

**Ubuntu / Debian / Linux Mint**
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl
# Node.js 22 LTS (versi di apt biasanya terlalu lama):
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
```

**Fedora**
```bash
sudo dnf install -y python3 python3-pip git nodejs npm
```

**Arch / Manjaro**
```bash
sudo pacman -S python python-pip git nodejs npm
```

Cek instalasi:
```bash
python3 --version
node --version
npm --version
```
Kalau `python3 --version` menunjukkan 3.14, pasang Python 3.13 (misalnya lewat `uv` atau `pyenv`), karena TensorFlow belum mendukung 3.14.

---

## 2. Mengambil kode

**Dengan Git:**
```bash
git clone https://github.com/frand-kod/tobacco-leaf.git
cd tobacco-leaf
```

**Tanpa Git:** buka <https://github.com/frand-kod/tobacco-leaf>, klik **Code → Download ZIP**, ekstrak, lalu buka terminal di dalam folder hasil ekstrak.

Semua perintah di bawah dijalankan dari folder `tobacco-leaf` ini, kecuali disebut lain.

---

## 3. Menjalankan backend

Pakai **terminal pertama**. Biarkan tetap terbuka selama aplikasi dipakai.

### 3.1 Buat lingkungan virtual Python

Langkah ini membuat folder `venv` supaya paket Python tidak bercampur dengan sistem Anda.

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
Kalau muncul error *"running scripts is disabled on this system"*, jalankan sekali:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
lalu ulangi perintah `Activate.ps1`. (Pengguna Command Prompt `cmd`: pakai `venv\Scripts\activate.bat`.)

**Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

Berhasil kalau awal baris terminal berubah menjadi `(venv)`.

### 3.2 Instal paket Python

```bash
pip install -r requirements.txt
```
Proses ini **memakan waktu beberapa menit** dan mengunduh ratusan MB (TensorFlow). Tunggu sampai selesai tanpa error.

### 3.3 Buat file konfigurasi `.env`

File `app/.env` menyimpan kunci rahasia. File ini **tidak ikut di repo**, jadi Anda harus membuatnya.

**Windows (PowerShell)**
```powershell
Copy-Item app\.env.example app\.env
python -c "import secrets; print(secrets.token_hex(32))"
```

**Linux**
```bash
cp app/.env.example app/.env
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Perintah `python -c ...` mencetak teks acak panjang. Buka `app/.env` dengan editor teks (Notepad, nano, dll.), lalu ganti `change-me` pada baris `SECRET_KEY=` dengan teks tadi. Contoh hasil akhirnya:
```env
SECRET_KEY=9f2c...teks-acak-panjang...
BASE_URL=http://localhost:8010
```

| Variabel | Default | Keterangan |
| --- | --- | --- |
| `SECRET_KEY` | wajib | kunci penanda tangan token login |
| `BASE_URL` | `http://localhost:8010` | alamat backend, dipakai membentuk URL gambar |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | alamat frontend yang diizinkan (format JSON list) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | lama token login berlaku |

### 3.4 Jalankan server

```bash
uvicorn app.main:app --reload --port 8010
```
Berhasil kalau muncul `Application startup complete`. Buka <http://localhost:8010/docs> untuk melihat dokumentasi API (Swagger).

Saat pertama dijalankan, file database `database.db` dan folder `app/uploads` dibuat otomatis.

### 3.5 (Opsional) Buat akun admin

Pendaftaran lewat web hanya membuat akun biasa. Untuk akun admin, buka **terminal baru** di folder yang sama, aktifkan `venv` lagi (langkah 3.1, bagian aktivasi saja), lalu:
```bash
python create_admin.py
```
Isi nama, email, dan password sesuai petunjuk. Akun admin bisa membuka menu **User Management**.

---

## 4. Menjalankan frontend

Pakai **terminal kedua** (backend tetap berjalan di terminal pertama).

```bash
cd frontend
npm install
npm run dev
```
`npm install` cukup dijalankan sekali. Setelah muncul `Local: http://localhost:5173/`, buka alamat itu di browser.

> Pengguna [Bun](https://bun.sh) bisa memakai `bun install` dan `bun dev` sebagai pengganti.

**Penting:** backend harus berjalan di port **8010** dan frontend di port **5173**. Alamat backend ditulis di `frontend/src/api.js`, dan alamat frontend ditulis di `CORS_ORIGINS` pada `app/.env`.

---

## 5. Memakai aplikasi

1. Buka <http://localhost:5173>, klik daftar, lalu buat akun.
2. Masuk (login).
3. Di dashboard, unggah foto daun tembakau (JPG/PNG, maksimal 5 MB). Hasil prediksi dan tingkat keyakinannya muncul, lalu tersimpan di tabel riwayat.
4. Hapus riwayat lewat ikon tempat sampah. Gambarnya ikut terhapus.
5. Menu **Profile** untuk mengubah data akun atau menghapus akun (semua riwayat ikut terhapus).

### Menjalankan lagi di hari berikutnya

Instalasi tidak perlu diulang. Cukup:

```bash
# terminal 1, dari folder tobacco-leaf
venv\Scripts\Activate.ps1          # Windows
source venv/bin/activate           # Linux
uvicorn app.main:app --reload --port 8010

# terminal 2
cd frontend
npm run dev
```

---

## 6. Masalah umum

| Gejala | Penyebab dan solusi |
| --- | --- |
| `python` / `pip` tidak dikenali (Windows) | PATH belum diatur. Instal ulang Python dengan centang *Add to PATH*, atau pakai `py`. Tutup dan buka lagi terminal. |
| `No matching distribution found for tensorflow` | Versi Python tidak cocok (kemungkinan 3.14, atau Python 32-bit). Pakai Python 3.11–3.13 64-bit. |
| `ensurepip is not available` / `venv` gagal (Linux) | Jalankan `sudo apt install python3-venv`. |
| `Activate.ps1 cannot be loaded` | Jalankan `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` sekali. |
| `ValidationError ... SECRET_KEY field required` | `app/.env` belum dibuat atau `SECRET_KEY` kosong. Ulangi langkah 3.3. |
| Backend gagal start dengan error saat memuat model | File `app/ml/model_tembakau.keras` hilang atau rusak. Unduh ulang repo secara utuh. |
| Login atau upload gagal, konsol browser menulis `CORS` | Frontend tidak berjalan di port 5173. Tambahkan alamat yang dipakai ke `CORS_ORIGINS` di `app/.env`, lalu restart backend. |
| `Network Error` di frontend | Backend belum jalan, atau tidak di port 8010. |
| Gambar riwayat tidak tampil | `BASE_URL` di `app/.env` tidak sesuai alamat backend. |
| Tiba-tiba kembali ke halaman login | Token berlaku 15 menit. Login lagi, atau naikkan `ACCESS_TOKEN_EXPIRE_MINUTES`. |
| `npm install` gagal karena versi Node | Node terlalu lama. Pasang Node.js 20.19 atau lebih baru. |
| Port 8010 atau 5173 sudah terpakai | Tutup program yang memakainya, atau ganti port (lalu sesuaikan `frontend/src/api.js` dan `CORS_ORIGINS`). |

---

## 7. Referensi

### Struktur proyek

```
app/                backend
  api/v1/           route (auth, user, prediction, report)
  services/         logika bisnis
  repository/       akses database
  models/ schemas/  tabel SQLAlchemy dan skema Pydantic
  ml/               model_tembakau.keras dan predictor
  uploads/          gambar upload (dibuat otomatis, tidak di-commit)
frontend/           Vue 3 + Vite + Tailwind
create_admin.py     CLI pembuat akun admin
requirements.txt    dependency Python
```

### Endpoint (prefix `/api/v1`)

Semua endpoint butuh header `Authorization: Bearer <token>` kecuali `/auth/*`.

| Method | Path | Akses |
| --- | --- | --- |
| POST | `/auth/register` | publik |
| POST | `/auth/login` | publik |
| POST | `/model/predict` | user (unggah gambar, maks 5 MB) |
| GET | `/reports/` | user (riwayat milik sendiri) |
| GET / DELETE | `/reports/{id}` | pemilik |
| GET | `/user/list` | admin |
| POST | `/user/` | admin |
| GET / PUT / DELETE | `/user/{id}` | pemilik akun atau admin (mengubah role: hanya admin) |

### Catatan teknis

- Gambar di-resize ke 224×224 dan disimpan lewat `app/utils/resizer_image.py`.
- Token tidak punya refresh. Saat kedaluwarsa, frontend diarahkan ke halaman login.
- Database memakai SQLite (`database.db` di folder tempat `uvicorn` dijalankan), jadi selalu jalankan backend dari folder `tobacco-leaf`.
