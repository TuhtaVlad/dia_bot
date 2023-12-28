import logging
from datetime import datetime
import sqlite3
from typing import Dict
import matplotlib.pyplot as plt
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application, CommandHandler, ContextTypes, \
    ConversationHandler, MessageHandler, filters
from io import BytesIO
from telegram import InputFile
from telegram.ext import CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Enter the blood sugar level', 'Enter a meal in carbohydrate content'],
    ['Injected insulin', 'Show statistics'],
    ['Done'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def hist(user_data: Dict[str, str]) -> str:
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return '\n'.join(facts).join(['\n', '\n'])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        'Hi! I am a bot created to help people with diabetes.',
        reply_markup=markup,
    )

    return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data['choice'] = text

    return TYPING_REPLY


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if 'choice' in context.user_data and context.user_data['choice'] == 'Enter the blood sugar level':

        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sugar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT NOT NULL,
        measure REAL
        )
        ''')

        user_data = context.user_data
        text = update.message.text
        category = user_data['choice']
        user_data[category] = text
        del user_data['choice']
        sug = user_data[category]
        sug = float(sug)

        cursor.execute('INSERT INTO Sugar (datetime, measure) VALUES (?, ?)',
                       (datetime.today().strftime('%Y-%m-%d-%H.%M.%S'), sug))

        connection.commit()
        connection.close()

        await update.message.reply_text(
            f'Your blood sugar is {sug} at {datetime.today().strftime('%Y-%m-%d-%H.%M.%S')}.',
            reply_markup=markup,
        )

    elif 'choice' in context.user_data and context.user_data['choice'] == 'Enter a meal in carbohydrate content':
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Meal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT NOT NULL,
        meal REAL
        )
        ''')

        user_data = context.user_data
        text = update.message.text
        category = user_data['choice']
        user_data[category] = text
        del user_data['choice']
        meal = user_data[category]
        meal = float(meal) / 15

        cursor.execute('INSERT INTO Meal (datetime, meal) VALUES (?, ?)',
                       (datetime.today().strftime('%Y-%m-%d-%H.%M.%S'), meal))

        connection.commit()
        connection.close()

        await update.message.reply_text(
            f'Your last meal at {datetime.today().strftime('%Y-%m-%d-%H.%M.%S')} contained {meal} carb units.',
            reply_markup=markup,
        )

    elif 'choice' in context.user_data and context.user_data['choice'] == 'Injected insulin':
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Insulin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT NOT NULL,
        insulin REAL
        )
        ''')

        user_data = context.user_data
        text = update.message.text
        category = user_data['choice']
        user_data[category] = text
        del user_data['choice']
        ins = user_data[category]
        ins = float(ins)

        cursor.execute('INSERT INTO Insulin (datetime, insulin) VALUES (?, ?)',
                       (datetime.today().strftime('%Y-%m-%d-%H.%M.%S'), ins))

        connection.commit()
        connection.close()

        await update.message.reply_text(
            f'The last time you injected insulin was {ins} units at {datetime.today().strftime('%Y-%m-%d-%H.%M.%S')}.',
            reply_markup=markup,
        )

    if 'choice' in context.user_data and context.user_data['choice'] == 'Show statistics':
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        user_data = context.user_data
        text = update.message.text
        category = user_data['choice']
        user_data[category] = text
        del user_data['choice']
        prefix = user_data[category]

        if prefix != 'all':
            original_table = 'Sugar'
            new_table = 'Sugar_day'
            column_name = 'datetime'
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {new_table} AS
            SELECT * FROM {original_table}
            WHERE {column_name} LIKE '{prefix}%';
            '''
            cursor.execute(create_table_query)
            cursor.execute(f'SELECT datetime, measure FROM {new_table}')
            data = cursor.fetchall()
            datetime_sug, measure = zip(*data)
            plt.plot(datetime_sug, measure, marker='o')
            plt.title('Graph of Blood Sugar Level Changes')
            plt.xlabel('Date and time')
            plt.ylabel('Measure')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            image_stream_Sugar = BytesIO()
            plt.savefig(image_stream_Sugar, format='png')
            image_stream_Sugar.seek(0)
            await update.message.reply_photo(photo=InputFile(image_stream_Sugar))
            plt.close()

            original_table = 'Meal'
            new_table = 'Meal_day'
            column_name = 'datetime'
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {new_table} AS
            SELECT * FROM {original_table}
            WHERE {column_name} LIKE '{prefix}%';
            '''
            cursor.execute(create_table_query)
            cursor.execute(f'SELECT datetime, meal FROM {new_table}')
            data = cursor.fetchall()
            datetime_meal, measure = zip(*data)
            plt.plot(datetime_meal, measure, marker='o')
            plt.title('Meal Intake Chart')
            plt.xlabel('Date and time')
            plt.ylabel('Meal')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            image_stream_Meal = BytesIO()
            plt.savefig(image_stream_Meal, format='png')
            image_stream_Meal.seek(0)
            await update.message.reply_photo(photo=InputFile(image_stream_Meal))
            plt.close()

            original_table = 'Insulin'
            new_table = 'Insulin_day'
            column_name = 'datetime'
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {new_table} AS
            SELECT * FROM {original_table}
            WHERE {column_name} LIKE '{prefix}%';
            '''
            cursor.execute(create_table_query)
            cursor.execute(f'SELECT datetime, insulin FROM {new_table}')
            data = cursor.fetchall()
            datetime_ins, measure = zip(*data)
            plt.plot(datetime_ins, measure, marker='o')
            plt.title('Insulin Intake Chart')
            plt.xlabel('Date and time')
            plt.ylabel('Injected insulin')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            image_stream_Insulin = BytesIO()
            plt.savefig(image_stream_Insulin, format='png')
            image_stream_Insulin.seek(0)
            await update.message.reply_photo(photo=InputFile(image_stream_Insulin))
            plt.close()

            connection.close()

            await update.message.reply_text(
                f'Here are the charts for this day {prefix}.',
                reply_markup=markup,
            )

        else:
            cursor.execute('SELECT datetime, measure FROM Sugar')
            data = cursor.fetchall()
            datetime_sug, measure = zip(*data)
            plt.plot(datetime_sug, measure, marker='o')
            plt.title('Graph of Blood Sugar Level Changes')
            plt.xlabel('Date and time')
            plt.ylabel('Measure')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            image_stream_Sugar = BytesIO()
            plt.savefig(image_stream_Sugar, format='png')
            image_stream_Sugar.seek(0)
            await update.message.reply_photo(photo=InputFile(image_stream_Sugar))
            plt.close()

            cursor.execute('SELECT datetime, meal FROM Meal')
            data = cursor.fetchall()
            datetime_meal, measure = zip(*data)
            plt.plot(datetime_meal, measure, marker='o')
            plt.title('Meal Intake Chart')
            plt.xlabel('Date and time')
            plt.ylabel('Meal')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            image_stream_Meal = BytesIO()
            plt.savefig(image_stream_Meal, format='png')
            image_stream_Meal.seek(0)
            await update.message.reply_photo(photo=InputFile(image_stream_Meal))
            plt.close()

            cursor.execute('SELECT datetime, insulin FROM Insulin')
            data = cursor.fetchall()
            datetime_ins, measure = zip(*data)
            plt.plot(datetime_ins, measure, marker='o')
            plt.title('Insulin Intake Chart')
            plt.xlabel('Date and time')
            plt.ylabel('Injected insulin')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            image_stream_Insulin = BytesIO()
            plt.savefig(image_stream_Insulin, format='png')
            image_stream_Insulin.seek(0)
            await update.message.reply_photo(photo=InputFile(image_stream_Insulin))
            plt.close()

            connection.close()

            await update.message.reply_text(
                'These are the graphs for all time.',
                reply_markup=markup,
            )


    else:
        await update.message.reply_text(
            'Data entered in the table!',
            reply_markup=markup,
        )
    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    await update.message.reply_text(
        f'Your request history: {hist(user_data)}',
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token('BOT-TOKEN').build()

    def error_handler(update: Update, context: CallbackContext) -> None:
        logger.error(f'Update {update} caused error {context.error}')

    application.add_error_handler(error_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex(
                        '^(Enter the blood sugar level|Enter a meal in carbohydrate content|Injected insulin|Show statistics)$'),
                    regular_choice
                )
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex('^Done$')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex('^Done$')),
                    received_information,
                )
            ],
        },
        fallbacks=[
            MessageHandler(filters.Regex('^Done$'), done),
            CommandHandler("start", start),
        ],
    )

    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
