from flask import Flask,request,render_template
import os
import requests
from dotenv import load_dotenv
#load_dotenv() 
API_KEY=os.getenv("API_KEY")

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def weather():
    weather=None
    if request.method=="POST":
        city=request.form.get("city").strip()
        with open("example.txt", "a") as file:
            file.write(city+"\n")  
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
        response = requests.get(url).json() 
        if response.get("cod") == 200:
            weather = {
                "city": response['name'],
                "temp": response['main']['temp'],
                "feels_like": response['main']['feels_like'],
                "desc": response["weather"][0]["description"].title(),
                "icon": response["weather"][0]["icon"]
            }
        else:
            weather={"error":"Enter a valid city"}
    
    return render_template("index.html", weather=weather,current_page='weather')
    
    
    
@app.route("/history")
def history():
    cities=[]
    try:
        with open("example.txt",'r') as file:
            cities = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        cities=[]
        
    return render_template('history.html',cities=cities,current_page='history')
    
if __name__ == "__main__":
    app.run(debug=True)
