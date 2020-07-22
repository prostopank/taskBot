import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./Your json file')
da = firebase_admin.initialize_app(cred, {
    'databaseURL': 'Your dataBase URL'
})

ref = db.reference()
users_ref = ref.child('users')


    
def addTask(user_id, title,body):
    users_ref.child(user_id).child(title).set(body)

def viewAllTasks(user_id):
    return users_ref.child(user_id).get()

def deleteTask(user_id, task):
    users_ref.child(user_id).child(task).delete()

def noneTask(user_id):
    test = users_ref.child(user_id).order_by_key().get()
    if test == None:
        x = False
    else:
        x = True 
    return x       

def getTask(user_id, task):
    x = False
    TaskList = []
    test = users_ref.child(user_id).order_by_key().get()
    for k,v in test.items():
        TaskList.append(k)
   
    for elem in TaskList:
        if elem == task:
            x = True
    return x
def getTaskForAdd(user_id, task):
    x = True
    test = users_ref.child(user_id).order_by_key().get()
    if test == None:
        return x
    else:
        TaskList = []
        test = users_ref.child(user_id).order_by_key().get()
        for k,v in test.items():
            TaskList.append(k)
   
        for elem in TaskList:
            if elem == task:
                x = False
        return x    

def getBodyTask(user_id, task):
    return users_ref.child(user_id).child(task).get()

def setBodyTask(user_id, task, body):
    return users_ref.child(user_id).child(task).set(body)