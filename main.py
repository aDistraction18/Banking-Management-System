from transaction_graph import TransactionGraph

tg = TransactionGraph()


tg.add_transaction("A", "B", 500)
tg.add_transaction("A", "C", 300)
tg.add_transaction("C", "A", 200)

tg.show_graph()
tg.get_user_transactions("A")


if tg.detect_cycles():
    print("⚠️  Circular transaction cycle detected!")
else:
    print("✅ No cycles in transactions.")
