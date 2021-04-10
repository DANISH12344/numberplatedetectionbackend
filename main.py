import base64
import json
import os
from src.Detection.detction import main_detection
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

from src.database.db import init_db, db_session
from flask_cors import cross_origin
from src.models.user import User

app = Flask(__name__, instance_relative_config=True,static_folder="build",template_folder="template")
# app.config.from_mapping(
#     SECRET_KEY = 'DEV')
# import os

@app.route("/api/upload_image", methods=['POST'])
@cross_origin()
def upload_image():
  file = request.files['file']
  target = os.path.abspath("src/images")
  if not os.path.isdir(target):
      os.mkdir(target)
  filename = secure_filename(file.filename)
  destination = "/".join([target, filename])
  file.save(destination)
  res = main_detection(filename)
  user = User(img=filename, result_number=res)
  db_session.add(user)
  db_session.commit()
  returnData = {
      "message":"Successfully Uploaded Image",
      "result": res
  }
  return json.dumps(returnData)

@app.route("/api/save_text", methods=['GET'])
@cross_origin()
def save_text():
  # record = json.loads(request.data)
  res = request.args.get("text")
  # res = record['text']
  number_save = open("build/number.txt", "a")
  number_save.writelines("number= " + res + "\n")
  number_save.close()
  returnData = {
      "message": "Successfully save number in file"
  }
  return send_from_directory(app.static_folder,"number.txt",as_attachment=True )

if __name__ == '__main__':
    init_db()
    app.run(debug = True)

