#!"g:\my drive\ubc\mech 540a\project\nguyen_goel_project\venv\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'numpy-stl==2.13.0','console_scripts','stl'
__requires__ = 'numpy-stl==2.13.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('numpy-stl==2.13.0', 'console_scripts', 'stl')()
    )
