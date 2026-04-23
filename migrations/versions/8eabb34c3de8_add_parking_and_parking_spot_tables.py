"""Add parking and parking_spot tables

Revision ID: 8eabb34c3de8
Revises: c0c3c48b9cae
Create Date: 2026-04-09 14:26:05.738098

"""
from alembic import op 
import sqlalchemy as sa 



revision ='8eabb34c3de8'
down_revision ='c0c3c48b9cae'
branch_labels =None 
depends_on =None 


def upgrade ():

    op .create_table ('parkings',
    sa .Column ('id',sa .Integer (),nullable =False ),
    sa .Column ('nome',sa .String (length =120 ),nullable =False ),
    sa .Column ('endereco',sa .String (length =255 ),nullable =False ),
    sa .PrimaryKeyConstraint ('id')
    )
    op .create_table ('parking_spots',
    sa .Column ('id',sa .Integer (),nullable =False ),
    sa .Column ('codigo',sa .String (length =50 ),nullable =False ),
    sa .Column ('ocupada',sa .Boolean (),nullable =False ),
    sa .Column ('parking_id',sa .Integer (),nullable =False ),
    sa .ForeignKeyConstraint (['parking_id'],['parkings.id'],),
    sa .PrimaryKeyConstraint ('id')
    )



def downgrade ():

    op .drop_table ('parking_spots')
    op .drop_table ('parkings')

