from gunso import *
from pixelation import *
import threading
import os

# FLASK_APP="gunso.py"
os.system("(set FLASK_APP=gunso.py && python3 -m flask run -p3001) & (set FLASK_APP=pixelation.py && python3 -m flask run -p3002) ")
# FLASK_APP="pixelation.py"
# os.system("py -m flask run -p3001")

# config_server_pixelation()
# send_data_pixelation()
