.. :changelog:

.. Template:

.. 0.0.1 (2016-05-09)
.. ++++++++++++++++++

.. **Features and Improvements**

.. **Bugfixes**

.. **Build**

.. **Documentation**

Release History
---------------

latest (unreleased)
+++++++++++++++++++

**Features and Improvements**

**Bugfixes**

* Script to modify salary structure BIZ-1225

**Build**

**Documentation**


10.12.1 (2018-01-29)
++++++++++++++++++++

**Features and Improvements**

* Moved and fixed in 10.12.2


10.12.0 (2018-01-24)
++++++++++++++++++++

**Features and Improvements**

* BIZ-1145: Clients Melioris AG, Melioris SA, Association Gamer Event layout non-conforme
* BIZ-843: Re: Odoo VAT 2018
* BIZ-1112: Congés des employees visible dans toutes les sociétés


10.11.0 (2018-01-19)
++++++++++++++++++++

**Features and Improvements**

* Install module web_environment_ribbon

**Bugfixes**

* BIZ-1067: Define a default paperformat when company is created
* BIZ-1120: Hide employee menu to employee
* BIZ-1108: Remap account_tax with correct company account_account

**Build**

* Update odoo-cloud-platform (BIZ-1093)

**Documentation**


10.10.0 (2017-12-19)
++++++++++++++++++++

**Features and Improvements**

* BIZ-987: in wizard hr.payroll.config group name LCA to IJM
* BIZ-987: add LAANP field on wizard
* BIZ-987: in Cantonal rules add amat_ge_per "Assurance maternité"


10.9.0 (2017-12-07)
+++++++++++++++++++

**Features and Improvements**

* Update project from odoo-template
* BIZ-827: Installation du module Rappel v2
* BIZ-854: Payroll setup on every company

**Build**

* Upgrade Dockerimage to 10.0-2.4.1


10.8.0 (2017-11-23)
+++++++++++++++++++

**Features and Improvements**

* Installing addons:
  - crm
  - survey
* BIZ-827 Install module account_credit_control
* Add default company on pricelist BIZ-791
* BIZ-812: Update account_payment_order with new bugfix
* Remove access to Settings from non 'Main' company users
* BIZ-840 Problème de sécurité dans le reporting des salaires
* BIZ-607: Add smtp configuration for production
* BIZ-805 Fwd: Salaires Enfin!

**Bugfixes**

**Build**

**Documentation**


10.7.1 (2017-10-04)
+++++++++++++++++++

**Features and Improvements**

* Update invoice report to use company partner's language + correct display of sale address


10.7.0 (2017-09-21)
+++++++++++++++++++

**Features and Improvements**

* Add Reliure des Planches and Reliure des Planches SARL companies

**Bugfixes**

* BSFIN-78: Fix payslip report (fix sorting of payslip lines)

**Build**

**Documentation**


10.6.5 (2017-08-30)
+++++++++++++++++++

**Features and Improvements**
* Improve invoice layout (BIZ-188)

**Bugfixes**
* Fix Incoming mail configuration

10.6.4 (2017-08-15)
+++++++++++++++++++

**Features and Improvements**

**Bugfixes**

* FIX faulty tab in XML definition for salary BIZ-328
* FIX missing payroll and hr contract permission BIZ-348


**Build**

**Documentation**

10.6.3 (2017-07-03)
+++++++++++++++++++

**Features and Improvements**

* Add new company Davia Conseil
* Change report header + set paper format on all companies
* Add payment user right to all users + new user right

**Bugfixes**

**Build**

**Documentation**


10.6.2 (2017-06-15)
+++++++++++++++++++

**Features and Improvements**

* Correct journal type and account type


10.6.1 (2017-06-13)
+++++++++++++++++++

**Bugfixes**

* Fix Internal Server Error on login by updating module l10n_ch_hr_payroll


10.6.0 (2017-06-13)
+++++++++++++++++++

**Features and Improvements**

* BSFIN-70: configurations for incoming mails for integration and production environments
* BSFIN-72: added external repository OCA/hr
            installed module hr_public_holidays
            installed module hr_holidays_compute_days
            checked function get_remaining_leaves

**Bugfixes**

* BSFIN-21: Bank account missing when salary registered in accounting

**Build**

* Update docker image to 10.0-2.2.0
* Load entrypoints
* Update cloud platform addons to be able to use Redis Sentinel
* Update Odoo sources to latest commit
* Remove pending-merge on OCA/server-tools


10.5.1 (2017-05-10)
+++++++++++++++++++

**Bugfixes**

* Fix failing product template product import


10.5.0 (2017-05-10)
+++++++++++++++++++

**Features and Improvements**

* BSFIN-9: Standardization of companies setup
* Update salary imputation for main company
* BSFIN-16: Create DTA Payment Mode for the salaries
* BSFIN-17: Leave management on the salary payslip
* BSFIN-18: Hide discuss and calendar menu
            Only enfinfidu users can see project and task specific additions
            Display menu entry for journal entries for accountants
            Hide powered by and db manager link on login page
            Hide powered by in menu
* BSFIN-19: Load products for Expenses from csv
* BSFIN-69 change-report-header
* Add icons on project buttons
* BSFIN-15: Set default value on the contract and payslip batch
* BSFIN-14: Update salary rules and structure
* BSFIN-24: Remove sharing of partners and products in multi-company

10.4.1 (2017-05-08)
+++++++++++++++++++

**Bugfixes**

* Upgrade base image
  Fixes security vulnerability CVE-2017-8291


10.4.0 (2017-04-11)
+++++++++++++++++++

**Features and Improvements**

* BSFIN-10: Do not diplay payslip line with a zero total in payslip report
* BSFIN-12: Add a specific module to custom payroll structure
* BSFIN-13: Fix custom payslip report after OCA review


10.3.0 (2017-04-06)
+++++++++++++++++++

**Features and Improvements**

* BSFIN-2: Custom project management
* Install modules account_asset and hr_timesheet


10.2.0 (2017-03-22)
+++++++++++++++++++

**Features and Improvements**

* Rename enfin_custom module to specific_fct module
* BSFIN-3: Custom payslip report
* BSFIN-4: New payslip yearly report
* BSFIN-6: Add songs for base and accounting configuration

**Build**

* Update all repositories
* Fix nginx version for test environment
* Add PRs (for xxx_environment modules in v10) for server-tools repository
* Add PR for l10n_ch_hr_payroll migration V10


10.1.0 (2017-02-28)
+++++++++++++++++++

**Build**

* Initial build
