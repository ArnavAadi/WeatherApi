from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def data(station, date):
    temperature = "25"
    no_of_zero = 6 - len(station)
    station = int(station)
    df = pd.read_csv(f"data_small/TG_STAID{no_of_zero*'0'}{station}.txt", skiprows=20, parse_dates=["    DATE"])
    temp = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temp}


if __name__ == "__main__":
    app.run(debug=True)