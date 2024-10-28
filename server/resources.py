from flask_restful import Resource
from flask import jsonify
from .models import db, Country, Indicator, Year, IndicatorValue

class IndicatorResource(Resource):
    def get(self, indicator_name):
        # Query for the indicator by name
        indicator = Indicator.query.filter_by(name=indicator_name).first()

        if not indicator:
            return {"message": "Indicator not found"}, 404

        # Retrieve all related countries and their indicator values for the specified indicator
        results = []
        countries = Country.query.all()

        for country in countries:
            # Retrieve all indicator values for the country and indicator
            indicator_values = (
                db.session.query(Year.year, IndicatorValue.value)
                .join(IndicatorValue, Year.id == IndicatorValue.year_id)
                .filter(
                    IndicatorValue.country_id == country.id,
                    IndicatorValue.indicator_id == indicator.id
                )
                .order_by(Year.year)
                .all()
            )

            # Format the years and values into a dictionary
            year_values = {str(year): value for year, value in indicator_values}

            # Append the country's data to the results list
            results.append({
                "id": country.id,
                "country": country.code,
                "country_name": country.name,
                "indicator": indicator.name,
                "indicator_value": year_values
            })

        return jsonify(results)
