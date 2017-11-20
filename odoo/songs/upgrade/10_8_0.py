# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def change_users_rights(ctx):
    """Remove ability to see Settings menu from users not in 'Main' company"""
    settings_group = ctx.env.ref('base.group_system')
    access_rights_group = ctx.env.ref('base.group_erp_manager')
    main_company = ctx.env.ref('base.main_company')

    ctx.env.cr.execute("""
        DELETE
        FROM res_groups_users_rel gur
        WHERE EXISTS(
            SELECT *
            FROM res_users u
            WHERE u.id = gur.uid AND gur.gid in %s and u.company_id <> %s
        );
    """, ((settings_group.id, access_rights_group.id), main_company.id))

    group_menu_discuss = ctx.env.ref('enfinfidu_security.group_menu_discuss')
    group_menu_calendar = ctx.env.ref('enfinfidu_security.group_menu_calendar')
    group_menu_settings = ctx.env.ref('enfinfidu_security.group_menu_settings')

    group_menu_discuss.users = main_company.user_ids
    group_menu_calendar.users = main_company.user_ids
    group_menu_settings.users = main_company.user_ids


@anthem.log
def main(ctx):
    """ Main 10.8.0 """
    change_users_rights(ctx)
