import numpy
from matplotlib import pyplot as plt
import csv
from collections import OrderedDict
import arrow
from datetime import timedelta
from matplotlib import lines

boroughs = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

colors = dict([
    *zip(
        boroughs,
        plt.rcParams['axes.prop_cycle'].by_key()['color']
    ), (None, "grey")
]) 

if __name__ == "__main__":

    data_by_zcta = {}
    data_by_neighborhood = {}

    with open("data/NYC-github-coronavirus-data-tests-by-zcta.csv") as fp:
        reader = csv.DictReader(fp)
        dates = [arrow.get(key) for key in reader.fieldnames if key.startswith("2020-")]
        for row in reader:
            if row["zip_code"] not in data_by_zcta.keys():
                data_by_zcta[row["zip_code"]] = {}
            data_by_zcta[row["zip_code"]][row["status"]] = OrderedDict(
                (key, val)
                for (key, val) in row.items()
                if key.startswith("2020-")
            )
            for key in row.keys():
                if not key.startswith("2020-"):
                    data_by_zcta[row["zip_code"]][key] = row[key]

    for zip_code, zip_data in data_by_zcta.items():
        if "uhf_code" not in zip_data.keys():
            continue
        uhf_code = zip_data["uhf_code"]
        if uhf_code not in data_by_neighborhood.keys():
            data_by_neighborhood[uhf_code] = {}
            for status in ["Total", "Positive"]:
                if status not in data_by_neighborhood[uhf_code].keys():
                    data_by_neighborhood[uhf_code][status] = numpy.zeros(len(dates))
                data_by_neighborhood[uhf_code][status] += numpy.array([float(x) for x in zip_data[status].values()])

            for key in zip_data.keys():
                if key not in ["Total", "Positive"]:
                    data_by_neighborhood[uhf_code][key] = zip_data[key]
    
    print(data_by_neighborhood)

    plt.figure()

    date_diff = numpy.diff(dates) / timedelta(days=1)
    # date_diff = date_diff / date_diff[0].

    for uhf_code, uhf_data in data_by_neighborhood.items():
        if uhf_code == "": continue
        x_array = numpy.diff(uhf_data["Total"]) / date_diff
        y_array = numpy.diff(uhf_data["Positive"]) / date_diff
        if max(y_array) > 1000:
            print(uhf_code)

        plt.plot(x_array, y_array, marker="o", c=colors[uhf_data["borough"]], alpha=.8, ls="dashed", markersize=1, lw=.75)
        plt.plot(x_array[-1], y_array[-1], marker="o", c=colors[uhf_data["borough"]], markersize=6, mec="white", zorder=10)
        if int(uhf_code) % 2 == 1 and y_array[-1] / x_array[-1] > .5:
            plt.text(
                x_array[-1], y_array[-1],
                "     " + uhf_data["neighborhood_name"] + f" ({int(y_array[-1])}/{int(x_array[-1])})",
                color=colors[uhf_data["borough"]],
                va="bottom", ha="right",
                size=6, alpha=.9,
                rotation=-45,
                zorder=15
            )
        else:
            plt.text(
                x_array[-1], y_array[-1],
                uhf_data["neighborhood_name"] + f" ({int(y_array[-1])}/{int(x_array[-1])})" + "     ",
                color=colors[uhf_data["borough"]],
                va="top", ha="left",
                size=6, alpha=.9,
                weight="bold",
                rotation=-45,
                zorder=15
            )


    plt.loglog()

    plt.xlabel("Daily tested for COVID-19")
    plt.ylabel("Daily positive for COVID-19")

    plt.legend([
        lines.Line2D([], [], c=color, marker="o")
        for color in colors.values()
    ], boroughs)
    plt.gca().set_aspect("equal")
    plt.xlim(left=5)
    plt.ylim(bottom=5)
    for percent in numpy.arange(0, 1.1, .25):
        plt.plot(plt.xlim(), numpy.array(plt.xlim()) * percent, c="grey", lw=.5, ls="dotted")
        if percent == 1: continue
        plt.text(plt.xlim()[1], plt.xlim()[1]*percent, f"  {percent*100:.0f}%", ha="left", va="bottom", c="k", rotation=45)
        
    plt.text(plt.ylim()[1], plt.ylim()[1], f"  100%", ha="left", va="bottom", c="k", rotation=45)

    plt.text(plt.xlim()[0] * 1.1, plt.ylim()[0] * 1.28, "daily positive rate $\\uparrow$", rotation=45, size=8)

    from matplotlib.ticker import LogLocator
    from util import LogFormatterSI

    plt.gca().xaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
    plt.gca().xaxis.set_major_formatter(LogFormatterSI(labelOnlyBase=False, minor_thresholds=(numpy.inf, numpy.inf)))
    plt.gca().yaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
    plt.gca().yaxis.set_major_formatter(LogFormatterSI(labelOnlyBase=False, minor_thresholds=(numpy.inf, numpy.inf)))

    plt.savefig("plots/NYC-districts-positive.png")


    #for neighboor, data in data_by_zcta.items():
        
        #plot(, c=[])