from flask import Flask,render_template,request
import ISS_Info as iss
from datetime import datetime
import time,notify2
from geopy.geocoders import Nominatim

app=Flask(__name__)
notify2.init("iss app")
geolocator = Nominatim(user_agent="iss-city")



@app.route('/')
@app.route('/city',methods=['GET','POST'])
def city_get():

	if request.method=='GET':
		return render_template('index.html')
	if request.method == 'POST':
		city=request.form['city']
		location = geolocator.geocode(city)

		#lon=request.form['lon']
		if(location):
			lat=(location.latitude)
			lon=(location.longitude)
			l=iss.iss_passes(lat,lon)['response']
			print(l)
			a=[]
			passes=[]
			for i in range(len(l)):
				a.append(int(l[i]['risetime']))
				passes.append(time.ctime(int(l[i]['risetime'])))
				#print(time.ctime(int(l[i]['risetime'])))
			# print(len(b))
			flag=0
			return render_template('city-list.html',passes=passes,len=len(passes),flag=flag,city=city)
		else:
			flag=1
			passes=['Please check the city name and try again']
			return render_template('city-list.html',passes=passes,len=len(passes),flag=flag)
	# n=notify2.Notification("test","iss is up","go")


	# while True:
		# t=int(time.time())
		# if t in a:	
		# 	n.show()

@app.route('/coord',methods=['GET','POST'])

def coord():
	if request.method == 'GET':
		return render_template('coord-list.html')
	if request.method == 'POST':
		lat=request.form['lat']
		lon=request.form['lon']
		print(lat,lon)
		x=str(lat)+','+str(lon)
		try:
			city=geolocator.reverse(x)
			l=iss.iss_passes(lat,lon)['response']
			print(l)
			a=[]
			passes=[]
			for i in range(len(l)):
				a.append(int(l[i]['risetime']))
				passes.append(time.ctime(int(l[i]['risetime'])))
				#print(time.ctime(int(l[i]['risetime'])))
			# print(len(b))
			flag=0
			return render_template('result.html',passes=passes,len=len(passes),city=city,flag=flag)
		except:
			passes=["Please enter valid cordinates"]
			city=""
			flag=1
			return render_template('result.html',passes=passes,len=len(passes),city=city,flag=flag)


if __name__ == '__main__':
	app.run(debug=True)