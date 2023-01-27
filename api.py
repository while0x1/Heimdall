from flask import Flask, jsonify, request, json
import secrets
import time

app = Flask(__name__)

metrics = []

def getNodeData():
    with open('nodeData.json') as d:
        metrics = json.load(d)
    return metrics
#curl -H "Content-Type: application/json" http://localhost:5000/metrics
@app.route('/metrics')
def get_metrics():
    return jsonify(getNodeData())

@app.route('/new')
def new():   
    return "GhostChain" + str(len(getNodeData()))
#curl -H "Content-Type: application/json" -H "Auth: GhostChain3" /
# http://localhost:5000/token
#---------TODO-----
#Change the token issue from a curl request to an email - this ensures the client has access to the email account !
@app.route('/token')
def set_nonce():
    reqAuth = request.headers.get("Auth")
    metrics = getNodeData()
    allow = "GhostChain" + str(len(metrics))
    if reqAuth == allow:
        newtoken = secrets.token_hex(32)
        metrics.append({"id": newtoken, "block":0})
        json_object = json.dumps(metrics, indent=4)
        with open("nodeData.json", "w") as outfile:
            outfile.write(json_object)
        return newtoken
    else:
        return '', 403

#curl -v -X POST -H "Content-Type: application/json" -H "Auth: ABC" -d '{
#  "id": "ABC",
#  "block": 9
#}' http://localhost:5000/metrics

@app.route('/metrics', methods=['POST'])
def update_metrics():
    reqAuth = request.headers.get("Auth")
    metrics = getNodeData()
    if any(d['id'] == reqAuth for d in metrics):
        now = int(time.time())
        try:
            reqIn = request.get_json()
            reqId = reqIn['id']
            if any(d['id'] == reqId for d in metrics):
                for pools in metrics:
                    if pools['id'] == reqId:
                        pools['block'] = reqIn['block']
                        pools['time'] = now
                        json_object = json.dumps(metrics, indent=4)
                        with open("nodeData.json", "w") as outfile:
                                outfile.write(json_object)
                print(metrics)
            else:
                metrics.append(reqIn)
                json_object = json.dumps(metrics, indent=4)
                with open("nodeData.json", "w") as outfile:
                    outfile.write(json_object)
            return 'Thanks', 204
        except Exception as e:
                print(e)
    else:
        return '', 403
