from app import create_app
from flask_script import Manager, Shell, Server, Command, Option
import os


class createadmin(Command):
    option_list = (
        Option('--username', '-u', dest='username'),
        Option('--password', '-pwd', dest='password')
    )

    def run(self, username, password):
        from foundation.database.account import ACCOUNTS
        try:
            ac = ACCOUNTS(username=username, is_active=True, email='hakhanhlong@gmail.com', fullname='hklong')
            ac.password = password
            ac.save()
            print(username + password)
        except Exception as ex:
            print('#ERROR CREATE ACCOUNT ADMIN:' + ex.message)



app = create_app(os.getenv('BLANKSPIDER_EVR') or 'default')

manager = Manager(app)

manager.add_command('runserver', Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port='8089'))

manager.add_command('create_account_admin', createadmin())

if __name__ == '__main__':
    manager.run()







