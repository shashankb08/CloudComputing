from flask import Flask,render_template,request,jsonify,redirect,send_file
from flask import request
import requests
import json
from flask_restful import Resource, Api, reqparse
import string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.errorhandler(405)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify('Method not matched'), 405
@app.route('/api/v1/users',methods=['GET'])
def list_users():
    '''
    fields = ['username', 'password']
    df = pd.read_csv('data.csv', skipinitialspace=True, usecols=fields)
    
    if(len(list(df.username))==0):
        #return jsonify(len(list(df.username)))
        return jsonify(),204
    '''
    with open('data.txt','r') as fp:
      info=json.load(fp)
    if info==[]:
        return jsonify(),204
    else:
        a=[]
        for i in info:
            a.append(i['username'])
        return jsonify(a),200

#Login if username exists and password matches
#Add user if username dose not exists
@app.route('/api/v1/users',methods=['POST'])
def add_user():
    #fields = ['username', 'password']
    #df = pd.read_csv('data.csv', skipinitialspace=True, usecols=fields)
    inp=request.get_json()

    username = inp['username']
    password = inp['password']
    with open('data.txt') as fp:
      info=json.load(fp)
   # print (username)
   # print (password)
    if username and password:
        if(len(password)!=40):
            return jsonify({'message':'Password format is wrong!'}),400
        for i in info:
            if i['username']==username:
                return jsonify({'message':'username_exist'}),400
        new_info={}
        new_info['username']=username
        new_info['password']=password
        l=list()
        l.append(new_info)
        updated_info=info+l
        with open('data.txt','w') as fp1:
            json.dump(updated_info,fp1)    
        return jsonify({'message':'user_added'}),201
    else:
        return jsonify({'message':'missing_Data'}),400

#Remove given user
@app.route('/api/v1/users/<username>',methods=['DELETE'])
def remove(username):
    #fields = ['username', 'password']
    #df = pd.read_csv('data.csv', skipinitialspace=True, usecols=fields)
    with open('data.txt','r') as fp:
      info=json.load(fp)
    if (username):
        for i in info:
            if i['username']==username:
                info.remove(i)
                with open('data.txt','w') as fp1:
                    json.dump(info,fp1)
                    return jsonify({'message':'user_removed'}),200
        return jsonify({'message':'user_dosent_exist'}),200
        '''
        if (username in list(df.username)):
            df=df.drop(df.index[list(df.username).index(username)])
            df.to_csv('data.csv', index=False)
            return jsonify({'message':'user_removed'}),200
        else:
            return jsonify({'message':'user_dosent_exist'}),400
        '''
    else:
        return jsonify({'message':'missing_data'}),400


if __name__ == '__main__':
	app.run(host='0.0.0.0',port='80',debug=True)

