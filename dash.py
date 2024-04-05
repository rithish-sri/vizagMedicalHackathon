import functools
from keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
# from werkzeug import secure_filename


model = load_model("vgg16_1.keras")

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('dash', __name__, url_prefix='/dash')

def predictCataract(img):
    img = image.img_to_array(img)
    img = preprocess_input(img, data_format=None)
    img = img/255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    predicted_class_idx=np.argmax(prediction,axis=1)
    if predicted_class_idx == 0:
        result = "cataract"
    else:
        result = "normal"
    return result

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

# New Scan
@bp.route("/dashboard")
def dashboard():
    return render_template("dashHomePage.html")

@bp.route("/dashNewScan", methods=["POST", "GET"])
def dashNewScan():
    if request.method == "POST":
        doctor_id = session.get("user_id")
        model = request.form["modelName"]
        firstName = request.form["firstName"]
        secondName = request.form["secondName"]
        age = request.form["age"]
        gender = request.form["gender"]
        symptoms = request.form["symptoms"]
        input_img = request.files["image"]
        # input_img.save(secure_filename(input_img.filename))
        # print(input_img)
        # print(type(input_img))
        # output_res = predictCataract(input_img)
        # try:
        #     db.execute(
        #         "INSERT INTO scan (firstName, secondName, model, age, gender, doctor_id, symptoms, input_img, output_res) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        #         (firstName, secondName, model, age, gender, doctor_id, symptoms, input_img, output_res))
        #     db.commit()
        #     print("Succesfully entered the data")
        # except:
        #     error = "Some error"
        # flash(error)
    return render_template("dashnewScan.html")

@bp.route("/dashHomePage")
def dashHomePage():
    return render_template("dashHomePage.html")

@bp.route("/dashPatients")
def dashPatients():
    return render_template("dashPatients.html")

@bp.route("/dashSharedPatients")
def dashSharedPatients():
    return render_template("dashSharedPatients.html")