"""unique_series_title_user

Revision ID: 0708a52984d7
Revises: 62d95ec567f8
Create Date: 2023-11-30 18:10:56.059424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0708a52984d7'
down_revision: Union[str, None] = '62d95ec567f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_user_title', 'series', ['user_uuid', 'title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_user_title', 'series', type_='unique')
    # ### end Alembic commands ###
