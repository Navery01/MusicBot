import mysql.connector as mysql
from mysql.connector import errorcode

from MusicBot.configs import CONFIG

class DBService:
    def __init__(self):
        pass

    def create_table(self, table_name, columns):
        conn = mysql.connect(**CONFIG['mysql'])
        cursor = conn.cursor(buffered=True)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
        cursor.close()
        conn.commit()
        conn.close()

    def add_user(self, guild_id, user_id, user_name):
        conn = mysql.connect(**CONFIG['mysql'])
        cursor = conn.cursor(buffered=True)
        try:
            if self.get_user(guild_id, user_id):
                print('[SQL] User already exists')
                return
            else:
                cursor.execute("INSERT INTO users (user_id, user_name, guild_id) VALUES (%s, %s, %s);", (user_id, user_name, guild_id))
                print('[SQL] User added')
        except mysql.Error as err:
            if err.errno == errorcode.ER_NO_SUCH_TABLE:
                print(f"Error: Table 'users' does not exist.")
                self.create_table('users', 'user_id BIGINT, user_name VARCHAR(64), guild_id BIGINT, load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            else:
                print(err.msg)
        cursor.close()
        conn.commit()
        conn.close()

    def get_user(self, guild_id, user_id):
        conn = mysql.connect(**CONFIG['mysql'])
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s AND guild_id = %s;", (user_id, guild_id))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    
    def add_guild(self, guild_id, guild_name):
        conn = mysql.connect(**CONFIG['mysql'])
        cursor = conn.cursor(buffered=True)
        try:
            if self.get_guild(guild_id):
                print('[SQL] Guild already exists')
                return
            else:
                cursor.execute("INSERT INTO guilds (guild_id, guild_name) VALUES (%s, %s);", (guild_id, guild_name))
                print('[SQL] Guild added')
        except mysql.Error as err:
            if err.errno == errorcode.ER_NO_SUCH_TABLE:
                print(f"Error: Table 'guilds' does not exist.")
                self.create_table('guilds', 'guild_id BIGINT, guild_name VARCHAR(64), load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            else:
                print(err.msg)
        cursor.close()
        conn.commit()
        conn.close()
    
    def get_guild(self, guild_id):
        conn = mysql.connect(**CONFIG['mysql'])
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM guilds WHERE guild_id = %s;", (guild_id,))
        guild = cursor.fetchone()
        cursor.close()
        conn.close()
        return guild
    
    def init_points(self, guild_id, user_id):
        conn = mysql.connect(**CONFIG['mysql'])
        cursor = conn.cursor(buffered=True)
        cursor.execute("INSERT INTO points (user_id, guild_id, points) VALUES (%s, %s, 100);", (user_id, guild_id))
        print('[SQL] Points added')
        cursor.close()
        conn.commit()
        conn.close()

    def add_points(self, guild_id, user_id, points):
        conn = mysql.connect(**CONFIG['mysql'])
        cursor = conn.cursor(buffered=True)
        try:
            if self.get_points(guild_id, user_id):
                cursor.execute("UPDATE points SET points = points + %s WHERE user_id = %s AND guild_id = %s;", (points, user_id, guild_id))
                print('[SQL] Points updated')
            else:
                self.init_points(guild_id, user_id)
                cursor.execute("UPDATE points SET points = points + %s WHERE user_id = %s AND guild_id = %s;", (points, user_id, guild_id))
                print('[SQL] Points updated')
        except mysql.Error as err:
            if err.errno == errorcode.ER_NO_SUCH_TABLE:
                print(f"Error: Table 'points' does not exist.")
                self.create_table('points', 'user_id BIGINT, guild_id BIGINT, points INT, load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            else:
                print(err.msg)
        cursor.close()
        conn.commit()
        conn.close()
    
    def get_points(self, guild_id, user_id):
        conn = mysql.connect(**CONFIG['mysql'])
        cursor = conn.cursor(buffered=True)
        try:
            print('[SQL] Getting points')
            cursor.execute("SELECT points FROM points WHERE user_id = %s AND guild_id = %s;", (user_id, guild_id))
            points = cursor.fetchone()
            if not points:
                print('[SQL] No points found')
                print('[SQL] Initializing points')
                self.init_points(guild_id, user_id)
                return 100
        except mysql.Error as err:
            print(err.msg)
            return None
        cursor.close()
        conn.close()
        return points[0]
    
    def update_points(self, guild_id, user_id, points):
        num_pts = self.get_points(guild_id, user_id)
        if num_pts < points:
            return
        
        conn = mysql.connect(**CONFIG['mysql'])
        cursor = conn.cursor(buffered=True)
        print('[SQL] Updating points')
        cursor.execute("UPDATE points SET points = points + %s WHERE user_id = %s AND guild_id = %s;", (points, user_id, guild_id))
        print('[SQL] Points updated')
        cursor.close()
        conn.commit()
        conn.close()
        return True

if __name__ == '__main__':
    db = DBService()
    # print(db.add_points(1335302010374848623, 183987232359579650, 100))