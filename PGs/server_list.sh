echo "t" && (export FLASK_APP=gunso.py && python3 -m flask run -p3001) &(export FLASK_APP=pixelation.py && python3 -m flask run -p3002) &