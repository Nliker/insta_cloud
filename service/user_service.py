import bcrypt
from datetime import datetime, timedelta
import jwt

class UserService:
    def __init__(self,user_dao,config):
        self.config=config
        self.user_dao=user_dao
    '''
    userdao
    get_user_id_and_password(email)
    insert_user(new_user)
    get_user_info(user_id)
    get_user_id_and_password(credential['email'])
    insert_friend(user_id,friend_user_id)
    get_user_frinedlist(user_id)
    delete_friend(user_id,friend_user_id)
    '''
    
    def is_email_exists(self,email):
        user=self.user_dao.get_user_id_and_password(email)
        #유저가 없다면 False,있으면 True
        if user:
            return False
        else:
            return True
        
    def create_new_user(self,new_user):
        password=new_user['password']
        new_user['hashed_password']=bcrypt.hashpw(password.encode('utf-8',bcrypt.gensalt()))
        new_user_id=self.user_dao.insert_user(new_user)
        return new_user_id

    def get_user_info(self,user_id):
        user=self.user_dao.get_user_info(user_id)

        return user

    def login(self,credential):
        user_credential=self.user_dao.get_user_id_and_password(credential['email'])
        password=credential['password']
        hashed_password=user_credential['hashed_password']
        authorized=bcrypt.checkpw(password.encode('utf-8'),hashed_password.encode('utf-8'))

        return authorized
    
    def generate_access_token(self,user_id):
        jwt_expire_time= timedelta(seconds=self.config['JWT_EXPIRE_TIME'])
        payload={
            'user_id':user_id,
            'exp':datetime.utcnow()+jwt_expire_time,
            'iat':datetime.utcnow()
        }
        access_token=jwt.encode(payload,self.config['JWT_SECRET_KEY'],'HS256')

        return access_token
    
    def get_user_id_and_password(self,email):
        user_credential=self.user_dao.get_user_id_and_password(email)

        return user_credential

    def create_user_friend(self,user_id,friend_user_id):
        result=self.user_dao.insert_friend(user_id,friend_user_id)

        return result

    def get_user_friendlist(self,user_id):
        friendlist=self.user_dao.get_user_frinedlist(user_id)
        friend_info_list=[]
        #실제 존재하는 유저만 정보를 불러 모음
        for user_id in friendlist:
            friend_info=self.user_dao.get_user_info(user_id)
            if friend_info:
                friend_info_list.append(friend_info)

        return friend_info_list
        
    def delete_user_friend(self,user_id,friend_user_id):
        result=self.user_dao.delete_friend(user_id,friend_user_id)
        return result