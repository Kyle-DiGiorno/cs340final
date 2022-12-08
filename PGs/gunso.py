from flask import Flask, jsonify, render_template, request
import json
import subprocess
import os
import sys
import dotenv
import numpy
import requests

gunso = Flask(__name__)
print("HIII")
port_num = 3001
coord_request_y = 50
coord_request_x = 50
id = -1

# subprocess.run("[ -s server_list.sh ] && echo & python3 -m flask run -p" +
#              str(port_num)+" || echo python3 -m flask run -p"+str(port_num), shell=True, check=True)


def config_server_gunso():
    global id
    # global coord_request_y
    # global coord_request_x
    # global port_num
    # print("t")
    # with open("server_list.sh", "a") as f:
    #     print("grep "+str(port_num)+" server_list.sh")
    #     if (subprocess.run("[ -s server_list.sh ]", shell=True).returncode == 1):
    #         print("aad")
    #         f.write("(cd " + os.getcwd() +
    #                 " && export FLASK_APP="+__name__+".py" + " && python3 -m flask run -p"+str(port_num)+") &")
    #     elif (not subprocess.run("grep "+str(port_num)+" server_list.sh", shell=True).returncode == 0):
    #         print("aad2")
    #         f.write("(cd " + os.getcwd() +
    #                 " && export FLASK_APP="+__name__+".py" + " && python3 -m flask run -p"+str(port_num)+") &")
    #     print("BYE")
    #     # subprocess.run()
    # with open("server_list.json", "r") as jsonFile:
    #     servers = json.load(jsonFile)
    #     # print("HG")
    #     # print((str(port_num) in servers['servers'][0]))
    #     # print(__file__ in servers['servers',1])
    #     print(numpy.array(servers['servers'])[:, 1])
    #     if (not servers['servers'] or not (str(port_num) in numpy.array(servers['servers'])[:, 0] or __file__ in numpy.array(servers['servers'])[:, 1])):
    #         servers['servers'].append(
    #             [str(port_num), __file__, coord_request_x, coord_request_y])
    # with open("server_list.json", "w") as jsonFile:
    #     json.dump(servers, jsonFile)
    # TODO: make port number acessible
    r1 = requests.get("http://127.0.0.1:" + "5000/settings")
    #print(r1.content)
    r = requests.put("http://127.0.0.1:" + "5000/register-pg", json= {"name": "gunso", "author": "kylend2", "secret":"NA"})
    r = r.json()
    #print(r)
    
    id = r['id']
    
def send_data_gunso():
    global id
    global coord_request_y
    global coord_request_x
    print(id)
    if(type(id) == type('g1')):
        list_out = [[3]*200]*200
        for i in range(0, len(list_out)):
            for j in range(0, len(list_out)):
                b = 1
                while(b):
                    r = requests.put("http://127.0.0.1:" + "5000" + "/update-pixel", json = {"id": id, "row": coord_request_y+i, "col":coord_request_x+j, "color":list_out[i][j]})
                    #print("loss")
                    if(r.content):
                        r = r.content
                        #print(r)
                        if(not b'timeoutRemaining' in r):
                            #print("hechoco")
                            b = 0
                        #print("did")

# @gunso.route('/', methods=["GET"])
# def pg_basic():
#     list_out = [[[3]*200]*200, [[2]*200]*200, [[1]*200]*200, [[0]*200]*200]
#     print("a")
#     print(list_out[0][0][0])
#     return jsonify({"basic": list_out}), 200
config_server_gunso()
print("G")
send_data_gunso()
print("H")