# species	island	bill_length_mm	bill_depth_mm	flipper_length_mm	body_mass_g

from flask import Flask, render_template,request
import pandas as pd
import pickle
import sklearn
import numpy as np
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

app=Flask(__name__)
model=pickle.load(open('rfc.pkl','rb'))

@app.route('/',methods=['GET'])  #mapping the URLs to a specific function that will handle the logic for that URL
def home_fun():
    return render_template('home.html') #redirect to html

@app.route('/predict',methods=['POST'])
def predict():
    island_Dream=0
    if request.method == 'POST':
        
        bill_length_mm=float(request.form['bill_length_mm'])
        bill_depth_mm=float(request.form['bill_depth_mm'])
        flipper_length_mm=int(request.form['flipper_length_mm'])
        body_mass_g=int(request.form['body_mass_g'])
        island_Torgersen=request.form['island_Torgersen']
        if (island_Torgersen=='Torgersen'):
            island_Torgersen=1
            island_Dream=0
        elif (island_Torgersen=='Dream'):
            island_Torgersen=0
            island_Dream=1
        else:
            island_Dream=0
            island_Torgersen=0
        sex_male=request.form['sex_male']
        if (sex_male=='male'):
            sex_male=1
        else:
            sex_male=0
        
        data={'bill_length_mm':bill_length_mm,
              'bill_depth_mm':bill_depth_mm,
              'flipper_length_mm':flipper_length_mm,
              'body_mass_g':body_mass_g,
              'island_Dream':island_Dream,
              'sex_male':sex_male}
        
        df=pd.DataFrame([data])   
        prediction=model.predict(df)
        output=prediction[0]
        print(output)
        if (output == 0):
            #spe="Adelie"
            return render_template('home.html', prediction_text='Penguin is Adelie')
        elif (output == 1):
            #spe='Chinstrap'
            return render_template('home.html', prediction_text='Penguin is Chinstrap')
        elif (output == 2):
            #spe='Gentoo'
            return render_template('home.html', prediction_text='Penguin is Gentoo')
        else:
            return render_template('home.html', prediction_text='Invalid')

    else:
        render_template('home.html')

if __name__ == '__main__':  #if we dont write this section then our model will not execute or work
    app.run(debug=True)