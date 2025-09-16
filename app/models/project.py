from sqlalchemy import Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from ..services.db import Base

class ProjectStatus(enum.Enum):
	review = "review"
	approved = "approved"
	rejected = "rejected"
	funded = "funded"

class Project(Base):
	__tablename__ = "projects"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	title_uk: Mapped[str] = mapped_column(String(255), nullable=False)
	title_de: Mapped[str] = mapped_column(String(255), nullable=False)
	desc_uk: Mapped[str] = mapped_column(Text, default="")
	desc_de: Mapped[str] = mapped_column(Text, default="")
	status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.review)

	author = relationship("User")
	votes = relationship("Vote", back_populates="project", cascade="all, delete-orphan")

class Vote(Base):
	__tablename__ = "votes"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	value: Mapped[int] = mapped_column(Integer, default=0)  # 1 = за, 0 = утрим., -1 = проти

	project = relationship("Project", back_populates="votes")
