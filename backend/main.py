import sys
from backend import ssh_interactive

class ArgvHander(object):
    def __init__(self,sys_argv):
        self.sys_argv = sys_argv

    def help_msg(self,error_msg=''):
        msgs = '''
        %s
        run    打印用户交互程序
        ''' % error_msg
        exit(msgs)

    def call(self):
        if len(self.sys_argv) == 1:
            self.help_msg()
        if hasattr(self,self.sys_argv[1]):
            func = getattr(self,self.sys_argv[1])
            func()

        else:
            self.help_msg('没有方法%s' % self.sys_argv[1])

    def run(self):
        from backend.ssh_interactive import SshHander
        obj = SshHander(self)
        obj.interactive()
