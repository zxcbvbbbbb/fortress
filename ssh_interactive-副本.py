from django.contrib.auth import authenticate

class SshHander(object):
    def __init__(self,argv_handler_interactive):
        self.argv_handler_interactive = argv_handler_interactive

    def auth(self):
        count = 0
        while count < 3:
            username = input('堡垒机帐号:').strip()
            password = input('password:').strip()
            user = authenticate(username=username,password=password)
            if user:
                self.user = user
                return True
            else:
                count += 1

    def interactive(self):
        if self.auth():
            print('Ready to display all the authorized host...to this user...')
            while True:
                host_group_list = self.user.host_groups.all()
                for index,host_group_obj in enumerate(host_group_list):
                    print('%s\t%s:[%s]' % (index,host_group_obj.name,host_group_obj.host_to_remote_users.count()))
                print('z.\t未分组主机:[%s]' % (self.user.host_to_remote_users.count()))

                choice = input('请选择主机组>>:').strip()
                if choice.isdigit():
                    choice = int(choice)
                    selected_host_group = host_group_list[choice]
                    while True:
                        for index,host_to_user_obj in enumerate(selected_host_group.host_to_remote_users.all()):
                            # self.host_to_user_obj = host_to_user_obj
                            print('%s\t%s' % (index, host_to_user_obj))
                        choice = input('请选择主机>>:').strip()
                        if choice.isdigit():
                            choice = int(choice)
                            selected_host_to_user_obj = selected_host_group.host_to_remote_users.all()[choice]
                            print('going to logon %s' % selected_host_to_user_obj)
                elif choice == 'z':
                    for index,host_to_user_obj in enumerate(self.user.host_to_remote_users.all()):
                        print('%s.\t%s' % (index, host_to_user_obj))


