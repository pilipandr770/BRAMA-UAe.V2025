from sqlalchemy import Integer, String, LargeBinary, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..services.db import Base

class ContentBlock(Base):
	"""
	Типи: 'info', 'gallery', 'projects'
	Для інфоблоку використовуємо title/body (укр/нім).
	Для 'gallery' є дочірні GalleryImage.
	"""
	__tablename__ = "content_blocks"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	block_type: Mapped[str] = mapped_column(String(32), nullable=False)  # info/gallery/projects
	title_uk: Mapped[str] = mapped_column(String(255), default="")
	title_de: Mapped[str] = mapped_column(String(255), default="")
	body_uk: Mapped[str] = mapped_column(Text, default="")
	body_de: Mapped[str] = mapped_column(Text, default="")

	images = relationship("GalleryImage", back_populates="block", cascade="all, delete-orphan")

class GalleryImage(Base):
	__tablename__ = "gallery_images"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	block_id: Mapped[int] = mapped_column(ForeignKey("content_blocks.id"), nullable=False)
	image_bytes: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
	caption_uk: Mapped[str] = mapped_column(String(255), default="")
	caption_de: Mapped[str] = mapped_column(String(255), default="")
	block = relationship("ContentBlock", back_populates="images")
