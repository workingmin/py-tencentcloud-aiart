#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import os
import json
import base64
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.aiart.v20221229 import aiart_client, models


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <input.json>")
        exit(1)
           
    try:
        with open(sys.argv[1]) as f:
            obj = json.loads(f.read())
            
        cred = credential.Credential(
            os.environ.get("TENCENTCLOUD_SECRET_ID"),
            os.environ.get("TENCENTCLOUD_SECRET_KEY"))
        client = aiart_client.AiartClient(cred, os.environ.get("TENCENTCLOUD_REGION"))
        
        req = models.TextToImageRequest()
        req.Prompt = obj.get('prompt')
        req.NegativePrompt = obj.get('negative_prompt')
        req.Styles = []
        req.Styles.append(obj.get('style'))
        req.LogoAdd = 0
        
        resp = client.TextToImage(req)
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        out_file = os.path.join(out_dir, resp.RequestId + ".jpg")
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(resp.ResultImage))
    except TencentCloudSDKException as e:
        print(e)
    except Exception as e:
        print(e)