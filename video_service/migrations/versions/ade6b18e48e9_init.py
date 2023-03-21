"""init

Revision ID: ade6b18e48e9
Revises: 
Create Date: 2023-03-21 08:12:24.555562

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ade6b18e48e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('videos',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('video_url', sa.String(length=2048), nullable=True),
    sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('text', sa.String(length=256), nullable=True),
    sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('video_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment_reactions',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('comment_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('reaction_type', sa.Enum('LIKE', 'DISLIKE', name='reactiontype'), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_reactions')
    op.drop_table('comments')
    op.drop_table('videos')
    op.drop_table('categories')
    # ### end Alembic commands ###