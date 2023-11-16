"""empty message

Revision ID: b8a5c13cf561
Revises: 52920e2bed61
Create Date: 2023-11-13 19:29:15.897494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8a5c13cf561'
down_revision = '52920e2bed61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admin')
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(timezone=True), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_column('date')

    op.create_table('admin',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('admin_key', sa.VARCHAR(length=150), nullable=True),
    sa.Column('password', sa.VARCHAR(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
