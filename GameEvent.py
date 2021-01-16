class GameEvent:

    def __init__(self, m_id, idx, author, time, min_players):
        self.author = author
        self.m_id = m_id
        self.id = idx
        self.time = time
        self.valid = True
        self.min = min_players
        self.users = set()
        self.numbers = self.update_numbers()

    def cancel(self, user, override=False):
        if self.author == user or override:
            self.valid = False
            return True
        return False
    
    def add_user(self, user):
        self.users.add(user)
        self.update_numbers()

    def remove_user(self, user):
        self.users.remove(user)
        self.update_numbers()

    def update_numbers(self):
        self.numbers = len(self.users)

    def get_users(self):
        return self.users

    def enough_people(self):
        print(self.numbers, self.min)
        return self.numbers >= self.min
