import frappe
from frappe.utils import money_in_words
def profit_taxes(doc, method):
    for a in doc.items:
        a.total_profit = float(a.rate) - float(a.item_buying_rate)
        profit_record = frappe.db.sql(""" select rate from `tabSales Taxes and Charges` where parent=%s """,(a.profit_taxes_template),as_dict=True)
        total = 0
        for p in profit_record:
            total += p.rate
        a.profit_tax_rate = total
        a.profit_tax_amount = (a.total_profit / 100) * a.profit_tax_rate
    total_pro = 0
    profit = 0
    for data in doc.items:
        if data.enable_profit_tax == 1:
            total_pro += data.profit_tax_amount
            profit += data.total_profit
    doc.total_taxes_on_profit = total_pro
    if doc.total_taxes_on_profit > 0:
        doc.grand_total  = doc.grand_total + doc.total_taxes_on_profit
        doc.rounded_total = round(doc.grand_total)
        doc.in_words = money_in_words(doc.rounded_total)
    # doc.total_profit = profit
def validate(doc, method):
    for it in doc.items:
        if it.profit_tax_rate > 0 and it.total_profit > 0:
            it.profit_tax_rate = 0
            it.total_profit = float(it.rate) - float(it.item_buying_rate)
            profit_record = frappe.db.sql(""" select rate from `tabSales Taxes and Charges` where parent=%s """,(it.profit_taxes_template),as_dict=True)
            total = 0
            for p in profit_record:
                total += p.rate
            it.profit_tax_rate = total
            it.profit_tax_amount = (it.total_profit / 100) * it.profit_tax_rate
    total_pro = 0
    profit = 0
    for data in doc.items:
        if data.profit_tax_amount:
            if data.enable_profit_tax == 1:
                total_pro += data.profit_tax_amount
                profit += data.total_profit
    doc.total_taxes_on_profit = total_pro
    if doc.total_taxes_on_profit > 0:
        doc.grand_total  = doc.grand_total + doc.total_taxes_on_profit
        doc.rounded_total = round(doc.grand_total)
        doc.in_words = money_in_words(doc.rounded_total)
    # doc.total_profit = profit