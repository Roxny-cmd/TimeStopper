from datetime import datetime, date

from sqlalchemy import (String, Integer, Boolean, DateTime, Date, ForeignKey, Text, UniqueConstraint)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )
    password_hash: Mapped[str] = mapped_column(String(400))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

class TrackedApp(Base):
    __tablename__ = "tracked_apps"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    app_identifier: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(255))
    daily_limit_minutes: Mapped[int] = mapped_column(Integer)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    sessions = relationship(
        "UsageSession",
        back_populates="tracked_app"
    )

    __table_args__ = (
    UniqueConstraint(
        "user_id",
        "app_identifier",
        name="unique_user_app"
        ),
    )

class UsageSession(Base):
    __tablename__ = "usage_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    tracked_app_id: Mapped[int] = mapped_column(
        ForeignKey("tracked_apps.id")
    )
    started_at: Mapped[datetime] = mapped_column(DateTime)
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)

    tracked_app = relationship(
        "TrackedApp",
        back_populates="sessions"
    )

class DailyUsage(Base):
    __tablename__ = "daily_usage"

    id: Mapped[int] = mapped_column(primary_key=True)
    tracked_app_id: Mapped[int] = mapped_column(
        ForeignKey("tracked_apps.id")
    )
    date: Mapped[date] = mapped_column(Date)
    total_seconds: Mapped[int] = mapped_column(Integer, default=0)

class Reward(Base):
    __tablename__ = "rewards"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    price: Mapped[int] = mapped_column(Integer)

class PointTransaction(Base):
    __tablename__ = "point_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    amount: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    date_key: Mapped[str] = mapped_column(String(10))

class DailyResult(Base):
    __tablename__ = "daily_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    tracked_app_id: Mapped[int] = mapped_column(
        ForeignKey("tracked_apps.id")
    )
    date: Mapped[date] = mapped_column(Date)
    result: Mapped[str] = mapped_column(String(50))
    processed: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "tracked_app_id",
            "date",
            name="unique_daily_result"
        ),
    )

class UserReward(Base):
    __tablename__ = "user_rewards"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    reward_id: Mapped[int] = mapped_column(
        ForeignKey("rewards.id")
    )
    purchased_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    points_spent: Mapped[int] = mapped_column(Integer)