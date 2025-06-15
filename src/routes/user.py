from flask import Blueprint

user_bp = Blueprint('user', __name__)
 
@user_bp.route('/test')
def test():
    return {'message': 'User routes are working!'} 