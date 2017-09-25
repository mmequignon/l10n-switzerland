
-- Remove noupdate flag from l10n_ch_hr_payroll module
-- Because noupdate flag have been removed in the data file

UPDATE ir_model_data
SET noupdate = false
WHERE module = 'l10n_ch_hr_payroll'
AND model = 'hr.salary.rule.category';
