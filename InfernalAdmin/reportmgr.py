class ReportSessionMgr:
    """Used to manage interactions with reporting,
    allows for opening and closing interactive sessions

    Anything said in a report channel should be recorded as comments for the report
    This class attaches to the main bot and will check if any
    """

    def __init__(self, bot):
        self.sessions = {}
        self.bot = bot

    def get_report_from_channel(self, channel):
        """returns whether or not a channel is a report channel
         will return report id """
        pass

    def open_session(self, report_id, ctx):
        pass

    def close_session(self, report_id, ctx):
        pass

    def generate_sessions(self, channels):
        """Used on bot startup will check for any open report channels and start sessions on them"""
        pass
