import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "randomstring123"
messages = []


def add_message(username, message): #add messages to the messages list
    now = datetime.now().strftime("%H:%M:%S")
    messages.append({"timestamp": now, "from": username, "message": message})

@app.route("/", methods = ["GET", "POST"])
def index():
    #Main page with instructions
    if request.method == "POST":
        session["username"] = request.form["username"]

    if "username" in session:
        return redirect(url_for("user", username = session["username"]))

    return render_template("index.html")


@app.route("/chat/<username>", methods = ["GET", "POST"])
def user(username): # add and display chat messages
    if request.method == "POST":
        username = session["username"] 
        message = request.form["message"]
        add_message(username, message)
        return redirect(url_for("user", username = session["username"]))
    
    return render_template("chat.html", username = username, chat_messages = messages)


if __name__ == "__main__": #references built-in variable
    app.run( #if statement above is true we run the app with the following arguments
        host = os.environ.get("IP", "0.0.0.0"), #using os module from standard library to get the 'IP' environment variable if it exists but return a default value if it isn't found
        port = int(os.environ.get("PORT", "5000")), #cast port as integer using int(), default is set to 5000 (common port used by Flask)
        debug = True #lets us debug code easier during devleopment stage
    )
    #__main__ is the name of default module in PY, so if not imported will be run directly (main will not be imported so app will run using arguments passed inside of statement)