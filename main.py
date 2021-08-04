import pandas as pd
from flask import Flask, request, jsonify, Response, render_template
import re
from io import StringIO
import requests
import json
#from IPython.display import HTML
#from dotenv import load_dotenv
import os
import math

#load_dotenv()
app = Flask(__name__)
user = ""
pwd = ""
counter = 0
all_tickets_df = pd.DataFrame()
all_ticket_id = []
limit = 0


#for each query
def get_data(url):
    global user
    global pwd
    url = url
    # Do the HTTP get request
    response = requests.get(url, auth=(user, pwd))
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    return data


#show the details of each ticket
def show_ticket_by_id(tick_id):
    url = "https://zccgupta232.zendesk.com/api/v2/tickets/"+tick_id+".json"
    data = get_data(url)
    t = data["ticket"]
    d = {}
    d["Ticket ID"] = t["id"]
    d["Description"] = t["description"]
    d["Status"] = t["status"]
    d["Tags"] = t["tags"]
    d["Priority"] = t["priority"]
    d["Requester_ID"] = t["requester_id"]
    d["Assignee_ID"] = t["assignee_id"]
    return d



def show_all(ret = False):
    url = 'https://zccgupta232.zendesk.com/api/v2/tickets.json'
    data = get_data(url)
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
    df = pd.read_json("data.json")
    df.to_csv('data.csv', index = None)
    req_list = list(pd.read_csv("data.csv")["tickets"])
    d = {"Ticket_ID": [],
         "Subject": [],
         "Status": [],
         "Priority": []
        }
    for ticket in req_list:
        t = eval(ticket)
        d["Ticket_ID"].append(t['id'])
        d["Subject"].append(t['subject'])
        d["Status"].append(t['status'])
        d["Priority"].append(t['priority'])   
    new_df = pd.DataFrame(data=d)
    return new_df



def highlight(s):
    if s.Status == 'open':
        return ['background-color: pink']*len(s)
    elif s.Status == 'solved':
        return ['background-color: light-green']*len(s)
    else:
        return ['background-color: yellow']*len(s)
    

    


@app.route('/index_2.html')
def show():
    return render_template("index_2.html")

@app.route('/error.html')
def wrong():
    return render_template("error.html")

@app.route('/quit.html')
def quit():
    return render_template("quit.html")

@app.route('/all_tickets.html')
def call():
    global counter
    global limit
    counter += 1
    
    o_df = show_all()
    if(counter == 1 or (counter > limit)):
        df = o_df[0:25]
        if(counter > limit):
            counter = 1
    else:
        df = o_df[25*(counter-1): 25*counter]
        
    with open("templates/all_tickets.html") as f:
        html = f.read()
    df=df.style.apply(highlight, axis=1)
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        return html.replace("{}",df._repr_html_())
    return render_template("all_tickets.html")



@app.route('/', methods =["GET", "POST"])
def gfg():
    global user
    global pwd
    global all_tickets_df 
    global all_ticket_id 
    global limit
    
    if request.method == "POST":
        value = request.form.get("opt")
        user = request.form.get("user")
        pwd = request.form.get("p")
        all_tickets_df = show_all()
        all_ticket_id = list(all_tickets_df["Ticket_ID"])
        limit = math.ceil(len(all_ticket_id)/25)

        #show all tickets
        if(value == "A"):
            return call()
        
        if(value == "Q"):
            return quit()

        #show a ticket by id
        else:
            if(int(value) in all_ticket_id):
                ticket = show_ticket_by_id(value)
                return render_template('ticket.html', ticket_d=ticket)
            else:
                return wrong()
                
    return render_template("index_2.html")




if __name__ == '__main__':
    # don't change this line!
    app.run(host="0.0.0.0", debug=True) 
