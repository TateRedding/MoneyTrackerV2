class Transaction:
    def __init__(self, id, amount, description, date, account_id, phrase_id):
        self.id = id
        self.amount = amount
        self.description = description
        self.date = date
        self.account_id = account_id
        self.phrase_id = phrase_id
