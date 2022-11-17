from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.eyhsbis.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def p4_home():
    return render_template('p4_index.html')

app.route('/p2')
def p2home():
   return render_template('p2.html')

@app.route("/p2_comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    doca = {
        'comment': comment_receive,
    }
    db.p2_comment.insert_one(doca)
    return jsonify({'msg':'입력 완료!'})

@app.route("/p2_comment", methods=["GET"])
def comment_get():
    comment_list = list(db.p2_comment.find({}, {'_id': False}))
    return jsonify({'comment':comment_list})


@app.route("/p4_user", methods=["POST"])
def p4_user_post():
    p4_name_receive = request.form['p4_name_give']
    p4_comment_receive = request.form['p4_comment_give']

    p4_user_list = list(db.p4_user.find({}, {'_id': False}))
    p4_count = len(p4_user_list) + 1

    doc = {
        'p4_num': p4_count,
        'p4_name': p4_name_receive,
        'p4_comment': p4_comment_receive,
        'p4_done': 0
    }

    db.p4_user.insert_one(doc)
    return jsonify({'msg': '저장 완료'})


@app.route("/p4_user", methods=["GET"])
def p4_user_get():
    p4_comment_list = list(db.p4_user.find({}, {'_id': False}))
    return jsonify({'p4_comments': p4_comment_list})


@app.route("/p4_user/p4_done", methods=["POST"])
def p4_delete_comment():
    p4_num_receive = request.form['p4_num_give']
    db.p4_user.update_one({'p4_num': int(p4_num_receive)}, {'$set': {'p4_done': 1}})
    return jsonify({'msg': '삭제 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


