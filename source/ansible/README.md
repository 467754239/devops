## Ansible sourceCode

> ansible/utils/cmd_functions.py

```
import os
import sys
import shlex
import subprocess
import select

def run_cmd(cmd, live=False, readsize=10):

    #readsize = 10

    cmdargs = shlex.split(cmd)
    p = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout = ''
    stderr = ''
    rpipes = [p.stdout, p.stderr]
    while True:
        rfd, wfd, efd = select.select(rpipes, [], rpipes, 1)

        if p.stdout in rfd:
            dat = os.read(p.stdout.fileno(), readsize)
            if live:
                sys.stdout.write(dat)
            stdout += dat
            if dat == '':
                rpipes.remove(p.stdout)
        if p.stderr in rfd:
            dat = os.read(p.stderr.fileno(), readsize)
            stderr += dat
            if live:
                sys.stdout.write(dat)
            if dat == '':
                rpipes.remove(p.stderr)
        # only break out if we've emptied the pipes, or there is nothing to
        # read from and the process has finished.
        if (not rpipes or not rfd) and p.poll() is not None:
            break
        # Calling wait while there are still pipes to read can cause a lock
        elif not rpipes and p.poll() == None:
            p.wait()

    return p.returncode, stdout, stderr
```


> ansible/color.py

```
codeCodes = {
    'black':     '0;30', 'bright gray':    '0;37',
    'blue':      '0;34', 'white':          '1;37',
    'green':     '0;32', 'bright blue':    '1;34',
    'cyan':      '0;36', 'bright green':   '1;32',
    'red':       '0;31', 'bright cyan':    '1;36',
    'purple':    '0;35', 'bright red':     '1;31',
    'yellow':    '0;33', 'bright purple':  '1;35',
    'dark gray': '1;30', 'bright yellow':  '1;33',
    'normal':    '0'
}

def stringc(text, color):
    """String in color."""

    if ANSIBLE_COLOR:
        return "\033["+codeCodes[color]+"m"+text+"\033[0m"
    else:
        return text
```

> ssh.py 命令行执行模块
> ansible/runner/connection_plugins/ssh.py

[查看源码ssh.py](./ssh.py)  
[core module](https://github.com/ansible/ansible-modules-core)  
[extras module](https://github.com/ansible/ansible-modules-extras)  
[nagios、zabbix plugin](https://github.com/ansible/ansible-modules-extras/tree/devel/monitoring)