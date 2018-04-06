-- Update XMLIDs of CSV imported taxes and tags with wrong
-- module name and nopupdate flag
UPDATE
    ir_model_data
SET
    module = '__setup__',
    noupdate = TRUE
WHERE
    module IN ('l10n_ch', 'enfinfidu_account')
AND
    model = 'account.tax';

-- Delete duplicate xlmid on account tax template
DELETE FROM
    ir_model_data
WHERE
    model = 'account.tax.template'
AND
    name LIKE '%tax_tmp_%'
AND
    res_id IN (
        SELECT
            res_id
        FROM
            ir_model_data
        WHERE
            model = 'account.tax.template'
        AND
            module = 'l10n_ch'
    );

-- Update account tax template xmlid
-- to avoid to recreate new xmlids with update of src repository
UPDATE
    ir_model_data
SET
    module = 'l10n_ch',
    name = REPLACE(name,'tax_tmp_','')
WHERE
    module = 'enfinfidu_account'
AND
    model = 'account.tax.template';

-- Update account account tag xmlid
-- to avoid to recreate new xmlids with update of src repository
UPDATE
    ir_model_data
SET
    name = 'vat_tag_302_a'
WHERE
    name = 'vat_tag_302'
AND
    model = 'account.account.tag';
UPDATE
    ir_model_data
SET
    name = 'vat_tag_302_b'
WHERE
    name = 'vat_tag_302b'
AND
    model = 'account.account.tag';
UPDATE
    ir_model_data
SET
    name = 'vat_tag_342_a'
WHERE
    name = 'vat_tag_342'
AND
    model = 'account.account.tag';
UPDATE
    ir_model_data
SET
    name = 'vat_tag_342_b'
WHERE
    name = 'vat_tag_342b'
AND
    model = 'account.account.tag';
