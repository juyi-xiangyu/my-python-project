from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 1. 创建一个Flask应用
app = Flask(__name__)
# 2. 允许跨域访问
CORS(app)
# 配置数据库的地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
# 3. 创建数据库对象
db = SQLAlchemy(app)

# 定义Todo模型
class Todo(db.Model):
    # 定义表名
    id = db.Column(db.Integer, primary_key=True)
    # 定义列对象
    task = db.Column(db.String(80), unique=True, nullable=False)
    # 定义打印该对象时的返回内容
    def serialize(self):
        return {
            'id': self.id,
            'task': self.task
        }

# 定义处理todos的路由
@app.route('/todos', methods=['GET', 'POST', 'DELETE'])
# 定义处理todos的函数
def handle_todos():
    # 处理POST请求
    if request.method == 'POST':
        # 判断请求是否为JSON
        if not request.is_json:
            # 返回错误响应
            return jsonify({"msg": "Missing JSON in request"}), 400
        # 获取请求中的task参数    
        task = request.json.get('task', None)
        # 如果task参数不存在 
        if not task:
            # 返回错误响应
            return jsonify({"msg": "Missing task parameter"}), 400
        # 创建一个Todo对象
        todo = Todo(task=task)
        # 将Todo对象保存到数据库中
        db.session.add(todo)
        # 提交数据库会话
        db.session.commit()
        # 返回创建成功的响应    
        return jsonify({"msg": "Todo created", "todo": task}), 201
    # 处理DELETE请求
    if request.method == 'DELETE':
        # 判断请求是否为JSON
        if not request.is_json:
            # 返回错误响应
            return jsonify({"msg": "Missing JSON in request"}), 400
        # 获取请求中的task参数
        task = request.json.get('task', None)
        # 如果task参数不存在
        if not task:
            # 返回错误响应
            return jsonify({"msg": "Missing task parameter"}), 400
        # 从数据库中查找task参数对应的Todo对象
        todo = Todo.query.filter_by(task=task).first()
        # 如果Todo对象不存在
        if not todo:
            # 返回错误响应
            return jsonify({"msg": "Todo not found"}), 404
        # 删除Todo对象    
        db.session.delete(todo)
        # 提交数据库会话
        db.session.commit()
        # 返回删除成功的响应
        return jsonify({"msg": "Todo deleted"}), 200
    # 处理GET请求
    todos = Todo.query.all()
    # 返回查询到的所有Todo对象
    return jsonify([e.serialize() for e in todos])
# 定义处理todo的路由
if __name__ == '__main__':
    # 4. 运行应用
    with app.app_context():
    # 在这里进行你的操作
        db.create_all()
        app.run(port=8080, debug=True)