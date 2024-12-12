#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo.exceptions import UserError
from odoo.tests import new_test_user

from odoo.addons.base.tests.common import BaseCommon


class TestUpdateLockDates(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_xmlid = "account_tax_lock_group.account_tax_lock_date_group_manager"

        cls.company = cls.env.company
        cls.company.tax_lock_date = date(2020, month=1, day=1)

        cls.restricted_user = new_test_user(
            cls.env,
            login="Restricted user",
        )
        cls.unrestricted_user = new_test_user(
            cls.env,
            login="Unrestricted user",
            groups=f"{cls.group_xmlid},base.group_erp_manager",
        )

    def test_empty_restricted_tax_lock_date(self):
        """If a user is not in group, they cannot update the Tax Return Lock Date."""
        # Arrange
        group_xmlid = self.group_xmlid
        company = self.env.company
        restricted_user = self.restricted_user
        # pre-condition
        self.assertTrue(company.tax_lock_date)
        self.assertFalse(restricted_user.has_group(group_xmlid))

        # Act
        with self.assertRaises(UserError) as ue:
            company.with_user(restricted_user).tax_lock_date = False

        # Assert
        exc_message = ue.exception.args[0]
        self.assertIn("date is irreversible", exc_message)

    def test_empty_unrestricted_tax_lock_date(self):
        """If a user is in group, they can update the Tax Return Lock Date."""
        # Arrange
        group_xmlid = self.group_xmlid
        company = self.env.company
        unrestricted_user = self.unrestricted_user
        # pre-condition
        self.assertTrue(company.tax_lock_date)
        self.assertTrue(unrestricted_user.has_group(group_xmlid))

        # Act
        company.with_user(unrestricted_user).tax_lock_date = False

        # Assert
        self.assertFalse(company.tax_lock_date)
