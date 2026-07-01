# ============================================================
# routers/dashboard.py
# Router untuk halaman dashboard e-learning setelah login.
# Menampilkan kelas, materi, dan pilihan kursus.
# ============================================================

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import User, Course, Lesson, Enrollment

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def seed_courses(db: Session):
    if db.query(Course).count() > 0:
        return

    course1 = Course(
        title="Teknik Struktur Beton",
        category="Teknik Sipil",
        description="Pelajari dasar-dasar struktur beton, elemen struktural, dan analisis beban.",
        level="Dasar"
    )
    course1.lessons = [
        Lesson(title="Pengantar Beton", description="Dasar teori beton dan komponennya.", content="Materi pengantar beton...", order=1),
        Lesson(title="Sifat Material", description="Kekuatan, modulus, dan perilaku beton.", content="Materi sifat material...", order=2),
        Lesson(title="Rancang Balok dan Kolom", description="Langkah-langkah desain elemen beton.", content="Materi rancang balok dan kolom...", order=3)
    ]

    course2 = Course(
        title="Manajemen Proyek Konstruksi",
        category="Teknik Sipil",
        description="Pelajari perencanaan proyek, kontrol biaya, dan manajemen lapangan.",
        level="Menengah"
    )
    course2.lessons = [
        Lesson(title="Perencanaan Proyek", description="Tahapan perencanaan dan penjadwalan.", content="Materi perencanaan proyek...", order=1),
        Lesson(title="Pengendalian Biaya", description="Strategi kontrol anggaran kontruksi.", content="Materi pengendalian biaya...", order=2),
        Lesson(title="Manajemen Risiko", description="Mengenali dan mengelola risiko proyek.", content="Materi manajemen risiko...", order=3)
    ]

    db.add_all([course1, course2])
    db.commit()


@router.get("/dashboard/{user_id}", response_class=HTMLResponse)
def dashboard_page(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    seed_courses(db)
    courses = db.query(Course).all()
    enrolled_course_ids = {enrollment.course_id for enrollment in user.enrollments}

    return templates.TemplateResponse(request, "dashboard.html", {
        "user": user,
        "courses": courses,
        "enrolled_ids": enrolled_course_ids
    })


@router.get("/course/{course_id}/{user_id}", response_class=HTMLResponse)
def course_detail(course_id: int, user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    if not user or not course:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")

    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()

    return templates.TemplateResponse(request, "course_detail.html", {
        "user": user,
        "course": course,
        "enrollment": enrollment
    })


@router.post("/course/{course_id}/{user_id}/enroll")
def enroll_course(course_id: int, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    if not user or not course:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")

    existing = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()

    if not existing:
        enrollment = Enrollment(user_id=user_id, course_id=course_id, status="Terdaftar", progress=0)
        db.add(enrollment)
        db.commit()

    return RedirectResponse(url=f"/course/{course_id}/{user_id}", status_code=303)
