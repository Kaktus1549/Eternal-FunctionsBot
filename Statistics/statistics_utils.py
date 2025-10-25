# def user_stats(user):
#     # -1 means that there was an error while connecting to the database
#     # -2 means that user is not found in stats

#     # Search for user in database
#     try:
#         connection = pool.get_connection()
#         cursor = connection.cursor()
#         if is_steamid(user) == 0:
#             # Removes @steam from steamid
#             user = user[:-6]
#             cursor.execute(f"SELECT * FROM {settings['leader_settings']['db']['playerTable']} WHERE SteamID = %s", (user,))
#             result = cursor.fetchall()
#             if len(result) == 0:
#                 return -2, -2, -2, -2, -2, -2
#             else:
#                 username = result[0][2]
#                 user = result[0][0]
#                 cursor.execute(f"SELECT * FROM {settings['leader_settings']['db']['table']} WHERE SteamID = %s", (user,))

#         else:
#             cursor.execute(f"SELECT * FROM {settings['leader_settings']['db']['playerTable']} WHERE Username = %s", (user,))
#             result = cursor.fetchall()
#             if len(result) == 0:
#                 return -2, -2, -2, -2, -2, -2
#             else:
#                 username = result[0][2]
#                 user = result[0][0]
#                 cursor.execute(f"SELECT * FROM {settings['leader_settings']['db']['table']} WHERE SteamID = %s", (user,))
#         result = cursor.fetchall()
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#         if len(result) == 0:
#             return -2, -2, -2, -2, -2, -2
#         else:
#             userID = result[0][0]
#             Humanills = result[0][1]
#             ScpKills = result[0][2]
#             Deaths = result[0][3]
#             TotalSeconds = result[0][4]

#             return userID, username, Humanills, ScpKills, Deaths, TotalSeconds
#     except mysql.connector.Error as e:
#         console_log(f"Got an database error while getting the stats: {e}", "error")
#         return -1, -1, -1, -1, -1, -1
#     except Exception as e:
#         console_log(f"There was an error while getting the stats: {e}", "error")
#         return -1, -1, -1, -1, -1, -1
# def get_stats(type):
#     # -1 means that there was an error while connecting to the database
#     # -2 means that stats are empty

#     # Sorts users by type from highest to lowest, then returns top 10
#     try:
#         connection = pool.get_connection()
#         cursor = connection.cursor()
#         cursor.execute(f"SELECT {settings['leader_settings']['db']['playerTable']}.Username, {settings['leader_settings']['db']['table']}.{type} FROM {settings['leader_settings']['db']['table']} INNER JOIN {settings['leader_settings']['db']['playerTable']} ON {settings['leader_settings']['db']['table']}.SteamID = {settings['leader_settings']['db']['playerTable']}.SteamID ORDER BY {settings['leader_settings']['db']['table']}.{type} DESC")
#         result = cursor.fetchall()
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#         if len(result) == 0:
#             return -2
#         else:
#             return result[:10]
#     # Except raise OperationalError("MySQL Connection not available.")
#     except mysql.connector.Error as e:
#         console_log(f"Got an database error while getting the stats: {e}", "error")
#         return -1
#     except Exception as e:
#         console_log(f"There was an error while getting the stats: {e}", "error")
#         return -1
# def all_players_list(index):
#     # -1 means that there was an error while connecting to the database
#     # -2 means that stats are empty

#     # Sorts users by total sum of ScpKills, HumanKills and TotalSeconds from highest to lowest
#     try:
#         connection = pool.get_connection()
#         cursor = connection.cursor()
#         cursor.execute(f"SELECT {settings['leader_settings']['db']['playerTable']}.Username, {settings['leader_settings']['db']['table']}.ScpKills, {settings['leader_settings']['db']['table']}.PlayerKills, {settings['leader_settings']['db']['table']}.Deaths , {settings['leader_settings']['db']['table']}.PlayedSeconds FROM {settings['leader_settings']['db']['table']} INNER JOIN {settings['leader_settings']['db']['playerTable']} ON {settings['leader_settings']['db']['table']}.SteamID = {settings['leader_settings']['db']['playerTable']}.SteamID ORDER BY {settings['leader_settings']['db']['table']}.ScpKills + {settings['leader_settings']['db']['table']}.PlayerKills + {settings['leader_settings']['db']['table']}.PlayedSeconds DESC")
#         result = cursor.fetchall()
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#         if len(result) == 0:
#             return -2
#         else:
#             return_list = []
#             try:    
#                 for i in range(10):
#                     i = i + index
#                     return_list.append(result[i])
#             finally:
#                 return return_list
#     except mysql.connector.Error as e:
#         console_log(f"Got an database error while getting the stats: {e}", "error")
#         return -1
#     except Exception as e:
#         console_log(f"There was an error while getting the stats: {e}", "error")
#         return -1
# def get_pages():
#     # -1 means that there was an error while connecting to the database

#     # Open stats and count pages
#     try:
#         connection = pool.get_connection()
#         cursor = connection.cursor()
#         cursor.execute(f"SELECT COUNT(*) FROM {settings['leader_settings']['db']['table']}")
#         result = cursor.fetchall()
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#         pages = result[0][0] // 10
        
#         return pages
#     except mysql.connector.Error as e:
#         console_log(f"Got an database error while getting the stats: {e}", "error")
#         return -1
#     except Exception as e:
#         console_log(f"There was an error while getting the stats: {e}", "error")
#         return -1