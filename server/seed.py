import pandas as pd
from .app import create_app, db
from .models import Country, Year, Indicator, IndicatorValue
import os

app = create_app()

excel_file_path = os.path.expanduser('~/Downloads/afcfta.xlsx')

def seed_data_from_excel():
    with app.app_context():
        # Load the specified sheets from the Excel file
        sheets = ['gdp', 'population']
        for sheet in sheets:
            data = pd.read_excel(excel_file_path, sheet_name=sheet)

            # Create tables if they don't exist
            db.create_all()

            # Step 1: Seed Years (2014 - 2024)
            for year in range(2014, 2025):
                if not Year.query.filter_by(year=year).first():
                    db.session.add(Year(year=year))
            db.session.commit()

            # Step 2: Seed Data for Countries, Indicators, and IndicatorValues
            for _, row in data.iterrows():
                # Get or create Country
                country_code = row["Country Code"]
                country_name = row["Country Name"]
                country = Country.query.filter_by(code=country_code).first()
                if not country:
                    country = Country(code=country_code, name=country_name)
                    db.session.add(country)
                    db.session.commit()  # Commit to get country.id
                
                # Get or create Indicator
                indicator_name = row["Indicator Name"]  # Adjust as needed
                indicator = Indicator.query.filter_by(name=indicator_name).first()
                if not indicator:
                    indicator = Indicator(name=indicator_name)
                    db.session.add(indicator)
                    db.session.commit()  # Commit to get indicator.id

                # Step 3: Seed IndicatorValues for each year (2014 - 2024)
                for year in range(2014, 2025):
                    year_entry = Year.query.filter_by(year=year).first()
                    value_column = str(year)  # Each year is a column name

                    # Ensure value exists in the column (not NaN)
                    if pd.notna(row[value_column]):
                        indicator_value = IndicatorValue.query.filter_by(
                            country_id=country.id,
                            year_id=year_entry.id,
                            indicator_id=indicator.id
                        ).first()

                        # Only insert if the combination doesn't already exist
                        if not indicator_value:
                            indicator_value = IndicatorValue(
                                value=row[value_column],
                                country_id=country.id,
                                year_id=year_entry.id,
                                indicator_id=indicator.id
                            )
                            db.session.add(indicator_value)

            # Commit all IndicatorValues for this sheet
            db.session.commit()

        print("Database seeded successfully from Excel file!")

if __name__ == "__main__":
    seed_data_from_excel()
