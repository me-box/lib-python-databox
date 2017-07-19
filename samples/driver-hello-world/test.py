import os
from flask import Flask
import json
import ssl


dpem = open(os.path.abspath("secret.pem")).read()
HTTPS_SECRETS = json.loads(dpem)
print(dpem)


fp_cert =  open(os.path.abspath('certs.crt'), 'w+')
fp_cert.write(HTTPS_SECRETS['clientcert'] or '')

fp_key = open(os.path.abspath('keys.pem'), 'w+')
fp_key.write(HTTPS_SECRETS['clientprivate'] or '')

ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ctx.load_cert_chain(
    certfile = os.path.abspath('cert.pem'),
    keyfile=os.path.abspath('key.pem')
)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8080, ssl_context=ctx)
