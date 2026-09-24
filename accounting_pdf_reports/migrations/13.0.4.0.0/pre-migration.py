# In 12.0 account.financial.report.sign/style_overwrite were Integer columns;
# from 13.0 they are Selection (varchar). The ORM cannot convert the column
# type itself and upgrade-util aborts on the resulting *_moved0 columns, so
# convert them in place before the module's tables are updated.


def migrate(cr, version):
    for column in ("sign", "style_overwrite"):
        cr.execute(
            """
            SELECT data_type FROM information_schema.columns
            WHERE table_name = 'account_financial_report' AND column_name = %s
            """,
            (column,),
        )
        row = cr.fetchone()
        if row and row[0] == "integer":
            cr.execute(
                'ALTER TABLE account_financial_report '
                'ALTER COLUMN "%s" TYPE varchar USING "%s"::varchar' % (column, column)
            )
