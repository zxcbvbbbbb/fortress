import sys,os
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fortress.settings")
    import django
    django.setup()
    from backend import main,ssh_interactive
    interactive_obj = main.ArgvHander(sys.argv)
    interactive_obj.call()
