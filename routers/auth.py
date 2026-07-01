# ============================================================
# routers/auth.py
# Router adalah cara FastAPI memisahkan "kelompok" endpoint.
# File ini khusus menangani autentikasi: register dan login.
# ============================================================

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import User

# APIRouter() membuat "sub-router" yang nanti digabungkan di app.py
router = APIRouter()

# Jinja2Templates memberitahu FastAPI di mana folder template HTML kita
templates = Jinja2Templates(directory="templates")

# ── REGISTER ──────────────────────────────────────────────
# @router.get → endpoint yang merespons HTTP GET (buka halaman)
# response_class=HTMLResponse → kita kembalikan HTML, bukan JSON
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    # Tampilkan halaman register
    return templates.TemplateResponse(request, "register.html", {})

# @router.post → endpoint yang merespons HTTP POST (kirim form)
@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),    # Form(...) artinya ambil data dari form HTML
    email: str = Form(...),        # tanda ... artinya field ini WAJIB diisi
    password: str = Form(...),
    full_name: str = Form(""),     # tanda "" artinya boleh kosong
    db: Session = Depends(get_db) # Depends(get_db) → minta sesi database otomatis
):
    # Cek apakah username sudah terdaftar
    # db.query(User) → mulai query ke tabel users
    # .filter(...) → tambah kondisi WHERE
    # .first() → ambil satu hasil pertama, atau None kalau tidak ada
    existing_user = db.query(User).filter(User.username == username).first()

    if existing_user:
        # Kalau sudah ada, tampilkan halaman register lagi dengan pesan error
        return templates.TemplateResponse(request, "register.html", {
            "error": "Username sudah digunakan!"
        })

    # Buat objek User baru (belum disimpan ke database)
    new_user = User(
        username=username,
        email=email,
        password=password,  # plain text — ingat: ini hanya untuk pembelajaran!
        full_name=full_name
    )

    # db.add() → tambahkan objek ke sesi (antrian penyimpanan)
    db.add(new_user)
    # db.commit() → simpan semua perubahan ke database
    db.commit()

    # Redirect ke halaman login setelah berhasil daftar
    return RedirectResponse(url="/login?success=1", status_code=303)


# ── LOGIN ──────────────────────────────────────────────────
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, success: int = 0):
    return templates.TemplateResponse(request, "login.html", {
        "success": success
    })


@router.post("/login")
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Cari user berdasarkan username DAN password
    user = db.query(User).filter(
        User.username == username,
        User.password == password  # perbandingan langsung (plain text)
    ).first()

    if not user:
        return templates.TemplateResponse(request, "login.html", {
            "error": "Username atau password salah!"
        })

    # Login berhasil → redirect ke halaman dashboard seleksi
    return RedirectResponse(url=f"/dashboard/{user.id}", status_code=303)


# ── LOGOUT ────────────────────────────────────────────────
@router.get("/logout")
def logout():
    return RedirectResponse(url="/login", status_code=303)