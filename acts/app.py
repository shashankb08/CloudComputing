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

#list of categories
@app.route('/api/v1/categories',methods=['GET'])
def list_categories():
    '''
    fields=['categories','number']
    df=pd.read_csv('categories.csv', skipinitialspace=True, usecols=fields)
    d={}
    if(df.shape[0]>0):
        
        for row in  df.itertuples():
            
            d[row[1]]=row[2]
            #d['number']=row[2]
            #dlist.append(d)
        return jsonify(d),200
     '''   
    with open('categories.txt','r') as fp:
      info=json.load(fp)
    
    if info==[]:
        return jsonify({'message':'no_categories'}),204
    else:
        l={}
        for i in info:
            l[i['categoryName']]=i['number']
        return jsonify(l),200
        

#add categoryName
@app.route('/api/v1/categories',methods=['POST'])
def add_category():
    inp=request.get_json()
    category = inp[0]

#    category = inp['categoryName']
    #fields=['categories','number']
    with open('categories.txt','r') as fp:
      info=json.load(fp)
      
    #df=pd.read_csv('categories.csv', skipinitialspace=True, usecols=fields)
    if(category):  
        '''
        if(categoryName not in list(df.categories)):
            df=df.append({'categories': categoryName,'number':0}, ignore_index=True)
            df.to_csv('categories.csv', index=False)
            return jsonify({'message':'categoryName_added'}),201
        else:
            return jsonify({'message':'alredy_exist'}),204
        '''
        for i in info:
            if i['categoryName']==category:
                return jsonify({'message':'alredy_exist'}),400
        
       
        new_info={}
        new_info['categoryName']=category
        new_info['number']=0
        l=list()
        l.append(new_info)
        updated_info=info+l
        
        with open('categories.txt','w') as fp1:
            json.dump(updated_info,fp1)    
        return jsonify({'message':'categoryName_added'}),201
    else:
        return jsonify({'message':'missing_data'}),400

#delete categoryName
@app.route('/api/v1/categories/<category>',methods=['DELETE'])
def delete_categoryName(category):
    #fields=['categories','number']
    #df=pd.read_csv('categories.csv', skipinitialspace=True, usecols=fields)
    with open('categories.txt','r') as fp:
      info=json.load(fp)
    with open('acts.txt','r') as fp2:
      info_acts=json.load(fp2)
    if(category):
        '''
        if(categoryName in list(df.categories)):
            field0=['actId','categoryName','username','timestamp','caption','upvote','imgB64']
            df0=pd.read_csv('act.csv', skipinitialspace=True, usecols=field0)
            for row in df0.itertuples():
                if row[2]==category:
                    df0=df0.drop(df0.index[list(df0.categoryName).index(category)])
            df0.to_csv('act.csv', index=False)
            df=df.drop(df.index[list(df.categories).index(category)])
            df.to_csv('categories.csv', index=False)
            return jsonify({'message':'categoryName_deleted'}),200
        '''
        for i in info:
            if i['categoryName']==category:
                info.remove(i)
                for j in info_acts:
                    if j['categoryName']==category:
                        info_acts.remove(j)
                
                with open('acts.txt','w') as fp3:
                    json.dump(info_acts,fp3)
                with open('categories.txt','w') as fp1:
                    json.dump(info,fp1)
                    return jsonify({'message':'categoryName_removed'}),200
        return jsonify({'message':'dosent_exist'}),400
    else:
        return jsonify({'message':'missing_data'}),400

#List 100 acts of the categoryName
@app.route('/api/v1/categories/<category>/acts',methods=['GET'])
def list_acts(category):
    '''
    field=['categories','number']
    df1=pd.read_csv('categories.csv', skipinitialspace=True, usecols=field)
    fields=['actId','categoryName','username','timestamp','caption','upvote','imgB64']
    df=pd.read_csv('act.csv', skipinitialspace=True, usecols=fields)
    dlist=[]
    '''
    l=[]
    with open('acts.txt','r') as fp:
        info_acts=json.load(fp)
    if(request.args.get('start')!=None and request.args.get('end')!=None):
        start=request.args.get('start')
        end=request.args.get('end')
        start=int(start)
        end=int(end)
        '''
        if(categoryName in list(df1.categories)):
            for row in df.itertuples():
                if row[2]==category and (int(row[1])in range(start,end+1)):
                    d={}
                    d['actId']=row[1]
                    d['username']=row[3]
                    d['timestamp']=row[4]
                    d['caption']=row[5]
                    d['upvote']=row[6]
                    d['imgB64']=row[7]
                    dlist.append(d)
        '''
        f=0
        for i in info_acts:
            if i['categoryName']==category and int(i['actId']) in range(start,end+1):
                l.append(i)
                f=1
        if f==1:    
            l=l[::-1]
            if len(l)<=100:
                l=l[0:len(l)]
            else:
                return({'message':'large_data'}),413
            return jsonify(l),200
        else:
            return jsonify({'message':'dosent_exist'}),204
    else:
        ''''
        if(categoryName in list(df1.categories)):
            for row in df.itertuples():
                if row[2]==category:
                    d={}
                    d['actId']=row[1]
                    d['username']=row[3]
                    d['timestamp']=row[4]
                    d['caption']=row[5]
                    d['upvote']=row[6]
                    d['imgB64']=row[7]
                    dlist.append(d)
        '''
        f=0
        for i in info_acts:
            if i['categoryName']==category:
                l.append(i)
                f=1
        if f==1:    
            l=l[::-1]
            if len(l)<=100:
                l=l[0:len(l)]
            else:
                return({'message':'large_data'}),413
            return jsonify(l),200
        else:
            return jsonify({'message':'dosent_exist'}),204
    


@app.route('/api/v1/categories/<category>/acts/size',methods=['GET'])
def act_size(category):
    '''
    fields=['categories','number']
    df=pd.read_csv('categories.csv', skipinitialspace=True, usecols=fields)
    if(categoryName in list(df.categories)):
        if(list(df.number)[list(df.categories).index(category)]!=0):
            return jsonify(list(df.number)[list(df.categories).index(category)]),200
    '''
    with open('categories.txt','r') as fp:
      info=json.load(fp)
    for i in info:
        if i['categoryName']==category:
            if int(i['number'])!=0:
                return jsonify(i['number']),200
            else:
                return jsonify({'message':'no_acts'}),204
    return jsonify({'message':'dosent_exist'}),400

@app.route('/api/v1/acts/upvote',methods=['POST'])
def upvote():
    inp=request.get_json()
    
    actId = inp['actId']
    with open('acts.txt','r') as fp:
      info_acts=json.load(fp)
    '''
    fields=['actId','categoryName','username','timestamp','caption','upvote','imgB64']
    df=pd.read_csv('act.csv', skipinitialspace=True, usecols=fields)
    b = [str(i) for i in list(df.actId)]
    #return jsonify(actId in b)
    if (actId in b):
        df.loc[df['actId']==int(actId),'upvote']+=1
        df.to_csv('act.csv', index=False)
        return jsonify({'message':'upvoted'}),200
    '''
    for i in info_acts:
            if i['actId']==actId:
                i['upvote']=int(i['upvote'])+1
                with open('acts.txt','w') as fp1:
                    json.dump(info_acts,fp1)
                    return jsonify({'message':'upvoted'}),200
    return jsonify({'message':'invalid'}),400

@app.route('/api/v1/acts/<actId>',methods=['DELETE'])
def delete_act(actId):
    '''
    fields=['actId','categoryName','username','timestamp','caption','upvote','imgB64']
    df=pd.read_csv('act.csv', skipinitialspace=True, usecols=fields)
    
    b = [str(i) for i in list(df.actId)]
    
    if (actId in b):
        categoryName=df.categoryName[list(df.actId).index(int(actId))]
        df=df.drop(df.index[list(df.actId).index(int(actId))])
        df.to_csv('act.csv', index=False)
        field1=['categories','number']
        df1=pd.read_csv('categories.csv', skipinitialspace=True, usecols=field1)
        df1.loc[df1['categories']==category,'number']-=1
        df1.to_csv('categories.csv', index=False)
        return jsonify({'message':'deleted'}),200
    '''
    with open('acts.txt','r') as fp:
        info_acts=json.load(fp)
    with open('categories.txt','r') as fp2:
        info=json.load(fp2)
    for i in info_acts:
            if i['actId']==actId:
                info_acts.remove(i)
                for j in info:
                    if j['categoryName']==i['categoryName']:
                        j['number']=int(j['number'])-1
                with open('acts.txt','w') as fp1:
                    json.dump(info_acts,fp1)
                with open('categories','w') as fp3:
                    json.dump(info,fp3)
                return jsonify({'message':'deleted'}),200
    return jsonify({'message':'invalid'}),400

@app.route('/api/v1/acts',methods=['POST'])
def upload():
    inp=request.get_json()

    actId = inp['actId']
    category = inp['categoryName']
    username = inp['username']
    timestamp = inp['timestamp']
    caption = inp['caption']
    imgB64 = inp['imgB64']
    r=requests.get('http://54.196.98.242:8080/api/v1/users')
    #r=requests.get('http://127.0.0.1:5000/api/v1/users')
    
    a=r.json()
    '''with open('categoriets.txt','r') as fp2:
        info=json.load(fp2)
    field1=['categories','with open('categoriets.txt','r') as fp2:
        info=json.load(fp2)number']
    df1=pd.read_csv('categwith open('categoriets.txt','r') as fp2:
        info=json.load(fp2)ories.csv', skipinitialspace=True, usecols=field1)
    field2=['actId','categwith open('categoriets.txt','r') as fp2:
        info=json.load(fp2)ory','username','timestamp','caption','upvote','imgB64']
    df=pd.read_csv('act.cswith open('categoriets.txt','r') as fp2:
        info=json.load(fp2)v', skipinitialspace=True, usecols=field2)
    if (username in a and with open('categoriets.txt','r') as fp2:
        info=json.load(fp2)categoryName in list(df1.categories) and (int(actId) not in list(map(int, list(df.actId))))):
        df.loc[len(df)]=[actId,categoryName,username,timestamp,caption,'0',imgB64] 
        df.to_csv('act.csv', index=False)
        df1.loc[df1['categories']==category,'number']+=1
        df1.to_csv('categories.csv', index=False)
        return jsonify({'message':'uploded'}),201
    '''
    with open('acts.txt','r') as fp:
        info_acts=json.load(fp)
    with open('categories.txt','r') as fp2:
        info=json.load(fp2)
    f=0
    for i in info_acts:
        if i['actId']==actId:
            f=1
    g=0
    for j in info:
        if j['categoryName']==category:
            g=1
    if f==0 and g==1 and username in a:
        new_info=request.get_json()
        new_info={}
        new_info['username']=username
        new_info['actId']=actId
        new_info['timestamp']=timestamp
        new_info['caption']=caption
        new_info['categoryName']=category
        new_info['imgB64']=imgB64
        new_info['upvote']=0
        l=[]
        l.append(new_info)
        updated_info=info_acts+l
        for i in info:
            if i['categoryName']==category:
                i['number']=int(i['number'])+1
                with open('categories.txt','w') as fp3:
                    json.dump(info,fp3)
        with open('acts.txt','w') as fp1:
            json.dump(updated_info,fp1)    
        return jsonify({'message':'uploded'}),201
    else:
        return jsonify({'message':'invalid'}),400

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='80',debug=True)

