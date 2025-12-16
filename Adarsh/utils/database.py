# MongoDB DISABLED (Temporary)

class Database:
    async def add_user(self, id):
        return True

    async def add_user_pass(self, id, ag_pass):
        return True

    async def get_user_pass(self, id):
        return None

    async def is_user_exist(self, id):
        return False

    async def total_users_count(self):
        return 0

    async def get_all_users(self):
        return []

    async def delete_user(self, user_id):
        return True

db = Database()
