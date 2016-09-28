#!/usr/bin/env python2
"""User representation"""

###

class User:
    """Representation of each game player"""

    def __init__(self, user_id, user_name):
        self.id = user_id
        self.name = user_name

    def __eq__(self, other):
        """Override: only the user.id need be compared"""

        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return True

    def __ne__(self, other):
        """Override: only the user.id need be compared"""

        return not self.__eq__(other)

