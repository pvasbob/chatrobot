#!/usr/bin/env python
# -*- coding: utf-8 -*-

from WXBizMsgCrypt3 import WXBizMsgCrypt
from flask import Flask, request
import xml.etree.cElementTree as ET
from datetime import datetime

app = Flask(__name__)

@app.route('/wxauth', methods=['GET', 'POST'])
def wxauth():
    if request.method == 'GET':
        # Callback URL verification (Example 1)
        sVerifyMsgSig = request.args.get('msg_signature', '')
        sVerifyTimeStamp = request.args.get('timestamp', '')
        sVerifyNonce = request.args.get('nonce', '')
        sVerifyEchoStr = request.args.get('echostr', '')

        sToken = "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo"
        sEncodingAESKey = "6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt"
        sCorpID = "ww1436e0e65a779aee"

        wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
        ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,
                                        sVerifyNonce, sVerifyEchoStr)

        if ret != 0:
            print("ERR: VerifyURL ret: " + str(ret))
            return "Failed to verify URL"
        else:
            print("Callback URL verified")

        return sEchoStr

    elif request.method == 'POST':
        # Decryption of the user's message (Example 2)
        sReqMsgSig = request.args.get('msg_signature', '')
        sReqTimeStamp = request.args.get('timestamp', '')
        sReqNonce = request.args.get('nonce', '')
        sReqData = request.data

        sToken = "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo"
        sEncodingAESKey = "6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt"
        sCorpID = "ww1436e0e65a779aee"

        wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
        ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig,
                                     sReqTimeStamp, sReqNonce)

        if ret != 0:
            print("ERR: DecryptMsg ret: " + str(ret))
            return "Failed to decrypt message"

        xml_tree = ET.fromstring(sMsg)
        content = xml_tree.find("Content").text
        print("Decrypted message content: " + content)

        # Get the current local time
        local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Record the local time and decrypted user message to a text file
        with open("user_msg_record.txt", "a") as file:
            file.write(f"{local_time}\t{content}\n")

        return "Message decrypted successfully"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)