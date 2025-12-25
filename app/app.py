from flask import Flask, render_template, request
import pandas as pd
import functions
import plotly.io as pio

app = Flask(__name__)

# Load the CSV file with area data
area_csv_path = r"/Users/zainnofal/Projects/Chicago Police/app/chicago_areas_avg_coords.csv"
areas_df = pd.read_csv(area_csv_path)

# Load the crime data
crime_data_path = r"/Users/zainnofal/Projects/Chicago Police/app/final_dataset.csv"
crime_df = pd.read_csv(crime_data_path)


@app.route("/", methods=["GET", "POST"])
def index():
    plot_html_1 = None
    plot_html_2 = None
    plot_html_3 = None
    error_message = None

    if request.method == "POST":
        try:
            # Retrieve the area name from the form
            area_name = request.form["area_name"].strip()

            # Find the corresponding latitude and longitude (case-insensitive search)
            matching_area = areas_df[areas_df["Area"].str.lower(
            ) == area_name.lower()]

            if matching_area.empty:
                raise ValueError("Invalid area name entered.")

            # Extract latitude and longitude
            latitude = matching_area.iloc[0]["Latitude"]
            longitude = matching_area.iloc[0]["Longitude"]

            # Filter crimes based on the neighborhood
            filtered_crimes = functions.calculate_neighborhood(
                crime_df, longitude=longitude, latitude=latitude, radius_km=1
            )

            # Generate the plots
            fig1 = functions.plot_combined_charts(filtered_crimes, top_n=5)
            plot_html_1 = pio.to_html(fig1, full_html=False)

            fig2 = functions.plot_crimes_by_month_and_year(filtered_crimes)
            plot_html_2 = pio.to_html(fig2, full_html=False)

            fig3 = functions.plot_crimes_by_arrest_status(filtered_crimes)
            plot_html_3 = pio.to_html(fig3, full_html=False)

        except ValueError as e:
            error_message = "Choose again: " + str(e)

    return render_template(
        "index.html",
        plot_html_1=plot_html_1,
        plot_html_2=plot_html_2,
        plot_html_3=plot_html_3,
        error_message=error_message
    )


if __name__ == "__main__":
    app.run(debug=True)
