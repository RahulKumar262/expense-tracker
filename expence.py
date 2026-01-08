import calendar
import datetime


class Expense:

    def __init__(self, name, amount ,category):
     self.name= name
     self.amount= amount
     self.category=category 

    def __repr__(self):
        return f"Expense:{self.name} {self.category} {self.amount:.2f}"

def main():
   
    expense=expense_money()                     # call expense function
    expense_file_path="expense.csv"

    budget=200000

    file_save(expense, expense_file_path)

    summarise_expenses(expense_file_path,budget)    

 # how much spend money 
    
def expense_money():                           
    print(" : HOW MUCH YOU SPEND MONEY : ")

    expense_name=input(": WHERE YOU SPEND MONEY  : ")
    expense_amount=float(input(": HOW MUCH YOU PAY : "))

    print(f"expense name is {expense_name},\n spend money is {expense_amount}")

    expense_category=[
        
        " food",
        " home",
        " work",
        " shopping",
        " fun"
        ]
    
    while True:
        print(" :  ON WHICH CATEGORY YOU SPEND MONEY :  ")               # FOR HEADING

        for i , category_name in enumerate(expense_category):
             print(f"{i+1}. {category_name}")
        
        value_range=f"[1-{len(expense_category)}]"
        select_idx=int(input(f" which category you want :: {value_range} "))-1
        

        if select_idx in range(len(expense_category)):
            select_category=expense_category[select_idx]
            print(select_category)


            new_expense=Expense(name=expense_name, category=select_category, amount=expense_amount)
            return new_expense
        else:

            print(" invalid category")
            
        break
 
def file_save(expense :Expense ,expense_file_path):                 # save money you spend
     
     print("SAVE how much you spend : {expense} to {expense_file_path}")
     with open(expense_file_path,"a") as f:
         f.write(f"{expense.name}  ,  {expense.amount}  ,  {expense.category}\n")


def summarise_expenses(expense_file_path,budget):           # how much left money

    print(" SUMMARY OF USER EXPENSES :")

    expenses =[]                                     # create list
    with open(expense_file_path,'r') as f:
        lines =f.readlines()
        for line in lines:
            #print(line)
            expense_name ,expense_amount ,expense_category =line.strip().split(",")
            print(f"{expense_name} {expense_amount} {expense_category}")
            line_expense=Expense(name=expense_name,  amount=float(expense_amount), category=expense_category)
            #print(line_expense)

            expenses.append(line_expense)
            #print(expenses)

    amount_by_category = {}
    for expense in expenses:
       key=expense.category

    if key in amount_by_category:
        amount_by_category[key] += expense_amount 
    else:
        amount_by_category[key] = expense_amount
     
    print(": YOU CAN SEE WHERE YOU SPEND MONEY :")

    for key , amount in amount_by_category.items():
        print(f"{key} : {amount}")
         
    
    total_spent = sum([x.amount for x in expenses])
    print(f"TOTAL AMOUNT YOU SPEND : {total_spent:.2f}")

    remaining_budget=budget-(total_spent)
    print(f"REMAINING BUDGET: {remaining_budget:.2f}")


    now=datetime.datetime.now()
    days_in_month=calendar.monthrange(now.year,now.month)[1]
    remaining_days=days_in_month - now.day
    print(" : REMAINING DAYS IN A MONTH : ",remaining_days)
    

    daily_budget = remaining_budget/remaining_days
    print(" : DAILY BUDGET : ",daily_budget)

if __name__=="__main__":
   main()
     