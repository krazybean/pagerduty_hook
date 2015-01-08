from flask import Flask, request, jsonify
import sys
import json
from datetime import datetime
from utils import redisq
app = Flask(__name__)

q = redisq.RedisQueue('pagerduty')


@app.route('/pagerduty/', methods=['POST'])
@app.route('/pagerduty', methods=['POST'])
def listener():
    # actaully listen and post json payload
    try:
        data = request.data
        print "Adding data-block to queue"
        q.put(data)
        print "Q-Size: {0}".format(q.qsize())
    except ValueError:
        print "Not valid Json"
        print "Output: {0}".format(request.data)
    return "OK"


@app.route('/heartbeat/', methods=['GET'])
@app.route('/heartbeat', methods=['GET'])
def json_response():
    if q.qsize():
        data = q.get()
        return jsonify(json.loads(data))
    else:
        return jsonify(Queue='Empty')

@app.route('/')
def newrelic_test():
    check = {}
    check['status'] = 'alive'
    return jsonify(check)

if __name__ == '__main__':
    print "Starting flask listener..."
    app.run(host='0.0.0.0', port=80, debug=True)
