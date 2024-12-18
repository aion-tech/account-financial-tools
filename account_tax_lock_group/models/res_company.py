#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _autorise_lock_date_changes(self, vals):
        if set(vals.keys()) == {"tax_lock_date"} and self.user_has_groups(
            "account_tax_lock_group.account_tax_lock_date_group_manager",
        ):
            # Only the "Tax Return Lock Date" is being modified
            # and the user can modify it.
            pass
        else:
            return super()._autorise_lock_date_changes(vals)
