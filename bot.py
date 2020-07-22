from telegram import Bot
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import KeyboardButton
from telegram import chat
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler
import dataBase
import buttons

from config import TG_TOKEN

TITLE, BODY = range(2)
Task_Name = range(1)
Task_Name_Edit, New_Task_Name, New_Task_Body = range(3)
Task_Name_Completed = range(1)


def doStart_handler(update: Update, context: CallbackContext):
    reply_markup = buttons.getBaseKeyboard()    
    update.message.reply_text(
        text = "Hello!\nI am a bot to save your tasks",
        reply_markup=reply_markup,
        )


#ADD NEW TASK
def addNewTask_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text = "Enter task name",
        reply_markup = ReplyKeyboardRemove(),
    )
    return TITLE
def title_handler(update: Update, context: CallbackContext):
    context.user_data[TITLE] = update.message.text
    if dataBase.getTaskForAdd(str(getChatId(update=update, context=context)),context.user_data[TITLE]):
        update.message.reply_text(
            text='Enter task description',
            reply_markup=ReplyKeyboardRemove(),
        )
        return BODY
    else:
        update.message.reply_text(
            text = "You already have such a task",
            reply_markup = buttons.getBaseKeyboard(),
        )
        return ConversationHandler.END

def finish_handler(update: Update, context: CallbackContext):
    context.user_data[BODY] = update.message.text
    dataBase.addTask(str(getChatId(update=update,context=context)), context.user_data[TITLE], context.user_data[BODY])
    update.message.reply_text(
        text = "Task added!",
        reply_markup=buttons.getBaseKeyboard(),
    )
    return ConversationHandler.END
def cancel_handler(update: Update, context: CallbackContext):  
    update.message.reply_text('')
    return ConversationHandler.END



#DELETE TASK
def deleteTask_handler(update: Update, context: CallbackContext):
    if dataBase.noneTask(str(getChatId(update=update,context=context))):
        update.message.reply_text(
            text = "Enter the name of the task you want to delete",
            reply_markup = ReplyKeyboardRemove(),
        )
        return Task_Name
    else:
        update.message.reply_text(
            text = "You have no tasks yet",
            reply_markup = buttons.getBaseKeyboard(),
        )

def taskName_handler(update: Update, context: CallbackContext):
    context.user_data[Task_Name] = update.message.text
    if dataBase.getTask(str(getChatId(update=update, context=context)),context.user_data[Task_Name]):
        dataBase.deleteTask(str(getChatId(update=update, context=context)), context.user_data[Task_Name])
        update.message.reply_text(
            text='Task deleted',
            reply_markup=buttons.getBaseKeyboard(),
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text='You dont have such a task',
            reply_markup=buttons.getBaseKeyboard(),
        )
        return ConversationHandler.END    


#EDIT TASK
def editTask_handler(update: Update, context: CallbackContext):
    if dataBase.noneTask(str(getChatId(update=update,context=context))):
        update.message.reply_text(
            text = "Enter the name of the task you want to editing",
            reply_markup = ReplyKeyboardRemove(),
        )
        return Task_Name_Edit
    else:
        update.message.reply_text(
            text = "You have no tasks yet",
            reply_markup = buttons.getBaseKeyboard(),
        )
        
def newTaskName_handler(update: Update, context: CallbackContext):
    context.user_data[Task_Name_Edit] = update.message.text
    if dataBase.getTask(str(getChatId(update=update, context=context)),context.user_data[Task_Name_Edit]):
        update.message.reply_text(
            text = "Enter a new task name",
            reply_markup = ReplyKeyboardRemove(),
        )
        return New_Task_Name
    else:
        update.message.reply_text(
            text='You dont have such a task',
            reply_markup=buttons.getBaseKeyboard(),
        )
        return ConversationHandler.END      

def newTaskBody_handler(update: Update, context: CallbackContext):
    context.user_data[New_Task_Name] = update.message.text
    update.message.reply_text(
        text = "Enter a new task description",
        reply_markup = ReplyKeyboardRemove(),
    )
    return New_Task_Body     

def finish_edit_handler(update: Update, context: CallbackContext):
    context.user_data[New_Task_Body] = update.message.text
    dataBase.deleteTask(str(getChatId(update=update,context=context)), context.user_data[Task_Name_Edit])
    dataBase.addTask(str(getChatId(update=update,context=context)),context.user_data[New_Task_Name],context.user_data[New_Task_Body])
    update.message.reply_text(
        text = "Task edited!",
        reply_markup=buttons.getBaseKeyboard(),
    )
    return ConversationHandler.END



#VIEW ALL TASKS
def viewAllTasks(update: Update, context: CallbackContext):
    if dataBase.noneTask(str(getChatId(update=update,context=context))):
        text = dataBase.viewAllTasks(str(getChatId(update=update,context=context)))
        new_list1 = []
        for k,v in text.items():
            new_list1.append(k + ":  " + v)
        update.message.reply_text(
            text = '\n'.join(new_list1),
            reply_markup=buttons.getBaseKeyboard(),
        )
    else:
        update.message.reply_text(
            text = "You have no tasks yet",
            reply_markup = buttons.getBaseKeyboard(),
        )    
    

#MARK TASK COMPLETED
def markTaskCompleted_handler(update: Update, context: CallbackContext):
    if dataBase.noneTask(str(getChatId(update=update,context=context))):
        update.message.reply_text(
            text = "Enter the name of the task you want to completed",
            reply_markup = ReplyKeyboardRemove(),
        )
        return Task_Name
    else:
        update.message.reply_text(
            text = "You have no tasks yet",
            reply_markup = buttons.getBaseKeyboard(),
        )      
def finishMark_handler(update: Update, context: CallbackContext):
    context.user_data[Task_Name_Completed] = update.message.text
    if dataBase.getTask(str(getChatId(update=update, context=context)),context.user_data[Task_Name_Completed]):
        if '✅' in dataBase.getBodyTask(str(getChatId(update=update,context=context)),context.user_data[Task_Name_Completed]):
            update.message.reply_text(
            text='This task has already been completed!',
            reply_markup=buttons.getBaseKeyboard(),
        )
        else:
            textBody = (dataBase.getBodyTask(str(getChatId(update=update,context=context)),context.user_data[Task_Name_Completed])+'✅')
            dataBase.setBodyTask(str(getChatId(update=update,context=context)),context.user_data[Task_Name_Completed], textBody)
            update.message.reply_text(
                text='Task complet!',
                reply_markup=buttons.getBaseKeyboard(),
            )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text='You dont have such a task',
            reply_markup=buttons.getBaseKeyboard(),
        )
        return ConversationHandler.END  



def getChatId(update: Update, context: CallbackContext):
    text = update.message.chat_id
    return text
 

def messageHandler(update: Update, context: CallbackContext):
    reply_markup = buttons.getBaseKeyboard()
    text = update.message.text
    if text == buttons.button_viewAllTasks:
        return viewAllTasks(update=update, context=context)
    else:    
        update.message.reply_text(
            text = "I do not know such a command",
            reply_markup=reply_markup,
            )
   
    

def main():
    print("Start")
    updater = Updater(
        token=TG_TOKEN,
        use_context=True,
    )


    ud = updater.dispatcher

    addNewTask = ConversationHandler(
        entry_points=[MessageHandler(filters=Filters.text(buttons.button_newTask), callback=addNewTask_handler)],
        states={TITLE: [MessageHandler(Filters.text, title_handler, pass_user_data=True),],BODY: [MessageHandler(Filters.text, finish_handler, pass_user_data=True),],},
        fallbacks=[CommandHandler('cancel', cancel_handler),],
    )

    deleteTask = ConversationHandler(
        entry_points=[MessageHandler(filters=Filters.text(buttons.button_deleteTask), callback=deleteTask_handler)],
        states={Task_Name: [MessageHandler(Filters.text, taskName_handler, pass_user_data=True),],},
        fallbacks=[CommandHandler('cancel', cancel_handler),],
    )

    editTask = ConversationHandler(
        entry_points=[MessageHandler(filters=Filters.text(buttons.button_editTask), callback=editTask_handler)],
        states={Task_Name_Edit: [MessageHandler(Filters.text, newTaskName_handler, pass_user_data=True),],New_Task_Name: [MessageHandler(Filters.text, newTaskBody_handler, pass_user_data=True),],New_Task_Body:[MessageHandler(Filters.text, finish_edit_handler, pass_user_data=True)]},
        fallbacks=[CommandHandler('cancel', cancel_handler),],
    )

    markTask = ConversationHandler(
        entry_points=[MessageHandler(filters=Filters.text(buttons.button_markTaskCompleted), callback=markTaskCompleted_handler)],
        states={Task_Name_Completed: [MessageHandler(Filters.text, finishMark_handler, pass_user_data=True),],},
        fallbacks=[CommandHandler('cancel', cancel_handler),],
    )
    

    
    ud.add_handler(editTask)
    ud.add_handler(deleteTask)
    ud.add_handler(addNewTask)
    ud.add_handler(markTask)
    ud.add_handler(CommandHandler("start", callback=doStart_handler))
    ud.add_handler(MessageHandler(filters=Filters.text, callback=messageHandler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()