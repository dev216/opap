from xml.etree.ElementPath import _SelectorContext

__author__ = 'nassos'

class ProgramMenu:

    def __init__(self):
        self.options = { 0: "Get Last Draw",
                         1: "Update Draws" }
        self.options_count = len(self.options.keys())

    def validate_option(self, option_selected):
        res = True

        if option_selected.isdigit() is False:
            res = False
        else:
            option_num = int(option_selected)
            if option_num not in range(1,self.options_count+1):
                res = False
        return res

    def print_menu(self):
        res = ""
        for (k, v) in self.options.items():
            if k != 0:
                res += "\n"
            res += "{0}: {1}".format(k+1, v)
        print(res)

    def get_action_str(self,option_selected):
        if self.validate_option(option_selected):
            option_num = int(option_selected)-1
            return self.options[option_num]
        else:
            return None

    def get_action_num(self,option_selected):
        if self.validate_option(option_selected):
            return int(option_selected)
        else:
            return None

