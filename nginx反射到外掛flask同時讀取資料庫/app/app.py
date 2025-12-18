from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 資料庫配置
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'flask_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'flask_password')
DB_NAME = os.getenv('DB_NAME', 'flask_db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定義資料模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# API: 獲取所有使用者
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API: 獲取單一使用者
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify({'success': True, 'user': user.to_dict()})
        return jsonify({'success': False, 'error': '使用者不存在'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API: 新增使用者
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        new_user = User(
            name=data.get('name'),
            email=data.get('email')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '使用者建立成功',
            'user': new_user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# API: 更新使用者
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': '使用者不存在'}), 404
        
        data = request.json
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '使用者更新成功',
            'user': user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# API: 刪除使用者
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': '使用者不存在'}), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': '使用者刪除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# 資料庫連線測試
@app.route('/api/db-test')
def db_test():
    try:
        # 測試資料庫連線
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'success': True,
            'message': '資料庫連線成功',
            'database': DB_NAME
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)