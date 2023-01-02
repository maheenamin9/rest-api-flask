from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import UserSchema
from models import UserModel
from db import db
from blocklist import BLOCKLIST
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

blp = Blueprint("Users", "users", description="Operations on users")

# ---------- user endpoints ----------
@blp.route('/register')
class RegisterUser(MethodView):
    @blp.arguments(UserSchema)
    def post(self, userData):
        # check if user already exists or not
        if UserModel.query.filter(UserModel.username == userData['username']).first():
            abort(409, message="User with that username already exists")
        user = UserModel(
            username = userData['username'],
            password = pbkdf2_sha256.hash(userData['password'])
        )
        db.session.add(user)
        db.session.commit()
        return { 'message': 'user created successfully' }, 201

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, userData):
        user = UserModel.query.filter(UserModel.username == userData['username']).first()
        if user and pbkdf2_sha256.verify(userData['password'], user.password):
            accessToken = create_access_token(identity=user.id, fresh=True)
            refreshToken = create_refresh_token(identity=user.id)
            return {'accessToken': accessToken, 'refreshToken': refreshToken}, 200
        abort(401, message="Invalid credentials")

@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return { "message": "successfully logout" }

@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        currentUser = get_jwt_identity()
        newToken = create_access_token(identity=currentUser, fresh=False)
        return {"accessToken": newToken}

@blp.route('/user/<int:userId>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, userId):
        user = UserModel.query.get_or_404(userId)
        return user
    
    def delete(self, userId):
        user = UserModel.query.get_or_404(userId)
        db.session.delete(user)
        db.session.commit()
        return { 'message': 'user deleted successfully' }, 200