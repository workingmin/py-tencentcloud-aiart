#!/usr/bin/env python3

import os
import json
import base64
from flask import Flask, jsonify, redirect, render_template, request, url_for
import logging
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.aiart.v20221229 import aiart_client, models

app = Flask(__name__)
logging.basicConfig(filename='console.log')


@app.route('/')
def index():
    return redirect(url_for('text'), code=301)

@app.route('/text')
def text():
    return render_template('text.html')

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/texttoimage', methods = ['POST'])
def texttoimage():
    data = json.loads(request.get_data(as_text=True))

    try:
        cred = credential.Credential(
            os.environ.get("TENCENTCLOUD_SECRET_ID"),
            os.environ.get("TENCENTCLOUD_SECRET_KEY"))
        client = aiart_client.AiartClient(cred, os.environ.get("TENCENTCLOUD_REGION"))
    
        req = models.TextToImageRequest()
        req.Prompt = data.get('prompt')
        if data.get('negative_prompt'):
            req.NegativePrompt = data.get('negative_prompt')
        req.Styles = []
        req.Styles.append(data.get('style'))
        req.LogoAdd = 0
        
        resp = client.TextToImage(req)
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        out_file = os.path.join(out_dir, resp.RequestId + ".jpeg")
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(resp.ResultImage))
        
        app.logger.info("input: %s, output: %s" % (data, out_file))
        return jsonify({
            "data": resp.ResultImage
        })
    except TencentCloudSDKException as e:
        app.logger.error(e)
        return jsonify({
            "error": str(e) 
        })

@app.route('/imagetoimage', methods = ['POST'])
def imagetoimage():
    data = json.loads(request.get_data(as_text=True))
    
    try:
        cred = credential.Credential(
            os.environ.get("TENCENTCLOUD_SECRET_ID"),
            os.environ.get("TENCENTCLOUD_SECRET_KEY"))
        client = aiart_client.AiartClient(cred, os.environ.get("TENCENTCLOUD_REGION"))
    
        req = models.ImageToImageRequest()
        
        if data.get('base64'):
            req.InputImage = data.get('base64')
        if data.get('url'):
            req.InputUrl = data.get('url')
        if data.get('prompt'):
            req.Prompt = data.get('prompt')
        if data.get('negative_prompt'):
            req.NegativePrompt = data.get('negative_prompt')
        req.Styles = []
        req.Styles.append(data.get('style'))
        req.LogoAdd = 0
        
        resp = client.ImageToImage(req)
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        out_file = os.path.join(out_dir, resp.RequestId + ".jpeg")
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(resp.ResultImage))
        
        app.logger.info("input: %s, output: %s" % (data, out_file))
        return jsonify({
            "data": resp.ResultImage
        })
    except TencentCloudSDKException as e:
        app.logger.error(e)
        return jsonify({
            "error": str(e) 
        })
        