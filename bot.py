import subprocess

def test():
    subprocess.call(['echo', 'hello'], shell=True)

if __name__ == '__main__':
    test()