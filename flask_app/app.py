from PIL import Image
from os import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME, X_OCR_SECRET
from botocore.exceptions import ClientError
from flask_cors import CORS
from flask import Flask
from flask import request

import time
import logging
import uuid
import boto3
import os
import requests
import json
import jsonpickle

server = Flask(__name__)
server.config['JSON_AS_ASCII'] = False

CORS(server)

S3_LOCATION = f"http://{BUCKET_NAME}.s3.amazonaws.com/"

@server.route("/api/ocr", methods=["POST"])
def clovaocr_from_image():
    image = request.files['image']
    user_id = request.form['id']
    
    #이미지 저장
    im = Image.open(image)
    path, ext = os.path.splitext(image.filename)
    imgpath = f'uploads/ocr_image{ext}'
    im.save(imgpath) # 파일명을 보호하기위한 함수, 지정된 경로에 파일 저장

    # s3 업로드
    s3_url = upload_image(image, imgpath, user_id)

    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'X-OCR-SECRET' : X_OCR_SECRET

    }

    requestJson = {
            "images": [{
                "format": "png",
                "name": "medium",
                "data": None,
                "url": s3_url,
            }],
            "lang": "ko",
            "requestId": "string",
            "resultType": "string",
            "timestamp": int(round(time.time() * 1000)),
            "version": "V1"
    }

    clova_url =  "https://g762ivic4j.apigw.ntruss.com/custom/v1/21243/84ed7d79adb3076b1861867a025ee84784c8542c4a15f9caed53ff4719a1b92c/general"

    res = requests.post(clova_url, json=requestJson, headers=headers)
    result = res.json()
    infer_texts = [field["inferText"] for field in result["images"][0]["fields"]]
    return jsonpickle.encode(get_cases(infer_texts))

def get_cases(inputlist):
    # 특약사항 부분만 추출
    start_index = inputlist.index('특약사항')
    last_index = len(inputlist) - 1 - inputlist[::-1].index('본')
    output = inputlist[start_index:last_index]

    #추출된 원소들을 문장으로 조합
    sentences = []
    sentence = ""
    for element in output:
        sentence += element
        if element.endswith("다."):
            sentences.append(sentence)
            sentence = ""
        else:
            sentence += " "
    if sentence:
        sentences.append(sentence)

    return sentences



def upload_image(image, imgpath, user_id):
    try:
        
        # filename = secure_filename(image.filename)
        image.filename = get_unique_imgname(image.filename, user_id)
    
        s3 = s3_connection()
        # s3.put_object(Bucket=BUCKET_NAME, Body=image, Key=image.filename)
        s3.upload_file(imgpath, BUCKET_NAME, image.filename,ExtraArgs={
                "ACL": "public-read",
                "ContentType": image.content_type
            } )
    except ClientError as e:
        logging.error(e)
        return None
    
    url = f"{S3_LOCATION}{image.filename}"
    
    return url    

def get_unique_imgname(filename, user_id):
    ext = filename.rsplit(".",1)[1].lower()
    # 이미지 파일명 구조 : {userid}/{uuid}.{확장자} 
    # 이미지의 원래 이름에 s3 파일이름에 들어갈 수 없는 문자가 있을 경우를 고려하여 일단 uuid만 넣었음
    return f"{user_id}/{uuid.uuid4().hex}.{ext}"  


def s3_connection():
    s3 = boto3.client('s3',aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
    return s3



