import sys
# sys.path.append("..")
# from .. import app
# from .. import models
# from .. import helpers

# from os import walk
# import os
import datetime




# If a menu item has children, selecting them will shot it's sub menu (no action on parents)
# All action listed in menu_list should have a function with the same name, but space replaced by '_' and lowercased
# if a function is missing, it will be taken for granted this is a sub menu item. 


menu_list = {
    "1": 'Generate Rooster',
    "2": 'Attendance',
    "2.1": 'Abscent',
    "2.2": 'Present',
    "q": 'Quit',
}

# menu_list = {"1": 'Transaction',
#             "1.1": 'Show All',
#             "1.2": 'Edit',
#             "1.2.1": 'Edit Header',
#             "1.2.2": 'Edit Line',
#             "1.2.b": 'Back',
#             "1.3": 'Create',
#             "1.3.1": 'Create From File',
#             "1.3.2": 'Create Manually',
#             "1.3.b": 'Back',
#             "1.4": 'Delete',
#             "1.b": 'Back',
#             "2": 'Import File',
#             "3": 'Import Folder',
#             "4": 'Edit Line',
#             "4.1": 'Search By Number',
#             "4.2": 'Save',
#             "4.b": 'Back',
#             "5": 'Remove Line',
#             "5.1": 'Search By Number',
#             "5.b": 'Back',
#             "q": 'Quit',
#             }

class Menu:
    """Display the menu and respond to choices when run."""
    def __init__(self, menu_list):

        self.menu_list = menu_list
        self.choices = {}

        sub_choices_key = []
        self.choices['0'] = {} # Dict containing the definition of sub menus

        for index, key in enumerate(self.menu_list.keys()):
            # print(sub_choices_key)
            # Create a dict with parent key and items. For the menu actions
            if len(key.split('.')) > len(list(self.menu_list.keys())[index-1].split('.')): # If level increased, we have a level to add
                sub_choices_key.append(list(self.menu_list.keys())[index-1])
            elif len(key.split('.')) < len(list(self.menu_list.keys())[index-1].split('.')):
                sub_choices_key.pop(-1)



            if '.' in key: # Leave the sub level action for sub level menu
                parent, selection = key.rsplit('.', 1)
                # print(key.rsplit('.', 1))

                if not self.choices.get(parent): # or not isinstance(self.choices[parent].get(parent), dict):
                    self.choices[parent] = {}

                parent_actions = ''

                for key2 in sub_choices_key:
                    if parent_actions != '':
                        parent_actions = parent_actions + self.menu_list.get(key2).lower().replace(' ', '_') + '_'
                    else:
                        parent_actions = self.menu_list.get(key2).lower().replace(' ', '_') + '_'

                self.choices[parent][selection] = parent_actions + self.menu_list.get(key).lower().replace(' ', '_')

            else: 
                action_name = self.menu_list.get(key).lower().replace(' ', '_')
                # self.choices['0'][key] = self + '.' + action_name
                self.choices['0'][key] = action_name
                # sub_choices_key.append(key)
            # print(self.choices)

                

    def display_menu(self, parent_filter='0'):
        # Display menu, either base or from a parent
        print('')

        if parent_filter == '0':
            for key in self.menu_list:
                if '.' in key:
                    continue
                print(key, self.menu_list[key])

        else: 
            for key in [key for key in self.menu_list if '.' in key]:
                parent, child = key.rsplit('.', 1)
                if parent_filter == parent:
                    print(child, self.menu_list[key])

    def call_me(self, name, arg=None):
        if arg == None:
            return getattr(self, name)()

    

    def run(self,):
        """Display the menu and respond to choices."""
        self.parent_menu = '0' # Main menu
        while True:
            self.display_menu(parent_filter=self.parent_menu)
            # print(self.choices)
            choice = input("Enter an option: ")


            action = self.choices[self.parent_menu].get(choice)


            # if choice in self.choices[self.parent_menu].keys(): # if user choose a sub-menu
            #     self.parent_menu = choice # Set as parent_filter and proceed to next loop
            #     print('Sub menu selected %s' %self.parent_menu)
            #     continue

            if action:
                print(action)
                multi_getattr(obj=self, attr=action, )







            else:
                print("{0} is not a valid choice".format(choice))

# menu_list = {"1": 'Transaction',
#             "1.1": 'Show All',
#             "1.2": 'Edit',
#             "1.2.1": 'Edit Header',
#             "1.2.2": 'Edit Line',
#             "1.2.b": 'Back',
#             "1.3": 'Create',
#             "1.3.1": 'Create From File',
#             "1.3.2": 'Create Manually',
#             "1.3.b": 'Back',
#             "1.4": 'Delete',
#             "1.b": 'Back',
#             "2": 'Import File',
#             "3": 'Import Folder',
#             "4": 'Edit Line',
#             "4.1": 'Search By Number',
#             "4.2": 'Save',
#             "4.b": 'Back',
#             "5": 'Remove Line',
#             "5.1": 'Search By Number',
#             "5.b": 'Back',
#             "q": 'Quit',
#             }

    # This demo line should be created automatically
    def transaction(self):
        self.parent_menu = '1'


    def transaction_show_all(self, transactions=None):
        print('ok')
        models.show_transactions(transactions=transactions)
    
    def transaction_edit(self, transaction=None):
        self.parent_menu = '1.2'
        if transaction is not None:
            choosen_result = transaction
        else:
            transaction_id = input('What transaction id are you looking for? >>')
            results = models.search_transaction(transaction_id=int(transaction_id))
            choosen_result = models.check_results(results)
        self.active_transaction_id = choosen_result.transaction_id
        choosen_result.print_transaction_terminal()



    def transaction_edit_edit_header(self, **kwargs):
        models.show_transactions(models.search_transaction(transaction_id=int(self.active_transaction_id)))
        print('Edit Header')

    def transaction_edit_edit_line(self, transaction_id):
        print('Edit Line')

    def transaction_edit_back(self):
        self.parent_menu = '1'
        print('Edit Back')

    def transaction_create(self):
        self.parent_menu = '1.3'
        print('create transaction')



    def transaction_create_create_from_file(self):
        models.menu_create_from_file()


    def transaction_create_create_manually(self):
        new_transaction = models.add_transaction()
        self.parent_menu = '1.2'
        self.transaction_edit(new_transaction)


    def transaction_create_back(self):
        self.parent_menu = '1'

    def transaction_delete(self):
        print('transaction delete')

    def transaction_back(self):

        self.parent_menu = '0'

    def import_file(self):
        filename = input('Enter filename to be imported >>')
        dataframe1 = app.import_disnat_file(filename)
        self.save_data(dataframe1)
        print(self.dataframe)
        

    def import_folder(self):
        print('import folder')
        pass

    def edit_line(self):
        print('editing line')

    def edit_line_search_by_number(self):
        print('search by number on line edit')

    def edit_line_save(self):
        print('line saved on edit line')

    def edit_line_back(self):
        print('going back from edit line')
        self.menu_level = "0"

    def remove_line(self):
        print('remove line')

    def remove_line_search_by_number(self):
        print('search by number on remove line')

    def remove_line_back(self):
        print('back from remove line')
        self.menu_level = "0"

    def quit(self):
        sys.exit('exitting, thank you!')

       


def multi_getattr(obj, attr, default = None):
        """
        Get a named attribute from an object; multi_getattr(x, 'a.b.c.d') is
        equivalent to x.a.b.c.d. When a default argument is given, it is
        returned when any attribute in the chain doesn't exist; without
        it, an exception is raised when a missing attribute is encountered.

        """
        attributes = attr.split(".")
        for i in attributes:
            try:
                obj = getattr(obj, i)
            except AttributeError:
                if default:
                    return default
                else:
                    raise
        return obj()