# -*- coding:utf-8 -*-
import sys
import copy

from code.app.v2frame.v2tool import *


def handle_help_cmd(cmd=None):
    if cmd is None:
        print("all cmd are as follow:")
        for c in cmd_array:
            print("\t%s"%(c.get_cmd()))

        print("\ntype : \"help [cmd]\" to show details")
    else:
        for c in cmd_array:
            if cmd == c.get_cmd():
                c.show_help()
                return
        handle_help_cmd()


def main():
    if len(sys.argv) < 2:
        handle_help_cmd()
        return 0

    cmd_argv = copy.deepcopy(sys.argv)
    cmd_argv.pop(0)
    cmd = cmd_argv.pop(0)
    if cmd == "help":
        if len(cmd_argv) == 0:
            handle_help_cmd()
        else:
            handle_help_cmd(cmd_argv[0])
    elif handle_tool_cmd(cmd, cmd_argv) is False:
        handle_help_cmd(cmd)
        return 0


if __name__ == '__main__':
    exit(main())
