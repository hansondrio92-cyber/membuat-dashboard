# ============================================================
# models.py
# File ini mendefinisikan "bentuk" tabel di database kita.
# Satu class = satu tabel. Ini yang disebut ORM (Object Relational Mapper):
# kita tulis class Python, SQLAlchemy yang urus SQL-nya.
# ============================================================

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Class User merepresentasikan tabel bernama "users" di database.
# Setiap atribut (id, username, dll) = satu kolom di tabel.
class User(Base):

    # __tablename__ menentukan nama tabel di database
    __tablename__ = "users"

    # Column(Integer, primary_key=True) → kolom angka, ID unik tiap user
    # index=True supaya pencarian berdasarkan ID lebih cepat
    id = Column(Integer, primary_key=True, index=True)

    # Column(String) → kolom teks
    # unique=True → tidak boleh ada username yang sama
    # index=True → pencarian username lebih cepat
    username = Column(String, unique=True, index=True, nullable=False)

    # Email juga harus unik, tidak boleh ada yang sama
    email = Column(String, unique=True, index=True, nullable=False)

    # Password disimpan plain text (teks biasa) untuk tujuan pembelajaran.
    # CATATAN PENTING: Di aplikasi nyata, password HARUS di-hash!
    # Materi hashing akan dibahas di modul Kriptografi nanti.
    password = Column(String, nullable=False)

    # Nama lengkap user, boleh kosong (nullable=True adalah default)
    full_name = Column(String, nullable=True)

    # Nama file foto profil. Kosong kalau belum upload.
    photo = Column(String, nullable=True)

    # Relasi ke kelas yang diikuti user
    enrollments = relationship("Enrollment", back_populates="user", cascade="all, delete-orphan")


# Class Course merepresentasikan kelas e-learning teknik sipil.
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, default="Teknik Sipil")
    description = Column(Text, nullable=True)
    level = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)

    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")


# Class Lesson merepresentasikan materi per pertemuan di dalam kursus.
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=1)

    course = relationship("Course", back_populates="lessons")


# Class Enrollment menyimpan informasi kursus yang dipilih oleh user.
class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"),nullable=False)
    status = Column(String, nullable=False, default="Terdaftar")
    progress = Column(Integer, default=0)

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
