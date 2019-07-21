#import docker
import docker
import requests
import datetime
import time
from threading import Lock
import threading
from flask import Flask,render_template,request,jsonify,redirect,send_file
from flask_restful import reqparse
import binascii
import json
import os
import base64
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

#client = docker.from_env()
lock= Lock()
lock2= Lock()
ports=[8000,8001,8002,8003,8004,8005,8006,8007,8008,8009]
active_ports=[8000] #8000
requests_count=0
flag=0


def round_robin():
    global active_ports
    res=active_ports.pop(0)
    active_ports.append(res)
    print("container selected : ",res)
    return res

@app.route('/')
def func():
    print("default path")
    return jsonify({}),200

@app.route('/api/v1/<path:path>',methods=["GET","POST","DELETE"])
def request_routing(path):
    global requests_count
    global flag
    if(flag==0):
        flag=1
        scaling()
    requests_count=requests_count + 1
    container=round_robin()
    print("Path: ",path)
    url_r="http://localhost:"+str(container)+"/api/v1/"+path
    if(request.method=="GET"):
        r = requests.get(url = url_r )
    elif(request.method=="POST"):
        data = request.get_json()
        headers={'content-type':'application/json'}
        r = requests.post(url = url_r, data = json.dumps(data),headers=headers)
    else: #method is delete
        r = requests.delete(url = url_r)
    print("container choosen :",container)
    print("r : ",r,'\n\n\n\n')
    if(r.status_code==200):
        result = r.json()
        return jsonify(result),200
    elif(r.status_code==201):
            return jsonify({}),201
    elif(r.status_code==400):
        return jsonify(r.reason),400
    elif(r.status_code==204):
        return jsonify({}),204
    elif(r.status_code==404):
        return jsonify({}),404
    elif(r.status_code==405):
        return jsonify({}),405
    else:
        return jsonify({}),500

 
def fault_tolerance():
    threading.Timer(1.0, fault_tolerance).start()
    #lock.acquire()
    for i in active_ports:
            r=requests.get("http://localhost:"+str(i)+"/api/v1/_health")
            if(r.status_code==500):
            	lock.acquire()
            	k=active_ports.remove(i)
            	res = os.popen("sudo docker container ls | grep -i \""+str(i)+"\"").read()
            	con_id = str(res).split()[0]
            	os.system("sudo docker stop "+ con_id)
            	os.system("sudo docker rm "+ con_id)
            	os.system("sudo docker run -d -v /home/ubuntu/database:/app/database -p "+str(i)+":80 acts")
            	active_ports.append(i)
            	lock.release()

def scaling():
    global requests_count
    threading.Timer(120.0, scaling).start()
    total_active=1
    if(requests_count<20):
        total_active=1
    elif(requests_count<40):
        total_active=2
    elif(requests_count<60):
        total_active=3
    elif(requests_count<80):
        total_active=4
    elif(requests_count<100):
        total_active=5
    elif(requests_count<120):
        total_active=6
    elif(requests_count<140):
        total_active=7
    elif(requests_count<160):
        total_active=8
    elif(requests_count<180):
        total_active=9
    elif(requests_count<200):
        total_active=10
    print("scaling function")
    if(total_active > len(active_ports)): #scale-up
        n=total_active-len(active_ports)
        for i in range(0,n):
            for j in ports:
                if j not in active_ports:
                    res=os.popen("sudo docker run -d -v /home/ubuntu/database:/app/database -p "+str(j)+":80 acts")
                    active_ports.append(j)
                    break
    else: #scale-down
        lock2.acquire()
        active_ports.sort(reverse=True)
        n=len(active_ports) - total_active
        l=[]
        for i in range(0,n):
                l.append(active_ports[i])
        for i in l:
                active_ports.remove(i)
        for k in l:
        	res = os.popen("sudo docker container ls | grep -i \""+str(k)+"\"").read()
        	con_id = str(res).split()[0]
        	os.system("sudo docker stop "+ con_id)
        	os.system("sudo docker rm "+ con_id)
        #active_ports.pop(i) #pop from active list
        active_ports.sort()
        lock2.release()
    requests_count=0
#scaling()
fault_tolerance()       
if __name__ == '__main__': 
    app.run(debug=True,host="0.0.0.0",port=80)

