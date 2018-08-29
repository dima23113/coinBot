from flask import Flask
import requests
import json
from flask import request   
from flask import jsonify
import re
from flask_sslify import SSLify 
app =Flask(__name__)
sslify=SSLify(app) #for  pythonanywhere

URL="https://api.telegram.org/botTOKEN/"


def write_json(data, filename="answer_json"):
     with open(filename, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.route("/", methods=["POST", "GET"])
def index():
        if request.method =="POST":
         r=request.get_json()
         chat_id=r["message"]["chat"]["id"]
         message=r["message"]["text"]
         pattern = r"/\w+"
         if re.search(pattern, message ):
             price=get_price(parse_text(message))
             send_mess(chat_id, text=price+"USD")
         
        #write_json(r)
         return jsonify(r)
        return "<h1>bot welcomes you</h1>"
#https://api.telegram.org/botTOKEN/setWebhook?url=
def parse_text(text):
     pattern = r"/\w+"
     crypto =re.search(pattern, text).group()
     return crypto [1:]
    

def get_price(crypto):
     url = "https://api.coinmarketcap.com/v1/ticker/{}".format(crypto)
     r = requests.get(url).json()
     price=r[-1]["price_usd"]
     #write_json(r.json(),filename="price.json")
     return price


def send_mess(chat_id,text="bla bla bla"):
     url = URL+"sendMessage"
     answer = {"chat_id":chat_id, "text":text}
     r = requests.post(url, json = answer)
     return r.json()

if __name__=="__main__":
    #main()
    app.run()