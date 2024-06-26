from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    df = pd.read_csv("data_small/stations.txt", skiprows=17)
    main_df = df[["STAID", "STANAME                                 "]]
    return render_template("home.html", data = main_df[0:92])


@app.route("/api/v1/<station>/<date>")
def data(station, date):
    no_of_zero = 6 - len(station)
    station = int(station)
    df = pd.read_csv(f"data_small/TG_STAID{no_of_zero*'0'}{station}.txt", skiprows=20, parse_dates=["    DATE"])
    temp = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10

    return {"station": station,
            "temperature": temp,
            "date": date,}


@app.route("/api/v1/<station>")
def all_data(station):
    data = []
    no_of_zero = 6 - len(station)
    station = int(station)
    df1 = pd.read_csv(f"data_small/TG_STAID{no_of_zero*'0'}{station}.txt", skiprows=20, parse_dates=["    DATE"])
    df = df1[["   TG", "    DATE", "STAID"]]
    df.columns = ["date", "station", "temperature"]

    data = df.to_dict(orient="records")
    return data

@app.route("/api/v1/<station>/yearly/<year>")
def all_data_yearly(station, year):
    no_of_zero = 6 - len(station)
    station = int(station)
    df1 = pd.read_csv(f"data_small/TG_STAID{no_of_zero*'0'}{station}.txt", skiprows=20,)
    df = df1[["   TG", "    DATE", "STAID"]]
    df["    DATE"] = df["    DATE"].astype(str)
    print(df)
    wanted_df = df.loc[df["    DATE"].str.startswith(str(year))]
    wanted_df.columns = ["date", "station", "temperature"]
    print(wanted_df)
    data = wanted_df.to_dict(orient="records")
    return data


if __name__ == "__main__":
    app.run(debug=True)