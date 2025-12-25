import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def calculate_neighborhood(df, longitude, latitude, radius_km):
    lon_rad = np.radians(longitude)
    lat_rad = np.radians(latitude)
    df["Latitude_rad"] = np.radians(df["Latitude"])
    df["Longitude_rad"] = np.radians(df["Longitude"])
    df["distance_km"] = 6371 * (
        2 * np.arcsin(
            np.sqrt(
                np.sin((df["Latitude_rad"] - lat_rad) / 2) ** 2
                + np.cos(lat_rad) * np.cos(df["Latitude_rad"]) *
                np.sin((df["Longitude_rad"] - lon_rad) / 2) ** 2
            )
        )
    )
    filtered_df = df[df["distance_km"] <= radius_km]
    filtered_df = filtered_df.drop(
        columns=["Latitude_rad", "Longitude_rad",
                 "distance_km", "Latitude", "Longitude"]
    )
    return filtered_df


def plot_combined_charts(df, top_n=5):
    # Data for Top Crime Types
    crime_type_count = df['Primary Type'].value_counts().reset_index()
    crime_type_count.columns = ['Primary Type', 'count']

    # Data for Arrest Distribution
    arrest_distribution = df[df['Arrest']].groupby(
        'Primary Type').size().reset_index(name='Arrest_Count')
    arrest_distribution = arrest_distribution.sort_values(
        by='Arrest_Count', ascending=False)

    # Create subplots with 1 row and 2 columns
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f"Top {top_n} Most Common Crime Types",
                        f"Top {top_n} Crime Types by Arrest Count")
    )

    # Bar chart for Top Crime Types
    fig.add_trace(
        go.Bar(
            x=crime_type_count.head(top_n)['count'],
            y=crime_type_count.head(top_n)['Primary Type'],
            orientation='h',
            name='Top Crime Types',
            marker=dict(color='blue')
        ),
        row=1, col=1
    )

    # Bar chart for Arrest Distribution
    fig.add_trace(
        go.Bar(
            x=arrest_distribution.head(top_n)['Arrest_Count'],
            y=arrest_distribution.head(top_n)['Primary Type'],
            orientation='h',
            name='Top Arrest Distribution',
            marker=dict(color='green')
        ),
        row=1, col=2
    )

    # Update layout for the subplots
    fig.update_layout(
        height=700,  # Increased height
        width=1400,  # Increased width
        title_text="Crime Analysis Dashboard",
        title_x=0.5,  # Center the title
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),  # Add padding
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
    )

    # Update x-axis and y-axis labels
    fig.update_xaxes(title_text="Count", row=1, col=1)
    fig.update_xaxes(title_text="Arrest Count", row=1, col=2)
    fig.update_yaxes(title_text="Primary Type", row=1, col=1)
    fig.update_yaxes(title_text="Primary Type", row=1, col=2)

    return fig


def plot_crimes_by_month_and_year(df):
    crimes_by_month = df['Month'].value_counts().reset_index()
    crimes_by_month.columns = ['Month', 'count']
    crimes_by_month = crimes_by_month.sort_values(by='Month')

    crimes_by_year = df['Year'].value_counts().reset_index()
    crimes_by_year.columns = ['Year', 'count']
    crimes_by_year = crimes_by_year.sort_values(by='Year')

    # Create subplots with 1 row and 2 columns
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Number of Crimes by Month",
                        "Number of Crimes by Year")
    )

    # Bar chart for Crimes by Month
    fig.add_trace(
        go.Bar(
            x=crimes_by_month['Month'],
            y=crimes_by_month['count'],
            marker_color='blue',
            name="Crimes by Month"
        ),
        row=1, col=1
    )

    # Bar chart for Crimes by Year
    fig.add_trace(
        go.Bar(
            x=crimes_by_year['Year'],
            y=crimes_by_year['count'],
            marker_color='green',
            name="Crimes by Year"
        ),
        row=1, col=2
    )

    # Update layout for the subplots
    fig.update_layout(
        height=700,  # Increased height
        width=1400,  # Increased width
        title_text="Crime Analysis: Monthly and Yearly Trends",
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),  # Add padding
    )

    # Update x-axis for month plot
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        title_text="Month",
        row=1, col=1
    )

    # Update x-axis for year plot
    fig.update_xaxes(
        title_text="Year",
        row=1, col=2
    )

    # Update y-axis labels
    fig.update_yaxes(title_text="Crime Count", row=1, col=1)
    fig.update_yaxes(title_text="Crime Count", row=1, col=2)

    return fig


def plot_crimes_by_arrest_status(df):
    """
    Create a centered subplot with:
    1. Bar chart for crimes with and without arrests.
    2. Line chart for crimes with arrests over the years.
    """
    # Calculate total crimes and arrested crimes
    total_crimes = len(df)
    arrested_crimes = df[df["Arrest"] == True].shape[0]
    no_arrested_crimes = total_crimes - arrested_crimes

    # Data for Bar Chart: Arrest Percentage
    arrest_data = {
        "Type": ["With Arrest", "Without Arrest"],
        "Count": [arrested_crimes, no_arrested_crimes]
    }
    arrest_df = pd.DataFrame(arrest_data)

    # Crimes with Arrests by Year
    crimes_arrested_by_year = df[df["Arrest"] == True].groupby(
        "Year").size().reset_index(name="count")

    # Create subplots with 1 row and 2 columns
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Crimes with and without Arrests",
                        "Crimes with Arrests by Year")
    )

    # Bar chart: Arrest Percentage
    fig.add_trace(
        go.Bar(
            x=arrest_df["Type"],
            y=arrest_df["Count"],
            marker_color=["green", "red"],
            name="Arrest Status"
        ),
        row=1, col=1
    )

    # Line chart: Crimes with Arrests by Year
    fig.add_trace(
        go.Scatter(
            x=crimes_arrested_by_year["Year"],
            y=crimes_arrested_by_year["count"],
            mode="lines+markers",
            marker=dict(size=8, color="blue"),
            line=dict(width=2, color="blue"),
            name="Arrests by Year"
        ),
        row=1, col=2
    )

    # Update layout
    fig.update_layout(
        height=700,  # Increased height
        width=1400,  # Increased width
        title_text="Crime Analysis: Arrest Trends",
        title_x=0.5,  # Center the title
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),  # Add padding
    )

    # Update axis labels
    fig.update_xaxes(title_text="Arrest Type", row=1, col=1)
    fig.update_xaxes(title_text="Year", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Crimes with Arrests", row=1, col=2)

    return fig
