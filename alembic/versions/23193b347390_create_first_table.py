"""create first table

Revision ID: 23193b347390
Revises: <Nombre de la persona quien revisa o crea la migración>
Create Date: 2023-10-25 11:20:55.271824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23193b347390' #identificador de la revisión,sirve para que alembic
#pueda identificar en que revisión esta actualmente
down_revision: Union[str, None] = None #identificador de la revisión anterior,sirve para
#que alembic pueda identificar la versión anterior a esta (puede ser None cuando no hay una anterior)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None: #son los comandos para aplicar la versión actual que queremos generar en la base de datos
    #es decir los cambios actuales que vamos a implementar en la estructura de la base de datos
    op.create_table(
        'persona',
        sa.Column("nombre",sa.String(),nullable=False),
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("usuario",sa.String(),nullable=False),
        sa.Column("password",sa.String(),nullable=False)
    )
    

def downgrade() -> None:#son los comandos para revertir el estado actual de la base de datos
    #es decir revertir los cambios aplicados por la instrucción upgrade
    op.drop_table("persona")
