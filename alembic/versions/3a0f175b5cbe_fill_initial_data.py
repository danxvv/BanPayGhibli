"""fill_initial_data

Revision ID: 3a0f175b5cbe
Revises: c6a93183189c
Create Date: 2024-06-05 20:58:53.816243

"""
import datetime
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select
from src.utils.security import get_password_hash
from src.users.models import Role, User


# revision identifiers, used by Alembic.
revision = '3a0f175b5cbe'
down_revision = 'c6a93183189c'
branch_labels = None
depends_on = None


def upgrade():

    roles = [
        {"name": "admin"},
        {"name": "films"},
        {"name": "people"},
        {"name": "locations"},
        {"name": "species"},
        {"name": "vehicles"},
    ]
    op.bulk_insert(Role.__table__, roles)

    conn = op.get_bind()
    role_ids = {}
    for role in roles:
        role_id = conn.execute(select(Role).where(Role.name == role["name"])).scalar_one()
        role_ids[role["name"]] = role_id

    """
    class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    """

    users_table = table('users',
                        column('id', sa.String),
                        column('name', sa.String),
                        column('email', sa.String),
                        column('password', sa.String),
                        column('created_at', sa.DateTime),
                        column('updated_at', sa.DateTime),
                        column('role_id', sa.Integer)
                        )


    users = [
        {
            "id": str(uuid.uuid4()),  # Ensure UUIDs are strings
            "name": "Films User",
            "email": "user_films@example.com",
            "password": get_password_hash("password123"),
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow(),
            "role_id": role_ids["films"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "People User",
            "email": "user_people@example.com",
            "password": get_password_hash("password123"),
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow(),
            "role_id": role_ids["people"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Locations User",
            "email": "user_locations@example.com",
            "password": get_password_hash("password123"),
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow(),
            "role_id": role_ids["locations"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Species User",
            "email": "user_species@example.com",
            "password": get_password_hash("password123"),
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow(),
            "role_id": role_ids["species"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Vehicles User",
            "email": "user_vehicles@example.com",
            "password": get_password_hash("password123"),
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow(),
            "role_id": role_ids["vehicles"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Admin User",            "email": "user_admin@example.com",
            "password": get_password_hash("password123"),
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow(),
            "role_id": role_ids["admin"]
        }
    ]

    op.bulk_insert(users_table, users)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        'DELETE FROM users WHERE email IN (\'user_films@example.com\', \'user_people@example.com\', \'user_locations@example.com\', \'user_species@example.com\', \'user_vehicles@example.com\', \'user_admin@example.com\')')
    op.execute(
        'DELETE FROM roles WHERE name IN (\'admin\', \'films\', \'people\', \'locations\', \'species\', \'vehicles\')')
    # ### end Alembic commands ###
