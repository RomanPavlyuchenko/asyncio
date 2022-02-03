import asyncio
from email.message import EmailMessage

import aiosmtplib
import aiosqlite

import conf


async def get_email(db_name):
    async with aiosqlite.connect(db_name) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM contacts') as cursor:
            async for row in cursor:
                yield row['email']


def template_message(user_name):
    return f'''
    Уважаемый {user_name}! \n
    Спасибо, что пользуетесь нашим сервисом объявлений.'''


async def send_mail(email):
    message = EmailMessage()
    message['From'] = 'root'
    message['To'] = email
    message['Subject'] = 'Spam'
    message.set_content(template_message(email))

    await aiosmtplib.send(message,
                          username=conf.USERNAME,
                          password=conf.PASS,
                          hostname='smtp.gmail.com',
                          port=465,
                          use_tls=True)


async def main():
    async for email in get_email('contacts.db'):
        await send_mail(email)

if __name__ == '__main__':
    asyncio.run(main())
