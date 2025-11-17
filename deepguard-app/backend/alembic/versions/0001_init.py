from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'wells',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
        sa.Column('field', sa.String),
        sa.Column('operator', sa.String),
        sa.Column('tvd', sa.Float),
    )
    op.create_table(
        'annuli',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('well_id', sa.Integer, sa.ForeignKey('wells.id'), nullable=False),
        sa.Column('limit_at_depth', sa.Float, nullable=False),
        sa.Column('gradient_bar_per_m', sa.Float, nullable=False),
        sa.Column('safety_factor', sa.Float, nullable=False, server_default='0.9'),
    )
    op.create_table(
        'tubulars',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('well_id', sa.Integer, sa.ForeignKey('wells.id'), nullable=False),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('top_md', sa.Float, nullable=False),
        sa.Column('bottom_md', sa.Float, nullable=False),
        sa.Column('od_in', sa.Float),
        sa.Column('weight_ppf', sa.Float),
    )
    op.create_table(
        'barrier_elements',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('well_id', sa.Integer, sa.ForeignKey('wells.id'), nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('md', sa.Float, nullable=False),
        sa.Column('status', sa.String, server_default='unknown'),
    )
    op.create_table(
        'critical_points',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('well_id', sa.Integer, sa.ForeignKey('wells.id'), nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('depth', sa.Float, nullable=False),
        sa.Column('description', sa.String),
    )
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('well_id', sa.Integer, sa.ForeignKey('wells.id'), nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('priority', sa.String, server_default='normal'),
        sa.Column('due_date', sa.DateTime(timezone=True)),
        sa.Column('status', sa.String, server_default='open'),
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('role', sa.String, server_default='admin'),
    )
    op.create_table(
        'measurements',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('annulus_id', sa.Integer, sa.ForeignKey('annuli.id'), nullable=False),
        sa.Column('pressure', sa.Float, nullable=False),
        sa.Column('tvd', sa.Float, nullable=False),
        sa.Column('recorded_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('measurements')
    op.drop_table('users')
    op.drop_table('tasks')
    op.drop_table('critical_points')
    op.drop_table('barrier_elements')
    op.drop_table('tubulars')
    op.drop_table('annuli')
    op.drop_table('wells')
