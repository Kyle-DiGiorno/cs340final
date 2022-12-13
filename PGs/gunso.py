from flask import Flask, jsonify, render_template, request
import json
import subprocess
import os
import sys
import dotenv
import cv2
import numpy
from PIL import Image, PngImagePlugin
import io
import requests
import base64

gunso = Flask(__name__)
print("HIII")
port_num = 3001
coord_request_y = 50
coord_request_x = 50
id = -1
url_pre = "http://fa22-cs340-adm.cs.illinois.edu:"#"http://127.0.0.1:"
url_target = "fa22-cs340-118.cs.illinois.edu"#http://127.0.0.1:"
sd_url = "https://a9aa35612caba338.gradio.app"
port_num = "34999"#5000

# subprocess.run("[ -s server_list.sh ] && echo & python3 -m flask run -p" +
#              str(port_num)+" || echo python3 -m flask run -p"+str(port_num), shell=True, check=True)


def config_server_gunso():
    global id
    global url_pre
    global port_num
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
    r1 = requests.get(url_pre + port_num+"/settings")
    #print(r1.content)
    r = requests.put(url_pre + port_num+"/register-pg", json= {"name": "gunso", "author": "kylend2", "secret":"taylor"})
    print(r.content)
    r = r.json()
    print(r)
    
    id = r['id']
    
def send_data_gunso():
    global id
    global coord_request_y
    global coord_request_x
    global url_pre
    global url_target
    global port_num
    global sd_url
    print(id)
    if(type(id) == type('g1')):
        #list_out = [[3]*20]*20
        s = requests.get(url_pre + port_num + "/settings")
        s = s.json()
        payload = {
            "prompt": "maltese puppy",
            "steps": 5
        }
        

        sd = requests.post(sd_url +"7777/sdapi/v1/txt2img", json=payload)
        sd = sd.json()
        for i in sd['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            image.save('output.png')
        list_out = pixelation('output.png', 20,
                           20, s["palette"]).tolist()
        #print(sd)
        #sd= sd.json()
        print('bye')
        #print(sd.content)
        print('hi')
        
        print(s)
        for i in range(0, min(len(list_out),s['height']-coord_request_y)):
            for j in range(0, min(len(list_out),s['width']-coord_request_x)):
                b = 1
                
                g = requests.get(url_pre + port_num + "/frontend-pixels")
                #print(g)
                g = g.json()
                while(b and not g['pixels'][coord_request_y+i][coord_request_x+j] == list_out[i][j]):
                    r = requests.put(url_pre + port_num + "/update-pixel", json = {"id": id, "row": coord_request_y+i, "col":coord_request_x+j, "color":list_out[i][j]})
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
def pixelation(filename, width, height, pallette):

    f_pre = cv2.imread(filename=filename)
    width = min(width,f_pre.shape[0])
    height = min(height,f_pre.shape[1])
    f = numpy.zeros((width, height))
    for i in range(width):
        for j in range(height):
            f[i, j] = numpy.mean(numpy.mean(f_pre[i*int(len(f_pre)/width):(i+1)*int(
                len(f_pre)/width), j*int(len(f_pre[0])/height):(j+1)*int(len(f_pre[0])/height)]))

    #print("YANO")
    #print()
    out = numpy.zeros((min(width, len(f)), min(height, len(f[0]))))
    pallette_img = numpy.empty((0, 3))
    print(f)
    for p in pallette:
        #print("Yow")
        #print(pallette_img)
        pallette_img = numpy.append(pallette_img, numpy.array([[int(p[1:3], 16), int(
            p[3:5], 16), int(p[5:7], 16)]]), axis=0)
        #print(pallette_img)
    for x in range(min(len(f), len(out))):
        for y in range(min(len(f[x]), len(out[x]))):

            out[x, y] = numpy.array([numpy.linalg.norm(
                f[x, y]-u) for u in pallette_img]).argmin()
            # if (not out[x, y] == 2):
            #     print(numpy.mean(numpy.absolute(
            #         pallette_img-f[x, y]), axis=1))
    #print(out)
    return out
config_server_gunso()
print("G")
send_data_gunso()
print("H")