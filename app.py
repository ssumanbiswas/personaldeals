#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "offer.recommendation":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("merchant")
    dollars = parameters.get("dollar")
    vid = parameters.get("VoiceIdentification")
    
    cost = {'Air India':2, 'Delta Airlines':2.5, 'American Airlines':3, 'BestBuy':4, 'Ebay':5, 'Amazon':1.5 , 'Target':2 , 'Hilton' : 3, 'BMW' : 2.5}
    vid1 = {'0000': 'Non Amex user','8829' : 'suman' , '0001' : 'Hema', '0002' : 'prem', '0003' : 'swarup'}
    #if zone == "BMW":
        #if  parameters.get("merchant") == "BMW":
        #speech = "Hey Suman, I found an excellent deal for you. Instead of your standard 1% on your AMEX blue cash card, I can offer" + str(cost[zone]) + " percent cash back for your current purchase of" + dollars + "or above with" + zone + ". This offer will expire in next 30 minutes."
        #elif :
        #speech = "Hey Suman, I found an excellent deal for you. Instead of your standard 1% on your AMEX blue cash card, I can offer" + str(cost[zone]) + " percent cash back for your current purchase of" + dollars + "or above with" + zone + ". This offer will expire in next 330 minutes." 
    
    if str(zone) =='BMW':
        speech = "Hey"+ str(vid1[vid]) + ", I could offer a deal. Instead of standard "+str(cost[zone])+" on your AMEX blue cash card, I can instantly offer 6 months pro-rated installment payments on your current large purchase of 10000$ or above with" +zone+". This offer will expire in next 48 hours."
    elif str(zone) == 'Target':
        speech = "Hey" + str(vid1[vid]) + ", I located a deal for you. Since you are in " + zone + "Your Visa Chase freedom have" + str(cost[zone]) + "cashback on Department Stores for current Quarter.I would recommend to take advantage of it."
    else:
        speech = "Hey" + str(vid1[vid]) + ", I found an excellent deal based on your Card Profiles. Instead of your standard 1% on your AMEX blue cash card, I can offer" + str(cost[zone]) + " percent cash back for your current purchase of" + dollars + "or above with" + zone + ". This offer will expire in next 30 minutes." 
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
