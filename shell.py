import getpass
import os 

def cd(args):
    if len(args) < 2:
        print "Expected argument to \"cd\""
    else: 
        os.chdir(args[1])    
    return 1

def clear(args):
    """
    From user 'poke' in http://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    return 1

def help(args):
    print "Interactive Shell"
    print "Type program names with arguments and hit enter"
    print "The following are built in: {}".format(builtinstr)
    print "Use the man command for information on other programs"
    return 1

def exit(args):
    return 0

builtinstr = ["cd", "clear", "help", "exit"]
builtinfunc = [cd, clear, help, exit]
strtofuncdict = dict(zip(builtinstr, builtinfunc))

def read_line():
    user = getpass.getuser()
    cwd = os.getcwd()
    promptstring = user + ":" + cwd + "> "
    line = raw_input(promptstring)
    return line 

def split_line(line):
    tokens = line.split()
    return tokens

def execute(args):
    if len(args) < 1 :
        # Empty command entered
        return 1
    for key, value in strtofuncdict.iteritems():
        if args[0] == key:
            return value(args)
    return launch(args)

def launch(args):
    status = 0
    pid = os.fork()

    if pid == 0:
        # Child process
        try:
            os.execvp(args[0], args)
        except Exception, e:
            print "There was an exception {}".format(e.args)
    elif pid < 0:
        # Failed to fork process
        print "Failed to fork process {}".format(pid)
    else:
        # Parent process
        while not os.WIFEXITED and not os.WIFSIGNALED:
            wpid = os.waitpid(pid, status, os.WUNTRACED)
            print wpid
    return 1

def shell():
    line = ""
    args = ""
    status = 1

    while status:
        line = read_line()
        args = split_line(line)
        status = execute(args)
    
    return status

def main():
    return shell() 

if __name__ == "__main__":
    main()
