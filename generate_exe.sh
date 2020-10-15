# /bin/bash
pyinstaller -F editor.py --exclude-module IPython:ipykernel
