# Importing the required libraries
import matplotlib.pyplot as plt
import json
import pandas as pd
import matplotlib.dates as mdates

fig = plt.figure()
fig = plt.figure(figsize=(11, 8.5))

# Opening JSON file
with open('data.json') as json_file:
    count = json.load(json_file)

    for category in count:
        fig.clear()
        dic = sorted(count[category].items())
        dates = []
        values = []
        for indice in dic:
            dates.append(indice[0])
            values.append(indice[1])
        dates = pd.to_datetime(dates)

        plt.title(category)
        plt.xlabel("Date")
        plt.ylabel("Tweet Count")

        DF = pd.DataFrame()
        DF['value'] = values
        DF = DF.set_index(dates)
        plt.plot(DF)
        
        # Set major ticks to be at the start of each month
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        # Set minor ticks to be at each day
        plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
        
        plt.gcf().autofmt_xdate()
        fig.savefig("img/" + category + ".png", dpi=fig.dpi, bbox_inches='tight', pad_inches=0.3)
