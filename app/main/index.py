import pandas as pd
import pickle
import requests
import jwt
import time

from flask import Blueprint, request, render_template
from flask import current_app as app

main = Blueprint('main', __name__)
result = Blueprint('result', __name__)
metabase = Blueprint('metabase', __name__) 

@main.route('/')
def index():
      return render_template('main/index.html')

@result.route('/POST', methods=['GET', 'POST'])
def post():
      minions = request.args.get('minions')
      gold = request.args.get('gold')
      ward = request.args.get('ward')
      damage = request.args.get('damage')
      kill = request.args.get('kill')
      death = request.args.get('death')
      assist = request.args.get('assist')

      with open('app/main/model.pkl', 'rb') as pf:
            model = pickle.load(pf)

      params = [int(minions), int(gold), int(ward), int(damage), int(kill), int(death), int(assist)]
      
      df = pd.DataFrame(params).T
      df.columns = ['totalMinionsKilled', 'goldEarned', 'wardsPlaced', 'damagePerMinute', 'kills', 'deaths', 'assists']
      
      y_pred = model.predict(df)

      if y_pred[0] == 'MID':
            path_route = render_template('main/mid.html', y_pred=y_pred)

      elif y_pred[0] == 'TOP':
            path_route = render_template('main/top.html', y_pred=y_pred)

      elif y_pred[0] == 'JUNGLE':
            path_route = render_template('main/jug.html', y_pred=y_pred)
            
      elif y_pred[0] == 'AD CARRY':
            path_route = render_template('main/ad.html', y_pred=y_pred)
      else: 
            path_route = render_template('main/sup.html', y_pred=y_pred)

      return path_route, 200

@metabase.route('/dashboard')
def dashboard():
      METABASE_SITE_URL = "http://localhost:3000"
      METABASE_SECRET_KEY = "e65ca6a8be18ca63c10e7b54776b93c7da99978ddd980f5b93db40eb1a383844"

      payload = {
      "resource": {"dashboard": 1},
      "params": {},
      "exp": round(time.time()) + (60 * 10) # 10 minute expiration
      }
      token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
      iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"
      
      html = render_template('main/dash.html', iframeUrl=iframeUrl)

      return html, 200
