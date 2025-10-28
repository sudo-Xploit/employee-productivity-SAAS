import os
import sys
from alembic.config import Config
from alembic import command

# Get the directory of this script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create the Alembic configuration
alembic_cfg = Config(os.path.join(dir_path, "alembic.ini"))

# Run the autogenerate command
command.revision(alembic_cfg, "Initial migration", autogenerate=True)
