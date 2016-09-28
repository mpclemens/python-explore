#!/usr/bin/env python2
"""Channel representation"""

###

class Channel:
    """Representation of each channel where a game is played"""

    def __init__(self, team_id, channel_id):
        self.team_id    = team_id
        self.channel_id = channel_id

        
    def __eq__(self, other):
        # Could compare __dict__ entries, but this is more explicit
        if isinstance(other, self.__class__):
            return self.team_id == other.team_id and self.channel_id == other.channel_id
        else:
            return False
