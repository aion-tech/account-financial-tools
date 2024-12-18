#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _autorise_lock_date_changes(self, vals):
        if self.user_has_groups(
            "account_tax_lock_group.account_tax_lock_date_group_manager",
        ):
            # Check that only the "Tax Return Lock Date" is being modified
            check_vals = vals.copy()
            lock_date_fields = [
                "period_lock_date",
                "fiscalyear_lock_date",
                "tax_lock_date",
            ]
            for lock_date_field in lock_date_fields:
                if check_vals.get(lock_date_field) == self.env.company[lock_date_field]:
                    check_vals.pop(lock_date_field)

            if set(check_vals.keys()) == {"tax_lock_date"}:
                # Only the "Tax Return Lock Date" is being modified
                # and the user can modify it.
                pass
        else:
            return super()._autorise_lock_date_changes(vals)
