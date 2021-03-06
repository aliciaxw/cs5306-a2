import csv
import matplotlib.pyplot as plt
from datetime import datetime

def main():
    print("Creating dataset...")

    # global dataset for analysis
    ds = create_dataset('steam_games.csv', 'steam_reviews.csv')
    # print(ds['Dead by Daylight'])

    print("Plotting graphs...")
    plot_review_quantity(ds)
    plot_review_length(ds)
    plot_review_popularity(ds)
    plot_review_recommended(ds)


def create_dataset(game_path, review_path):
    """
    Returns a data structure representing the combined Steam game and review data.
    Will skip any games that do not have reviews associated with them in the datasets.

    Example:
    {
        "Fallout 4": {
            num_owners: int representing midpoint of number bin
            average_playtime: int
            median_playtime: int
            price: float
            days_since_release: int
            reviews: [
                {
                    funny: int
                    helpful: int
                    hours_played: int
                    is_recommended: boolean
                    length: int (number of characters in description)
                }
            ]
        }
    }
    """

    with open(game_path) as game_csv, open(review_path) as review_csv:
        game_reader = csv.DictReader(game_csv)
        review_reader = csv.DictReader(review_csv)
        data = {}

        for row in game_reader:
            game_dict = {}
            owners = row["owners"].split("-")
            avg_owners = (int(owners[0]) + int(owners[1])) / 2  # take the midpoint of the bin
            game_dict["owners"] = avg_owners
            game_dict["average_playtime"] = int(row["average_playtime"])
            game_dict["median_playtime"] = int(row["median_playtime"])
            game_dict["price"] = float(row["price"])
            release_date = datetime.strptime(row["release_date"], '%Y-%m-%d')
            curr_date = datetime.strptime('2019-06-12', '%Y-%m-%d')
            game_dict["days_since_release"] = (curr_date-release_date).days
            game_dict["reviews"] = []
            data[row["name"]] = game_dict

        for row in review_reader:
            if row['title'] in data:
                reviews = data[row["title"]]['reviews']
                review = {}
                review["funny"] = int(row["funny"])
                review["helpful"] = int(row["helpful"])
                review["hours_played"] = int(row["hour_played"])
                review["is_recommended"] = row["recommendation"] == "Recommended"
                review["length"] = len(row["review"])
                reviews.append(review)
                data[row["title"]]['reviews'] = reviews

        return { title:value for (title, value) in data.items() if value['reviews'] != [] }

def plot_review_quantity(dataset):
    """
    x - number of reviews per game
    y - number of players
    """
    x = [len(game['reviews']) for game in dataset.values()]
    pass

def plot_review_length(dataset):
    """
    x - average length of helpful reviews per game
    y - number of players
    """
    pass

def plot_review_popularity(dataset):
    """
    Will have two trend lines: one for funny / helpful reviews.

    x - average number of react_type (funny, helpful) per game
    y - number of players
    """
    pass

def plot_review_recommended(dataset):
    """
    x - average proportion of recommended to not recommended reviews per game 
    y - number of players
    """
    pass


if __name__ == "__main__":
    main()
