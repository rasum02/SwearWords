import os
import sys

# Ensure we always run from the GreenGroceries project root,
# regardless of where the script is invoked from.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)
sys.path.insert(0, project_root)

from GreenGroceries import app

if __name__ == '__main__':
    app.run(debug=True)
