'''
Description: This is the main program to interact with \
the 'Heinz Career Outcome Application.'

'''

#import the utilities as menu options
import HeinzReport as option1
import careerReport as option2
import CPI as option3

def main():
    #coding the menu option
    choice = 0
    while choice != 4:
        print('Please input 1, 2, or 3 to choose one of the options below.')
        print('\nMENU')
        print('Option 1: Display past employers who hired a Heinz student specific to a job title.')
        print('Option 2: Display a career outcome report for a job title.')
        print('Option 3: Convert cost of living between two cities in the U.S.')
        print('Option 4: Quit the program')
        choice = input('\nWhat do you want to do? ')
        print('\n')
        try: #prevent str input
            choice = int(choice)
        except ValueError:
            print('Invalid input. Please only enter 1, 2, 3, or 4.\n')
            choice = 0
            continue
        else:
            if choice not in (1,2,3,4): #prevent digit input that is not a menu option
                print('Invalid input. Please only enter 1, 2, 3, or 4.\n')
                choice = 0
                continue
            else: #run respective .py file for choice
                if choice == 1:
                    option1.main()
                    print('-'*50+ '\n')
                    continue
                if choice == 2:
                    option2.main()
                    print('-'*50+ '\n')
                    continue
                if choice == 3:
                    option3.main()
                    print('-'*50+ '\n')
                    continue

if __name__ == '__main__':
    main()