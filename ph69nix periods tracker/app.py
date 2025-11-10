from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# store period start dates in memory (for now)
period_dates = []

@app.route("/", methods=["GET", "POST"])
def index():
    global period_dates
    message = None
    next_period = None

    if request.method == "POST":
        date_str = request.form.get("period_date")
        if date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            period_dates.append(date_obj)

    # Sort dates and compute average cycle length
    if len(period_dates) >= 2:
        period_dates = sorted(period_dates)
        gaps = [
            (period_dates[i] - period_dates[i-1]).days
            for i in range(1, len(period_dates))
        ]
        avg_cycle = round(sum(gaps) / len(gaps))
        next_period = period_dates[-1] + timedelta(days=avg_cycle)
        message = f"Average cycle length: {avg_cycle} days. Next period: {next_period.date()}"
    elif len(period_dates) == 1:
        message = "Add one more date to calculate your cycle."

    return render_template("index.html", dates=period_dates, message=message)
    

if __name__== "__main__":
    app.run(debug=True)