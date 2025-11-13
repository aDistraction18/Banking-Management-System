class TransactionGraph:
    def __init__(self):
        self.graph = {}  # {sender: [(receiver, amount), ...]}

    def add_transaction(self, sender, receiver, amount):
        if sender not in self.graph:
            self.graph[sender] = []
        self.graph[sender].append((receiver, amount))

    def show_graph(self):
        print("📊 Transaction History Graph:")
        for sender in self.graph:
            for receiver, amount in self.graph[sender]:
                print(f"{sender} ➝ {receiver} : ₹{amount}")

    def get_user_transactions(self, user):
        if user not in self.graph:
            print(f"No transactions found for {user}.")
            return
        print(f"Transactions by {user}:")
        for receiver, amount in self.graph[user]:
            print(f"  ➝ {receiver} : ₹{amount}")

    def get_all_users(self):
        return list(self.graph.keys())

    def detect_cycles(self):
        visited = set()
        stack = set()

        def dfs(user):
            visited.add(user)
            stack.add(user)
            for neighbor, _ in self.graph.get(user, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in stack:
                    return True
            stack.remove(user)
            return False

        for user in self.graph:
            if user not in visited:
                if dfs(user):
                    return True
        return False
