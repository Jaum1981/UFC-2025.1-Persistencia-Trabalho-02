"""initial schema

Revision ID: 33f51347be1b
Revises: 
Create Date: 2025-06-11 02:36:49.972766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33f51347be1b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'director',
        sa.Column('director_id', sa.Integer(), primary_key=True),
        sa.Column('director_name', sa.String(), nullable=False),
        sa.Column('nationality', sa.String(), nullable=False),
        sa.Column('birth_date', sa.String(), nullable=False),
        sa.Column('biography', sa.String(), nullable=False),
        sa.Column('website', sa.String(), nullable=False),
    )
    op.create_table(
        'movie',
        sa.Column('movie_id', sa.Integer(), primary_key=True),
        sa.Column('movie_title', sa.String(), nullable=False),
        sa.Column('genre', sa.String(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('rating', sa.String(), nullable=False),
        sa.Column('synopsis', sa.String(), nullable=False),
    )
    op.create_table(
        'movie_director_link',
        sa.Column('movie_id', sa.Integer(), sa.ForeignKey('movie.movie_id'), primary_key=True),
        sa.Column('director_id', sa.Integer(), sa.ForeignKey('director.director_id'), primary_key=True),
    )
    op.create_table(
        'room',
        sa.Column('room_id', sa.Integer(), primary_key=True),
        sa.Column('room_name', sa.String(), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('screen_type', sa.String(), nullable=False),
        sa.Column('audio_system', sa.String(), nullable=False),
        sa.Column('acessibility', sa.Boolean(), nullable=False),
    )
    op.create_table(
        'session',
        sa.Column('session_id', sa.Integer(), primary_key=True),
        sa.Column('date_time', sa.DateTime(), nullable=False),
        sa.Column('exibition_type', sa.String(), nullable=False),
        sa.Column('language_audio', sa.String(), nullable=False),
        sa.Column('language_subtitles', sa.String(), nullable=True),
        sa.Column('status_session', sa.String(), nullable=False),
        sa.Column('room_id', sa.Integer(), sa.ForeignKey('room.room_id'), nullable=True),
        sa.Column('movie_id', sa.Integer(), sa.ForeignKey('movie.movie_id'), nullable=True),
    )
    op.create_table(
        'ticket',
        sa.Column('ticket_id', sa.Integer(), primary_key=True),
        sa.Column('chair_number', sa.Integer(), nullable=False),
        sa.Column('ticket_type', sa.String(), nullable=False),
        sa.Column('ticket_price', sa.Float(), nullable=False),
        sa.Column('purchase_date', sa.DateTime(), nullable=False),
        sa.Column('payment_status', sa.String(), nullable=False),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('session.session_id'), nullable=True),
    )
    op.create_table(
        'paymentdetails',
        sa.Column('payment_id', sa.Integer(), primary_key=True),
        sa.Column('transaction_id', sa.String(), nullable=False),
        sa.Column('payment_method', sa.String(), nullable=False),
        sa.Column('final_price', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('payment_date', sa.DateTime(), nullable=False),
        sa.Column('ticket_id', sa.Integer(), sa.ForeignKey('ticket.ticket_id'), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('paymentdetails')
    op.drop_table('ticket')
    op.drop_table('session')
    op.drop_table('room')
    op.drop_table('movie_director_link')
    op.drop_table('movie')
    op.drop_table('director')
    # ### end Alembic commands ###
