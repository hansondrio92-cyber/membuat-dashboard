# ============================================================
# app.py
# Ini adalah file utama aplikasi kita.
# Jalankan: python app.py
# Akses di browser: http://localhost:8000
# ============================================================

import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import koneksi database dan model
from database import engine
import models

# Import router dari masing-masing modul fitur
from routers import auth, profile, dashboard

# ── SETUP APLIKASI ─────────────────────────────────────────
# FastAPI() membuat instance aplikasi web kita
app = FastAPI(title="Sistem Login & Profil", version="1.0.0")

# Pastikan folder uploads ada sebelum aplikasi berjalan
os.makedirs("static/uploads", exist_ok=True)

# Buat semua tabel di database berdasarkan models yang sudah kita definisikan.
# Kalau tabel sudah ada, perintah ini akan diabaikan (tidak hapus data).
# Ini seperti menjalankan CREATE TABLE IF NOT EXISTS di SQL.
models.Base.metadata.create_all(bind=engine)

# Daftarkan folder "static" supaya FastAPI bisa serve file statis
# (CSS, gambar upload, dll) langsung dari folder tersebut.
# http://localhost:8000/static/uploads/foto.jpg → baca file static/uploads/foto.jpg
app.mount("/static", StaticFiles(directory="static"), name="static")

# Gabungkan router auth dan profile ke aplikasi utama.
# Semua endpoint di auth.py dan profile.py akan tersedia di app ini.
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(dashboard.router)


# ── HALAMAN UTAMA ──────────────────────────────────────────
# Kalau user buka http://localhost:8000, redirect ke halaman login
from fastapi.responses import RedirectResponse

@app.get("/")
def root():
    return RedirectResponse(url="/login")


# ── JALANKAN SERVER ────────────────────────────────────────
# Blok ini hanya dijalankan kalau file ini dieksekusi langsung
# (bukan diimport dari file lain)
if __name__ == "__main__":
    print("=" * 50)
    print("  Server berjalan di: http://localhost:8000")
    print("  Tekan CTRL+C untuk berhenti")
    print("=" * 50)

    # uvicorn.run() menjalankan server web
    # "app:app" → file app.py, variabel bernama app
    # host="0.0.0.0" → bisa diakses dari jaringan lokal
    # port=8000 → nomor port
    # reload=True → otomatis restart kalau kode berubah (berguna saat development)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)