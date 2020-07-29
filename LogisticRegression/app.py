# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            Pregnancies=float(request.form['Pregnancies'])
            Glucose = float(request.form['Glucose'])
            BloodPressure = float(request.form['BloodPressure'])
            SkinThickness = float(request.form['SkinThickness'])
            Insulin = float(request.form['Insulin'])
            BMI = float(request.form['BMI'])
            DiabetesPedigreeFunction = float(request.form['DiabetesPedigreeFunction'])
            Age = float(request.form['Age'])

            filename = 'LogisticRegmodel.sav'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            scaler = pickle.load(open("Scaler.sav", "rb"))
            # predictions using the loaded model file
            prediction=loaded_model.predict(scaler.transform([[Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]]))
            if prediction[0] == 1:
                result = 'You are a Diabetic'
            else:
                result = 'Congratulation! Your are a Non-Diabetic'

            print('prediction is', result)
            # showing the prediction results in a UI
            #return render_template('results.html',prediction=round(100*prediction[0]))
            return render_template('results.html', prediction=result)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')

@app.route("/from_postman", methods=["POST"])
def from_postman():
    Pregnancies = float(request.json['Pregnancies'])
    Glucose = float(request.json['Glucose'])
    BloodPressure = float(request.json['BloodPressure'])
    SkinThickness = float(request.json['SkinThickness'])
    Insulin = float(request.json['Insulin'])
    BMI = float(request.json['BMI'])
    DiabetesPedigreeFunction = float(request.json['DiabetesPedigreeFunction'])
    Age = float(request.json['Age'])

    filename = 'LogisticRegmodel.sav'
    loaded_model = pickle.load(open(filename, 'rb'))  # loading the model file from the storage
    scaler = pickle.load(open("Scaler.sav", "rb"))
    # predictions using the loaded model file
    prediction = loaded_model.predict(scaler.transform([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]))
    if prediction[0] == 1:
        result = 'Diabetic'
    else:
        result = 'Non-Diabetic'
    print('prediction is', result)
    return jsonify({"prediction":result})

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app