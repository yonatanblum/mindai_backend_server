from typing import Dict, Any


class PeriodConverter:
    """
    Converts and formats periods between different representations (days, hours, string formats).
    """

    ALLOWED_PERIODS = ["day", "week", "twoWeek", "threeWeek", "month"]

    # Mapping from days to period names
    DAYS_MAPPING = {
        1: "day",
        7: "week",
        14: "twoWeek",
        21: "threeWeek",
        30: "month",
    }

    # Reverse mapping from period names to days
    PERIOD_TO_DAYS_MAPPING = {v: k for k, v in DAYS_MAPPING.items()}

    # Hours to period mapping
    HOURS_MAPPING = {
        24: "day",
        168: "week",  # 7 days
        336: "twoWeek",  # 14 days
        504: "threeWeek",  # 21 days
        720: "month",  # 30 days
    }

    @staticmethod
    def convert_to_period(value) -> str:
        """
        Converts a given input (integer days or string period) into a valid period option.
        If the value is not recognized, defaults to "week".
        """
        if isinstance(value, int):  # Handle integer (days) input
            return PeriodConverter.DAYS_MAPPING.get(value, "week")  # Default to "week"

        if isinstance(value, str) and value in PeriodConverter.ALLOWED_PERIODS:
            return value  # Return as is if valid

        return "week"  # Default if input is invalid

    @staticmethod
    def convert_to_days(value) -> int:
        """
        Converts a valid period name into its corresponding number of days.
        If the value is not recognized, defaults to 7 (week).
        """
        if isinstance(value, str) and value in PeriodConverter.PERIOD_TO_DAYS_MAPPING:
            return PeriodConverter.PERIOD_TO_DAYS_MAPPING[
                value
            ]  # Convert period to days

        if isinstance(value, int) and value in PeriodConverter.DAYS_MAPPING:
            return value  # If it's already an integer and valid, return as is

        return 7  # Default to "week" (7 days) if invalid input

    @staticmethod
    def extract_period_from_params(params: Dict[str, Any]) -> str:
        """
        Extracts the period value from params. The function checks for:
        - "days" key (int) → Converts days into a valid period string.
        - "period" key (str) → Returns if valid.
        - Defaults to "week" if neither is provided.

        Returns:
            str: The extracted period as a string (e.g., "week", "twoWeek").
        """
        if "days" in params and isinstance(params["days"], int):
            return PeriodConverter.convert_to_period(
                params["days"]
            )  # Convert days to period string

        if "period" in params and isinstance(params["period"], str):
            return PeriodConverter.convert_to_period(
                params["period"]
            )  # Validate and return period

        return "week"  # Default to "week" if no valid period is found

    @staticmethod
    def format_period_text(hours: int) -> str:
        """
        Convert period in hours to a readable format.

        Args:
            hours (int): Period in hours

        Returns:
            str: Formatted period string
        """
        # Check if the hours match a standard period
        if hours in PeriodConverter.HOURS_MAPPING:
            return PeriodConverter.HOURS_MAPPING[hours]

        # For custom periods, return the number of hours/days
        if hours < 24:
            return f"{hours} hours"
        else:
            days = hours // 24
            return f"{days} days"
