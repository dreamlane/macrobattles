## decisionhandlers.py Holds all handlers for decision API calls.

class TownspersonHireHandler():
    """Handles TownspersionHire calls."""
    test = False

    @staticmethod
    def test():
        test = True
        return "TESTED"
