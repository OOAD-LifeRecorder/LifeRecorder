from kivy.lang import Builder
from libs.kivymd_package import *
from kivy.properties import ObjectProperty

from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.pickers import MDDatePicker

import datetime
import calendar
import copy

from Screen.KV_files.ExpenseTrackerScreenKV import *
from Screen.KV_files.AddExpenseModule import *
from Screen.KV_files.AddBudgetModule import *


def get_month_range(year_, month_):
    start_date = datetime.date(year=year_, month=month_, day=1)
    last_day = calendar.monthrange(year_, month_)[1]
    end_date = datetime.date(year=year_, month=month_, day=last_day)
    return [start_date, end_date]


class Expense():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.eid = ""
        self.type = ""
        self.date = ""
        self.expense = 0
        self.name = ""

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, val):
        self.__date = val

    @property
    def expense(self):
        return self.__expense

    @expense.setter
    def expense(self, val):
        self.__expense = val

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type


class ExpenseEvent(Expense):
    def __init__(self, expense=None, **kwargs):
        super().__init__(**kwargs)
        # status:
        # 1: need to be update to list;
        # 0: nothing changed
        self.status = 0
        # edited:
        # 2: delete from db;
        # 1: update to db;
        # 0: nothing changed
        self.edited = 0
        if expense is not None:
            self.eid = expense.eid
            self.name = expense.name
            self.type = expense.type
            self.expense = expense.expense
            self.date = expense.date

    def reset(self):
        self.eid = ""
        self.name = ""
        self.type = ""
        self.expense = 0
        self.date = ""
        self.status = 0
        self.edited = 0


class Budget():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.budget = 0
        self.type = ""
        self.month = 0
        self.year = 0


class BudgetEvent(Budget):
    def __init__(self, budget=None, **kwargs):
        super().__init__(**kwargs)
        # status:
        # 1: need to be update to db;
        # 0: nothing
        self.status = 0
        if budget is not None:
            self.budget = budget.budget
            self.type = budget.type
            self.month = budget.month
            self.year = budget.year


class DatabaseEmulator(Expense, Budget):
    ExpenseDatabase = []
    BudgetDatabase = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def db_get_total_expense_by_date(self, date):
        total = 0
        for e in self.ExpenseDatabase:
            if e.date == date:
                total += e.expense
        return total

    @classmethod
    def db_delete_expense(cls, del_e):
        for e in cls.ExpenseDatabase:
            if e.eid == del_e.eid:
                cls.ExpenseDatabase.remove(e)
                break

    @classmethod
    def db_update_expense(cls, new_e):
        for e in cls.ExpenseDatabase:
            if e.eid == new_e.eid:
                e = copy.deepcopy(new_e)
                return
        cls.ExpenseDatabase.append(new_e)

    @classmethod
    def db_get_expense_by_eid(cls, eid):
        for e in cls.ExpenseDatabase:
            if e.eid == eid:
                return e

    @classmethod
    def db_get_expense_list_by_date(cls, date):
        elist = []
        for e in cls.ExpenseDatabase:
            if e.date == date:
                elist.append(e)
        return elist

    @classmethod
    def db_get_expense_list_by_date_range(cls, date_range):
        elist = []
        for e in cls.ExpenseDatabase:
            if e.date >= date_range[0] and e.date <= date_range[1]:
                elist.append(e)
        return elist

    @classmethod
    def db_print_all_expenses(cls):
        for e in cls.ExpenseDatabase:
            print(e.eid, e.name, e.date)

    @classmethod
    def db_get_budget(cls, year, month, type):
        for b in cls.BudgetDatabase:
            if b.month == month and b.year == year and b.type == type:
                return b
        return -1

    @classmethod
    def db_get_budget_list(cls, year, month):
        b_list = []
        for b in cls.BudgetDatabase:
            if b.month == month and b.year == year:
                b_list.append(b)
        return b_list

    @classmethod
    def db_set_budget(cls, budget_instance):
        b = budget_instance
        target = cls.db_get_budget(
            b.year, b.month, b.type)
        if target == -1:
            cls.BudgetDatabase.append(budget_instance)
        else:
            target = budget_instance


class ExpenseReport():
    def __init__(self, expense_list=[], **kwargs):
        super().__init__(**kwargs)
        self.expense_list = expense_list

    def get_total_expense_by_date(self, date):
        total = 0
        for e in self.expense_list:
            if e.date == date:
                total += e.expense
        return total

    def get_total_expense_by_date_range(self, date_range):
        total = 0
        for e in self.expense_list:
            if e.date >= date_range[0] and e.date <= date_range[1]:
                total += e.expense
        return total

    def get_total_expense_by_type(self, type):
        total = 0
        for e in self.expense_list:
            if e.type == type:
                total += e.expense
        return total

    def get_total_expense_by_type_and_drange(self, type, date_range):
        total = 0
        for e in self.expense_list:
            if e.type == type and e.date >= date_range[0] and e.date <= date_range[1]:
                total += e.expense
        return total

    def get_expense_each_day(self, date_range):
        total = self.get_total_expense_by_date_range(date_range)
        return round(total/(date_range[1].day-date_range[0].day+1), 3)


class BudgetReport(ExpenseReport):
    def __init__(self, budget=Budget(), expense_list=[], date=None, **kwargs):
        super().__init__(expense_list)
        self.budget_instance = budget
        self.expense_list = expense_list
        self.date = date

        start_date = datetime.date(
            self.budget_instance.year, self.budget_instance.month, 1)
        end_date = self.date
        self.total_expense = self.get_total_expense_by_date_range(
            [start_date, end_date])

    def get_surplus_by_day(self):
        total_days = calendar.monthrange(
            self.budget_instance.year, self.budget_instance.month)[1]
        return round((self.budget_instance.budget-self.total_expense)/(total_days-self.date.day), 3) or 0

    def get_surplus_by_month(self):
        return self.budget_instance.budget-self.total_expense


class SingleTypeBudgetReport(ExpenseReport):
    def __init__(self, budget=Budget(), expense_list=[], **kwargs):
        super().__init__(expense_list)
        self.budget_instance = budget
        self.expense_list = expense_list

    def get_surplus_by_type_date_range(self, date_range):
        total = self.get_total_expense_by_type_and_drange(
            self.budget_instance.type, date_range)
        return self.budget_instance.budget - total


class ExpenseTrackerScreen(MDScreen):
    # load KV should be here instaed of under __init__ to get ids
    Builder.load_string(ExpenseTrackerScreenKV)

    def __init__(self, **kwargs):
        super(ExpenseTrackerScreen, self).__init__(**kwargs)
        self.name = "Expense Tracker"
        self.add_expense_module = AddExpenseModule(current_screen=self)
        self.add_budget_module = AddBudgetModule()
        self.current_module = self.add_expense_module

        self.load_widget(mode="expense")

    def load_widget(self, mode=None):
        self.current_module.save_to_database()
        self.clear_widgets()
        if mode == "expense":
            self.current_module = self.add_expense_module
            self.add_widget(self.current_module)
            self.add_widget(DatePicker(self.current_module))
            self.add_widget(ContainerB())
            # self.box.add_widget(ToOverviewAndBudget())
        else:
            self.current_module = self.add_budget_module
            self.add_widget(self.current_module)
            self.add_widget(DateRangePicker(self.add_budget_module))
            self.add_widget(ContainerE())

        self.current_module.init()

    def clear_widgets(self):
        unwanted = [
            child for child in self.children if not isinstance(child, MDBoxLayout)]
        for w in unwanted:
            self.remove_widget(w)
        if len(self.children) > 0:
            self.children[0].clear_widgets()

    def on_leave(self):
        self.current_module.save_to_database()


class AddExpenseModule(MDGridLayout):

    Builder.load_string(AddExpenseModuleKV)

    expense_list_widget = ObjectProperty()
    current_expense = ExpenseEvent()

    def __init__(self, current_screen=None, **kwargs):
        super(AddExpenseModule, self).__init__(**kwargs)
        self.name = "AddExpenseModule"
        self.current_screen = current_screen

        self.expense_list = []
        self.old_type = ""
        self.the_list_item = ObjectProperty()
        self.last_id_no = 0
        self.cnt_list = 0
        self.budget_overview = None
        self.expense_overview = None
        self.current_expense.date = datetime.date.today()

    def init(self):
        self.clear_input()
        self.expense_list_widget.clear_widgets()
        self.create_new_item()
        self.init_expense_list()
        self.init_budget_and_expense_overview()
        self.update_total_and_budget_view()

    def init_budget_and_expense_overview(self):
        date = self.current_expense.date
        self.budget_overview = None
        budget = DatabaseEmulator.db_get_budget(date.year, date.month, 'all')
        if budget != -1:
            self.budget_overview = BudgetReport(
                budget=budget,
                expense_list=self.expense_list,
                date=date
            )

        self.expense_overview = ExpenseReport(
            expense_list=self.expense_list
        )

    def init_expense_list(self):
        date = self.current_expense.date
        tmp_list = DatabaseEmulator.db_get_expense_list_by_date(date)
        self.expense_list.clear()
        for i in range(len(tmp_list)):
            if i >= len(self.expense_list):
                self.expense_list.append(
                    copy.deepcopy(ExpenseEvent(tmp_list[i])))
            else:
                self.expense_list[i] = copy.deepcopy(tmp_list[i])

            self.add_list_item(tmp_list[i])  # Add widget to list

        if len(self.expense_list) > 0:
            self.last_id_no = int(self.expense_list[-1].eid.split('_')[1])

    def print_expense_list(self):
        for e in self.expense_list:
            print(f'{e.name}: [{e.type}] [{e.eid}] [{e.expense}]')

    def update_value(self, widget_index, the_list_item):
        self.old_type = self.current_expense.type
        expense_index = len(self.ids.expense_list_widget.children)-widget_index-1
        if len(self.expense_list) > expense_index:
            self.current_expense = self.expense_list[expense_index]

        # update to edit area
        self.ids.add.text = 'Save'

        self.set_expense_type(self.current_expense.type)

        new_amount = the_list_item.text[1:]
        self.current_expense.expense = int(new_amount)
        self.ids.expense_amount.text = new_amount

        new_name = the_list_item.secondary_text
        self.current_expense.name = new_name
        self.ids.expense_name.text = new_name

        self.the_list_item = the_list_item
        self.the_list_item.widget_index = widget_index
        self.current_expense.status = 1

    def add_list_item(self, e):
        list_item = ListExpenseItemWithIcon(
            text='$' + str(e.expense),
            secondary_text=e.name,
            current_module=self
        )
        if e.type == 'food':
            list_item.ids.the_item_icon.add_widget(
                MDFoodButton(icon_size="16sp"))
        elif e.type == 'transport':
            list_item.ids.the_item_icon.add_widget(
                MDTransportButton(icon_size="16sp"))
        elif e.type == 'housing':
            list_item.ids.the_item_icon.add_widget(
                MDHousingButton(icon_size="16sp"))
        elif e.type == 'entertainment':
            list_item.ids.the_item_icon.add_widget(
                MDEntertainmentButton(icon_size="16sp"))
        else:
            list_item.ids.the_item_icon.add_widget(
                MDOtherButton(icon_size="16sp"))

        if self.current_expense.status == 1:
            self.ids.expense_list_widget.add_widget(
                list_item, self.the_list_item.widget_index)
        else:
            self.ids.expense_list_widget.add_widget(list_item)

    def delete_list_item(self, expense_index):
        self.expense_list.remove(self.expense_list[expense_index])
        self.update_total_and_budget_view()

    def save_expense(self):
        if self.check_input_valid():
            # edited
            if self.current_expense.status == 1:
                self.current_expense.edited = 1
                self.expense_list_widget.remove_widget(self.the_list_item)

            self.add_list_item(self.current_expense)
            # add new
            if self.current_expense.status == 0:
                self.expense_list.append(self.current_expense)

            self.clear_input()
            self.init_budget_and_expense_overview()
            self.update_total_and_budget_view()

    def update_total_and_budget_view(self):
        total_expense = self.expense_overview.get_total_expense_by_date(
            self.current_expense.date)
        self.ids.total_expense.text = '$' + str(total_expense)

        if self.budget_overview is not None:
            surplus = self.budget_overview.get_surplus_by_month()
            if surplus < 0:
                self.ids.surplus_month.text = '-$ '+str(surplus)
            else:
                self.ids.surplus_month.text = '$ '+str(surplus)
            surplus = self.budget_overview.get_surplus_by_day()
            if surplus < 0:
                self.ids.surplus_day.text = '-$ '+str(surplus)
            else:
                self.ids.surplus_day.text = '$ '+str(surplus)

    def check_input_valid(self):
        # check input non-empty
        if self.ids.expense_amount.text != "" and self.ids.expense_name.text != "":
            self.current_expense.expense = int(self.ids.expense_amount.text)
            self.current_expense.name = self.ids.expense_name.text
            return True
        return False

    def create_new_item(self):
        tmp_date = self.current_expense.date
        self.current_expense = ExpenseEvent()
        self.set_expense_type("food")
        self.current_expense.edited = 1  # Mark to update db
        self.last_id_no += 1
        self.current_expense.date = tmp_date
        self.current_expense.eid = str(
            self.current_expense.date)+'_'+str(self.last_id_no)

    def clear_input(self):
        # Update view
        self.ids.expense_amount.text = ""
        self.ids.expense_name.text = ""
        if self.current_expense.type != "":
            self.ids[self.current_expense.type].line_width = 0.001
            self.ids[self.current_expense.type].line_color = "#ffffff"
        self.ids.add.text = 'Add'
        self.ids.total_expense.text = "$0"
        if hasattr(self.the_list_item, "bg_color"):
            self.the_list_item.bg_color = "#DDDDDD"

        if self.current_expense in self.expense_list:
            self.create_new_item()

    def set_expense_type(self, type):
        # Set unselected icon-color back to black
        if self.old_type != "":
            self.ids[self.old_type].line_width = 0.001
            self.ids[self.old_type].line_color = "#ffffff"
            self.old_type = ""
        elif self.current_expense.type:
            self.ids[self.current_expense.type].line_width = 0.001
            self.ids[self.current_expense.type].line_color = "#ffffff"

        # update new type
        self.current_expense.type = type
        # Set current selected icon-color to white
        self.ids[self.current_expense.type].line_width = 1.5
        self.ids[self.current_expense.type].line_color = "#43ccb1"

    def set_expense_name(self):
        self.current_expense.name = self.ids.expense_name.text

    def set_expense_amount(self):
        self.current_expense.expense = self.ids.expense_amount.text

    def set_expense_date(self, date):
        if self.current_expense.date != date:
            self.save_to_database()
            self.current_expense.date = date
            self.clear_input()
            self.expense_list_widget.clear_widgets()
            self.init_expense_list()
            self.init_budget_and_expense_overview()
            self.update_total_and_budget_view()
        self.create_new_item()

    def save_to_database(self):
        for e in self.expense_list:
            if e.edited == 1:
                DatabaseEmulator.db_update_expense(e)
            elif e.edited == 2:
                DatabaseEmulator.db_delete_expense(e)


class AddBudgetModule(MDGridLayout):

    Builder.load_string(AddBudgetModuleKV)

    current_budget = BudgetEvent()
    budget_list_widget = ObjectProperty()
    budget_amount = ObjectProperty()
    type_list = ["all", "food", "transport",
                 "housing", "entertainment", "other"]
    icon_list = ["all-inclusive", "food", "train-car",
                 "washing-machine", "teddy-bear", "shopping"]

    def __init__(self, **kwargs):
        super(AddBudgetModule, self).__init__(**kwargs)
        self.name = "AddBudgetModule"
        self.old_type = ""
        self.budget_list = []
        self.expense_list = []
        self.budget_overview = None
        self.expense_overview = None

    def init(self):
        today = datetime.date.today()
        self.current_budget.year = today.year
        self.current_budget.month = today.month
        self.date_range = get_month_range(today.year, today.month)
        self.set_date_range(self.date_range)
        self.set_budget_type("all")
        self.update_budget_overview()
        self.update_expense_overview()

    def init_budget_list(self):
        d = self.date_range[0]
        b_list = DatabaseEmulator.db_get_budget_list(d.year, d.month)

        self.budget_list = [0] * len(self.type_list)
        sorted_b_list = [0] * len(self.type_list)
        for b in b_list:
            for i in range(len(self.type_list)):
                if b.type == self.type_list[i]:
                    budget = BudgetEvent(b)
                    sorted_b_list[i] = SingleTypeBudgetReport(
                        budget=budget,
                        expense_list=self.expense_list
                    )
                    break

        for i in range(len(sorted_b_list)):
            if sorted_b_list[i] == 0:
                budget = BudgetEvent()
                budget.year = d.year
                budget.month = d.month
                budget.type = self.type_list[i]
                self.budget_list[i] = SingleTypeBudgetReport(
                    budget=budget,
                    expense_list=self.expense_list
                )
            else:
                self.budget_list[i] = sorted_b_list[i]

        for b in self.budget_list:
            self.add_list_item(b)  # Add widget to list
        self.set_budget_type('all')
        self.update_budget_overview()

    def update_budget_overview(self):
        self.budget_overview = BudgetReport(
            budget=self.current_budget,
            expense_list=self.expense_list,
            date=self.date_range[1]
        )

        str_style = self.str_style_maker(
            self.budget_overview.get_surplus_by_month())
        self.ids.surplus_month.text = str_style["dollar"]
        self.ids.surplus_month.text_color = str_style["color"]

    def update_expense_overview(self):
        self.expense_overview = ExpenseReport(
            expense_list=self.expense_list
        )
        str_style = self.str_style_maker(self.expense_overview.get_total_expense_by_date_range(
            self.date_range))
        self.ids.total_expense.text = str_style["dollar"]

        str_style = self.str_style_maker(
            self.expense_overview.get_expense_each_day(self.date_range))
        self.ids.expense_per_day.text = str_style["dollar"]
        self.ids.expense_per_day.text_color = str_style["color"]

    def type_to_icon(self, type):
        for i in range(len(self.type_list)):
            if self.type_list[i] == type:
                return self.icon_list[i]

    def str_style_maker(self, amount):
        if amount < 0:
            return {"dollar": f'-$ {abs(amount)}', "color": "red"}
        else:
            return {"dollar": f'$ {amount}', "color": "red"}

    def add_list_item(self, b):
        budget_instance = b.budget_instance
        if budget_instance.budget == 0:
            return
        else:
            stop_flag = False
            for child in self.ids.budget_list_widget.children:
                for grandchild in child.ids.the_item_icon.children:
                    if grandchild.icon == self.type_to_icon(budget_instance.type):
                        self.ids.budget_list_widget.remove_widget(child)
                        stop_flag = True
                        break
                if stop_flag:
                    break

        list_item = ListBudgetItemWithIcon(
            text='$' + str(budget_instance.budget)
        )

        type = budget_instance.type
        if type == 'all':
            list_item.ids.the_item_icon.add_widget(
                MDAllButton(icon_size="16sp"))
        elif type == 'food':
            list_item.ids.the_item_icon.add_widget(
                MDFoodButton(icon_size="16sp"))
        elif type == 'transport':
            list_item.ids.the_item_icon.add_widget(
                MDTransportButton(icon_size="16sp"))
        elif type == 'housing':
            list_item.ids.the_item_icon.add_widget(
                MDHousingButton(icon_size="16sp"))
        elif type == 'entertainment':
            list_item.ids.the_item_icon.add_widget(
                MDEntertainmentButton(icon_size="16sp"))
        else:
            list_item.ids.the_item_icon.add_widget(
                MDOtherButton(icon_size="16sp"))

        surplus = b.get_surplus_by_type_date_range(self.date_range)
        str_style = self.str_style_maker(surplus)
        if type == 'all':
            list_item.secondary_text = "Overall budget (Monthly)"
        else:
            list_item.secondary_text = "Budget Surplus: "+str_style["dollar"]
        list_item.secondary_text_color = str_style["color"]

        self.ids.budget_list_widget.add_widget(list_item)


    def get_current_budget_report(self, type):
        return next((b for b in self.budget_list if b.budget_instance.type == type), None)

    def set_show_type(self, button_index):
        self.ids.show_type_button.icon = self.icon_list[button_index]
        self.current_budget.type = self.type_list[button_index]

    def set_budget_amount(self):
        if self.budget_amount.text != "":
            self.current_budget.status = 1  # Mark to save into DB
            self.current_budget.budget = int(self.budget_amount.text)
            br = self.get_current_budget_report(self.current_budget.type)
            self.add_list_item(br)
            self.reset_input()
            self.update_budget_overview()
            self.update_expense_overview()

    def set_budget_type(self, type):
        # Set unselected icon-color back to black
        if self.old_type != "":
            self.ids[self.old_type].line_width = 0.001
            self.ids[self.old_type].line_color = "#ffffff"
            self.old_type = ""
        elif self.current_budget.type:
            self.ids[self.current_budget.type].line_width = 0.001
            self.ids[self.current_budget.type].line_color = "#ffffff"

        # update new type
        br = self.get_current_budget_report(type)
        self.current_budget = br.budget_instance
        # value checking skipped
        # Set current selected icon-color to white
        self.ids[self.current_budget.type].line_width = 1.5
        self.ids[self.current_budget.type].line_color = "#43ccb1"

    def set_date_range(self, date_range):
        self.ids.date_range.text = date_range[0].strftime(
            "%d %b, %Y") + ' ~ ' + date_range[1].strftime("%d %b, %Y")

        self.save_to_database()
        self.expense_list = DatabaseEmulator.db_get_expense_list_by_date_range(
            date_range)

        self.date_range = date_range
        self.budget_list_widget.clear_widgets()
        self.init_budget_list()
        self.update_expense_overview()
        self.reset_input()
        # self.current_budget.month = date_range[0].month

    def reset_input(self):
        self.old_type = self.current_budget.type
        self.budget_amount.text = ""
        if len(self.budget_list) > 0:
            self.current_budget = self.budget_list[0].budget_instance  # all
        self.set_budget_type("all")

    def save_to_database(self):
        for b in self.budget_list:
            if b.budget_instance.status == 1:
                DatabaseEmulator.db_set_budget(b.budget_instance)


class DatePicker(MDAnchorLayout):
    module = ObjectProperty()

    def __init__(self, module=None, **kwargs):
        super().__init__(**kwargs)
        self.module = module
        self.set_picker_text_date(self.module.current_expense.date)

    def show_date_picker(self):
        date_dialog = MDDatePicker(
            year=self.module.current_expense.date.year,
            month=self.module.current_expense.date.month,
            day=self.module.current_expense.date.day
        )
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.module.set_expense_date(value)
        self.set_picker_text_date(value)

    def set_picker_text_date(self, date):
        if date == datetime.date.today():
            self.ids.picked_date.text = "Today"
        else:
            self.ids.picked_date.text = date.strftime("%d %b, %Y")


class DateRangePicker(MDAnchorLayout):

    def __init__(self, module=None, **kwargs):
        super().__init__(**kwargs)
        self.module = module
        self.set_picker_text_date_range(datetime.date.today())

    def show_date_picker(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        if len(date_range) == 0:
            return
        self.set_picker_text_date_range(date_range[0])
        first_and_last_day = [date_range[0], date_range[len(date_range)-1]]
        self.module.set_date_range(first_and_last_day)

    def set_picker_text_date_range(self, date):
        if date.month == datetime.date.today().month:
            self.ids.picked_date_range.text = "This Month"
        else:
            self.ids.picked_date_range.text = date.strftime(
                "%b, %Y")
