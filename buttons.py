from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton

button_newTask = "New Task 🗒️"
button_deleteTask = "Delete Task ❌"
button_editTask = "Edit Task ✎"
button_viewAllTasks = "View All Tasks 🔎"
button_markTaskCompleted = "Mark task completed ✔️"

def getBaseKeyboard():
    keyboard=[
        [
            KeyboardButton(text=button_newTask), KeyboardButton(text=button_viewAllTasks),
        ],
        [
            KeyboardButton(text=button_editTask), KeyboardButton(text=button_deleteTask),
        ],
        [
            KeyboardButton(text=button_markTaskCompleted),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard,resize_keyboard=True)    