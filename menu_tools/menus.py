
def selection_menu(prompt, options):
    choice_not_made = True
    while choice_not_made:
        try:
            print(prompt)
            for i in range(0, len(options)):
                print("[%d] %s" % (i + 1, options[i]))
            choice = int(input())
            if 1 <= choice <= len(options):
                return choice
            else:
                raise ValueError
        except ValueError:
            print("Invalid input. You must make a choice from 0 to " + str(len(options) - 1))
