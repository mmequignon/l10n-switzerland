
-- Remap account_tax (account_id and refund_account_id)
-- with corresponding company account

WITH aa AS (SELECT id, code, company_id FROM account_account)
UPDATE
	account_tax acct
SET
	account_id = (SELECT aa2.id FROM aa aa2 WHERE aa2.code = aa.code AND aa2.company_id = acct.company_id)
FROM aa 
WHERE
	acct.account_id = aa.id AND acct.company_id != aa.company_id;

WITH aa AS (SELECT id, code, company_id FROM account_account)
UPDATE
	account_tax acct
SET
	refund_account_id = (SELECT aa2.id FROM aa aa2 WHERE aa2.code = aa.code AND aa2.company_id = acct.company_id)
FROM aa 
WHERE
	acct.refund_account_id = aa.id AND acct.company_id != aa.company_id;