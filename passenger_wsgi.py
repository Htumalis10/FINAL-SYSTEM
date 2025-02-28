import sys
import os

INTERP = os.path.expanduser("/home/Htumalis10/.virtualenvs/env/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

from app import create_app
application = create_app() 