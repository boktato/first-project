from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.eyhsbis.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/user", methods=["POST"])
def user_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    user_list = list(db.user.find({}, {'_id': False}))
    count = len(user_list) + 1

    doc = {
        'num': count,
        'name': name_receive,
        'comment': comment_receive,
        'done': 0
    }

    db.user.insert_one(doc)
    return jsonify({'msg': '저장 완료'})


@app.route("/user", methods=["GET"])
def user_get():
    comment_list = list(db.user.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})


@app.route("/user/done", methods=["POST"])
def delete_comment():
    num_receive = request.form['num_give']
    db.user.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '삭제 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


