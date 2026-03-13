# customers_orders table
# customer_id, order_id, order_date, order_amount,
#
# revenue (total order amount per customer)
# revenue = valoarea vanzarilor totale
# find repeat customers in the last 30 days , ranking them by revenue

'''
SELECT *
FROM customers_orders
WHERE order_date >= DATE('now', '-30 day');
'''




#last 30 days
#cati clienti au plasat mai mlt de 1 comanda
#