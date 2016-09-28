#!/usr/bin/env python2
"""Test cases for User class"""

import unittest

from User2    import User

###

class Test_User(unittest.TestCase):

    ### ID IS ALL THAT MATTERS
    ###
    ###
    def test_id_comparisons(self):

        # * Two User instances exist with string ids and names

        USER_1 = User(user_id = "ABC123", user_name = "XYZ098")
        USER_2 = User(user_id = "ABC123", user_name = "XYZ098")

        # * They should compare the same

        self.assertTrue(USER_1 == USER_2, "They should be the same 1")
        
        # * Even when one username changes, they are the same

        USER_2.name = "foo"
        self.assertTrue(USER_1 == USER_2, "They should be the same 2")
        
        # * Even when both usernames differ, they are the same

        USER_1.name = None
        self.assertTrue(USER_1 == USER_2, "They should be the same 3")

        # * But when the usernames match and ids do not, they differ

        USER_1.name = USER_2.name = "NEW_NAME"
        USER_2.id = USER_1.id + "ABC"
        self.assertTrue(USER_1 != USER_2, "They should differ 1")

        # * None ids don't match, either (an unlikely case, though)
        
        USER_2.id = None
        self.assertTrue(USER_1 != USER_2, "They should differ 2")

        # * But if both are None (unlikely!) they are the same

        USER_1.id = None
        self.assertTrue(USER_1 == USER_2, "They should be the same 4")

        
#

if __name__ == '__main__':
    unittest.main()
