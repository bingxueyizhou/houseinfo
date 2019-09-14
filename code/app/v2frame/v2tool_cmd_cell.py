class ToolCMDCell:
    __cmd = ""
    __func = None
    __desc = []

    def __init__(self, cmd, func, help_desc):
        self.__cmd = cmd
        self.__func = func
        self.__desc = help_desc

    def get_cmd(self):
        return self.__cmd

    def func(self, argv):
        if self.__func is not None:
            return self.__func(argv)
        return None

    def show_help(self):
        if self.__desc is None:
            return

        for desc in self.__desc:
            print(desc)
        print("\n")