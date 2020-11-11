import pytest
from immudb.client import ImmudbClient
import immudb.constants
from immudb.grpc import schema_pb2
import string,random
import grpc._channel
import google.protobuf.empty_pb2

def get_random_name(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters+string.digits) for i in range(length))

class TestUser:
    def test_users_functions(self):
        try:
            a = ImmudbClient("localhost:3322")
            a.login("immudb","immudb")
        except grpc._channel._InactiveRpcError as e:
            pytest.skip("Cannot reach immudb server")
        users=a.listUsers()
        assert type(users.userlist.users[0])==schema_pb2.User
        
        user="test_"+get_random_name(8)
        password="Pw0:"+get_random_string(12)
        database="defaultdb"
        permission=immudb.constants.PERMISSION_RW
        
        resp=a.createUser(user, password, permission, database)
        assert type(resp.reply)== google.protobuf.empty_pb2.Empty
        
        try:
            resp=a.createUser(user, password, permission, database)
            assert False # it is not allowed to create a user twice
        except grpc._channel._InactiveRpcError as e:
            assert e.details()=='user already exists'
            
        user1="test_"+get_random_name(8)
        password="Pw0:"+get_random_string(12)
        database="defaultdb"
        permission=immudb.constants.PERMISSION_RW
        
        try:
            resp=a.createUser(user1, "12345", permission, database)
            assert False # it is not allowed to create a trivial password
        except grpc._channel._InactiveRpcError as e:
            pass
        
        try:
            resp=a.createUser(user1, "12345", permission, database)
            assert False # it is not allowed to create a trivial password
        except grpc._channel._InactiveRpcError as e:
            pass
        
        newPassword="Pw1:"+get_random_string(12)
        resp=a.changePassword(user, newPassword, password)
        assert type(resp.reply)== google.protobuf.empty_pb2.Empty

        
        



