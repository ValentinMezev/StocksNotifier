import yaml

CONFIG_FILE = "config/config.yaml"


class Config:
    def __init__(self):
        with open(CONFIG_FILE, 'r') as f:
            self.config = yaml.safe_load(f)
            self.validate()

    def validate(self):
        self.validate_percent_change()
        self.validate_run_in_background()
        self.validate_companies_list()
        self.validate_executed_every_hours()
        self.validate_report_for_days()

    def validate_percent_change(self):
        percent_change = self.config["percent-change"]
        if not isinstance(percent_change, int):
            raise ValueError("Percent change config prop is not int")
        if int(percent_change) <= 0 or int(percent_change) > 1000:
            raise ValueError("Percent change should be positive number between 1 and 1000")

    def validate_run_in_background(self):
        if not isinstance(self.config["run-in-background"], bool):
            raise ValueError("Run in background config prop must be bool")

    def validate_companies_list(self):
        if not isinstance(self.config["companies"], list):
            raise ValueError("Companies config prop must be list")
        if len(list(self.config["companies"])) > 100:
            raise ValueError("Max length of companies is 100")

    def validate_executed_every_hours(self):
        scheduled_in_hours = self.config["executed-every-hours"]
        if not isinstance(scheduled_in_hours, int):
            raise ValueError("Executed every hours config prop is not int")
        if int(scheduled_in_hours) <= 0 or int(scheduled_in_hours) > 168:
            raise ValueError("Executed every hours should be positive number between 1 and 168")

    def validate_report_for_days(self):
        report_for_days = self.config["report-for-days"]
        if not isinstance(report_for_days, int):
            raise ValueError("Report for days config prop is not int")
        if int(report_for_days) <= 0 or int(report_for_days) > 365:
            raise ValueError("Report for days should be positive number between 1 and 365")

    def companies(self):
        return self.config['companies']

    def percent_change(self):
        return self.config['percent-change']

    def run_in_background(self):
        return self.config['run-in-background']

    def executed_every_hours(self):
        return self.config['executed-every-hours']

    def report_for_days(self):
        return self.config['report-for-days']
