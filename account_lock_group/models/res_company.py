#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _autorise_lock_date_changes(self, *args, **kwargs):
        if not self.user_has_groups(
            "account_lock_group.account_lock_dates_group_manager"
        ):
            return super()._autorise_lock_date_changes(*args, **kwargs)
