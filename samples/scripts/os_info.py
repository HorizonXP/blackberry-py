import os

def run():
    print('os.name', os.name)
    print('os.device_encoding(0)', os.device_encoding(0))
    print('os.device_encoding(1)', os.device_encoding(1))
    print('os.device_encoding(2)', os.device_encoding(2))
    print('os.getcwd()', os.getcwd())
    print('os.getlogin()', os.getlogin())
    print('os.getpid()', os.getpid())
    print('os.getppid()', os.getppid())
    print('os.get_exec_path()', os.get_exec_path())
    print('os.supports_bytes_environ', os.supports_bytes_environ)
    print('os.times()', os.times())
    width = max(len(x) for x in os.environ)
    for key in os.environ:
        print('{key:<{width}}= {}'.format(os.environ[key], **locals()))
