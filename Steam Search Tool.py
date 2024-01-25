#####################################################
#               Computer Project #8
#   a Python program that makes use of steam data and 
#   answer user search queries by finding
#   appropriate games from the database.
#####################################################
import csv
from datetime import datetime
from operator import itemgetter


MENU = '''\nSelect from the option: 
        1.Games in a certain year 
        2. Games by a Developer 
        3. Games of a Genre 
        4. Games by a developer in a year 
        5. Games of a Genre with no discount 
        6. Games by a developer with discount 
        7. Exit 
        Option: '''
        
      
        
def open_file(s):

    ''' This function prompts the user to input a csv file name to open and keeps prompting until a
    correct name is entered. The parameter s is a string to incorporate into your prompt 
    so you are prompting the user for a particular type of file ( "games" , "discount" ). '''

    file_name = input('\nEnter {} file: '.format(s))
    file_found = False
    while file_found == False:
        try:
            fp = open(file_name, "r", encoding="utf-8")
            file_found = True
        #if file name not found print error message
        except FileNotFoundError:
            print('\nNo Such file')
            file_name = input('\nEnter {} file: '.format(s))
            continue
    return fp
            


def read_file(fp_games):

    ''' This function uses the provided file pointer and reads the games data file.'''

    reader = csv.reader(fp_games)
    next(reader)
    #intialize an empty dictionary
    game_data = {}

    for row in reader:
        # extract the data from the file
        name = row[0]
        release_date = row[1]
        developer = row[2].split(';')
        genres =  row[3].split(';')
        player_modes = row[4].split(';')[0].lower()
        if 'multi-player' in player_modes:
            mode = 0
        else:
            mode = 1
        price = row[5].replace(',', '')
        try:
            price = float(price)*0.012
        except ValueError:
            price = 0.0
        overall_reviews = row[6]
        reviews = int(row[7])
        percent_positive = int(row[8].replace('%', ''))
        win_support = row[9]
        mac_support = row[10]
        lin_support = row[11]
        support = []
        # if the game is supported on the platform add the platform to the support list
        if win_support == '1':
            support.append("win_support")
        if mac_support == '1':
            support.append("mac_support")
        if lin_support == '1':
            support.append("lin_support")
        
        #add the information to the dictionary
        game_data[name] = [release_date,developer,genres, mode, price, overall_reviews, reviews,percent_positive, support]

    return game_data


def read_discount(fp_discount):

    ''' The function would read the discount file and create a dictionary with key as the name of the game
        and value as the discount as a float rounded to 2 decimals.'''

    reader = csv.reader(fp_discount)
    next(reader)
    # initalize an empty dictionary
    discount_data = {}

    for row in reader:
        name = row[0]
        #make the discount string into a float rounded to two digits
        discount = round(float(row[1]), 2)
        discount_data[name] = discount

    return discount_data
    
def in_year(master_D,year):

    ''' This function filters out games that were released in a specific year from the main dictionary you have
        created in the read_file function (master_D).'''

    filtered_games = []

    for game, game_details in master_D.items():

        date_str = game_details[0]
        # extract the year from the release date string
        day, month,year_str = date_str.split('/')
        game_year = int(year_str)
        #if the game is released in the specified year add it to the filtered list
        if game_year == year:
            filtered_games.append(game)

    return sorted(filtered_games)


def by_genre(master_D,genre):

    ''' This function filters out games that are of a specific genre from the main 
    dictionary you have created in the read_file function (master_D).'''

    filtered_games = []
    for game, game_details in master_D.items():

        if genre in game_details[2]:
            filtered_games.append(game)

    sorted_games = sorted(filtered_games, key=lambda x: (-master_D[x][7], filtered_games.index(x)))

    return sorted_games

        
def by_dev(master_D,developer): 

    ''' This function filters out games that are made by a specific developer from the main dictionary you
    have created in the read_file function (master_D). It creates a list of game names sorted from
    latest to oldest released games.'''

    filtered_games = []

    for game, game_details in master_D.items():
        # if the developer matches the users desired developer add it to the filtered list
        if developer in game_details[1]:
            filtered_games.append(game)
            
    # sorts the filtered list by release year from latest to oldest
    sorted_games = sorted(filtered_games, key=lambda x: (datetime.strptime(master_D[x][0], '%d/%m/%Y').year), reverse=True)

    return sorted_games

def per_discount(master_D,games,discount_D): 

    ''' This function accepts as an argument the main dictionary you have created in the read_file function
    (master_D), a list of games (games), and the discount dictionary that you created in the
    read_discount function (discount_D). The function calculates and returns a list of the
    discounted price for each game in the list of games rounded to 6 decimal digits'''

    discounted_prices = []

    for game in games:

        if game in discount_D:

            discount_percentage = discount_D[game]
            original_price = float(master_D[game][4])
            discounted_price = round((1 - discount_percentage/100) * original_price, 6)
            discounted_prices.append(discounted_price)

        else:
            discounted_prices.append(float(master_D[game][4]))

    return discounted_prices


def by_dev_year(master_D,discount_D,developer,year):

    ''' This function filters out games by a specific developer and released in a specific year. It returns a
        list of game names sorted in increasing prices. '''

    game_list = []

    for game, details in master_D.items():

        if developer in details[1] and int(details[0].split('/')[2]) == year:
            price = details[4]

            if game in discount_D:
                discount = discount_D[game]
                price = price * (100 - discount) / 100

            game_list.append((game, price))

    game_list.sort(key=lambda x: (x[1], x[0]))
    return [game[0] for game in game_list]

          
def by_genre_no_disc(master_D, discount_D, genre):

    ''' This function filters out games by a specific genre that do not offer a discount on their price. It returns
        a list of game names sorted from cheapest to most expensive.'''

    filtered_games = by_genre(master_D, genre)
    games_with_discount = set(discount_D.keys())

    # Filter out games that have a discount
    filtered_games = [game for game in filtered_games if game not in games_with_discount]

    # Sort by price and percentage positive reviews in ascending order
    filtered_games = sorted(filtered_games, key=lambda game: (master_D[game][4], -master_D[game][7]), reverse=False)

    return filtered_games



def by_dev_with_disc(master_D, discount_D, developer):

    '''This function filters out games by a specific developer and offers discounts. The function should
    return a list of game names sorted from cheapest to most expensive.  '''

    filtered_games = by_dev(master_D, developer)
    games_with_discount = set(discount_D.keys())

    # Filter out games that do not have a discount
    filtered_games = [game for game in filtered_games if game in games_with_discount]

    # Sort by original price, release date, and game name in ascending order
    filtered_games = sorted(filtered_games, key=lambda game: (master_D[game][4], master_D[game][0], game), reverse=False)

    return filtered_games

def get_option():

    menu_option = input(MENU)
    if menu_option in ['1','2','3','4','5','6','7']:
        return menu_option    
    else:
        print("\nInvalid option")

             
def main():

    game_fp = open_file("games")
    discount_fp = open_file("discount")

    games_list = read_file(game_fp)
    discount_list = read_discount(discount_fp)

    # calls the helper function to display the menu and recieve user option
    menu_option = get_option()
    
    while menu_option != '7':
        
        if menu_option == '1':

            year = input("\nWhich year: ")
            year_valid = False

            while year_valid == False:
                try:
                    year = int(year)
                    year_valid = True

                except:
                    print("\nPlease enter a valid year")
                    year = input('\nWhich year: ')

            released_games = in_year(games_list, year)
            if released_games == []:
                print("\nNothing to print")
            else:
                print("\nGames released in {}:".format(year))
                print(', '.join(released_games))

        if menu_option == '2':

            developer = input('\nWhich developer: ')
            dev_list = by_dev(games_list, developer)

            if dev_list == []:
                print("\nNothing to print")
            else:
                print("\nGames made by {}:".format(developer))
                print(', '.join(dev_list))

        if menu_option == '3':

            genre = input('\nWhich genre: ')
            genre_list = by_genre(games_list, genre)
            
            if genre_list == []:
                print("\nNothing to print")
            else:
                print("\nGames with {} genre:".format(genre))
                print(', '.join(genre_list))
        
        if menu_option == '4':

            developer = input('\nWhich developer: ')
            year =  input('\nWhich year: ')
            year_valid = False

            while year_valid == False:

                try:
                    year = int(year)
                    year_valid = True
                except:
                    print("\nPlease enter a valid year")
                    year = input('\nWhich year: ')

            filtered_list = by_dev_year(games_list,discount_list,developer,year)
            if filtered_list == []:
                print("\nNothing to print")
            else:
                print("\nGames made by {} and released in {}:".format(developer,year))
                print(', '.join(filtered_list))

        if menu_option == '5':

            genre = input('\nWhich genre: ')

            filtered_list = by_genre_no_disc(games_list,discount_list,genre)
            if filtered_list == []:
                print("\nNothing to print")
            else:
                print("\nGames with {} genre and without a discount:".format(genre))
                print(", ".join(filtered_list))
        
        if menu_option == '6':

            developer = input('\nWhich developer: ')
            filtered_list = by_dev_with_disc(games_list,discount_list,developer)
            if filtered_list == []:
                print("\nNothing to print")
            else:
                print("\nGames made by {} which offer discount:".format(developer))
                print(', '.join(filtered_list))
        menu_option = get_option()

    # if option 7 is chosen it breaks the loops and prints the thank you message
    print("\nThank you.")

if __name__ == "__main__":
    main()