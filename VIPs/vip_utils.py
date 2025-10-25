from Database.Player import Player
from Database.Role import Role
from Database.VipRole import VipRole
from Database.VipAssignment import VipAssignment
from Database.db_session import get_session
from GlobalUtils.utils import is_steamid
from GlobalUtils.logging import console_log
import json

def load_vips(vip_file_path: str) -> dict | int:
    # -1 = error

    # {
    #     "Kontributor":{
    #         "RoleID": "1232333",
    #         "NumberOfActivations": 2,
    #     }
    # }
    
    try:
        with open(vip_file_path, 'r') as json_file:
            data = json.load(json_file)
            vips = data
    except json.decoder.JSONDecodeError:
        console_log("JSON file is empty!", "warning")
        # if json file is empty, make empty list
        data = {}
        # save empty list to json file
        with open(vip_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        vips = data
    except FileNotFoundError:
        console_log("JSON file not found!", "warning")
        # if json file is empty, make empty list
        data = {}
        # save empty list to json file
        with open(vip_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        vips = data
    except Exception as e:
        console_log("An error has occured while loading vips! Error: " + str(e), "error")
        vips = -1
    
    return vips
def user_check(steamid: str, discord_id: str, current_vip: str, vips: dict) -> tuple[int, str | None]:
    """
    Returns:
        -1 = error, error message
        0 = user doesn't have VIP or has one more to share, none
        1 = VIP upgrade, none
        2 = Discord user has VIP, none
        3 = SteamID user has VIP, none
    """
    try:

        with get_session() as session:
            player = (
                session.query(Player)
                .filter((Player.UserId == steamid) | (Player.DiscordId == discord_id))
                .first()
            )

            if not player:
                return -1, "Player not found in database."

            assignments = (
                session.query(VipAssignment)
                .filter(VipAssignment.PlayerId == player.Id)
                .join(VipRole)
                .all()
            )

            if not assignments:
                return 0, None

            current_vip_db = session.query(VipRole).filter_by(Name=current_vip).first()
            if not current_vip_db:
                console_log(f"VIP role '{current_vip}' not found in database!", "error")
                return -1 , f"VIP role '{current_vip}' not found in database."

            for assignment in assignments:
                if str(player.UserId) == str(steamid):
                    # Compare rank IDs if needed (upgrade logic)
                    if assignment.vip_role.Id < current_vip_db.Id:
                        return 1, None  # VIP upgrade
                    return 3, None  # Already has VIP (steam)

                if str(player.DiscordId) == str(discord_id):
                    vip_activation_count = (
                        session.query(VipAssignment)
                        .filter(VipAssignment.PlayerId == player.Id)
                        .count()
                    )
                    max_activations = vips[assignment.vip_role.Name]['NumberOfActivations']
                    if vip_activation_count >= max_activations:
                        return 2, None  # Discord user has VIP and cannot share more
                    return 0, None  # Can share more

            return 0, None  # No VIP or can share more
    except Exception as e:
        console_log(f"There was an error while checking the user: {e}", "error")
        return -1, f"Error: {e}"
def user_add(steamid: str, discord_id: str, vip_role: str) -> tuple[bool, str | None]:
    """
    Adds a new user to the VIP system.

    Args:
        steamid (str): Player's Steam ID (UserId in database)
        discord_id (str): Player's Discord ID
        vip_role (str): Name of the VIP role (e.g. "Donátor")

    Returns:
        int:
            True = Success, None
            False = Failure, error message
    """
    try:

        with get_session() as session:
            player = (
                session.query(Player)
                .filter((Player.UserId == steamid))
                .first()
            )

            if not player:
                return False, "Player not found in database."

            vip = session.query(VipRole).filter_by(Name=vip_role).first()
            if not vip:
                console_log(f"VIP role '{vip_role}' not found in database.", "error")
                return False, f"VIP role '{vip_role}' not found."

            existing_assignment = (
                session.query(VipAssignment)
                .filter(VipAssignment.PlayerId == player.Id,
                        VipAssignment.VipRoleId == vip.Id)
                .first()
            )
            if existing_assignment:
                console_log(f"User {steamid} already has VIP '{vip_role}'.", "warning")
                return True, None  # Already assigned, no error

            assignment = VipAssignment(PlayerId=player.Id, VipRoleId=vip.Id)
            session.add(assignment)
            session.commit()
            console_log(f"Assigned VIP '{vip_role}' to {steamid}", "info")

            return True, None

    except Exception as e:
        console_log(f"Error adding user to VIP system: {e}", "error")
        return False, str(e)
def user_update(steamid: str, new_vip_role: str) -> tuple[bool, str | None]:
    """
    Updates a user's VIP role.

    Args:
        steamid (str): The player's SteamID (UserId in DB).
        new_vip_role (str): The new VIP role name (e.g. "Donátor").

    Returns:
        True if update succeeded.
        (False, str) if update failed (with an error message).
    """
    try:

        with get_session() as session:
            player = session.query(Player).filter(Player.UserId == steamid).first()
            if not player:
                msg = f"Player with SteamID {steamid} not found."
                console_log(msg, "warning")
                return False, msg

            vip_role = session.query(VipRole).filter_by(Name=new_vip_role).first()
            if not vip_role:
                msg = f"VIP role '{new_vip_role}' not found in database."
                console_log(msg, "error")
                return False, msg

            assignment = session.query(VipAssignment).filter_by(PlayerId=player.Id).first()
            if not assignment:
                msg = f"Player {steamid} does not have any VIP assigned."
                console_log(msg, "warning")
                return False, msg

            assignment.VipRoleId = vip_role.Id
            session.commit()

            console_log(f"Updated VIP for {steamid} to '{new_vip_role}'.", "info")
            return True, None

    except Exception as e:
        msg = f"Error while updating VIP role: {e}"
        console_log(msg, "error")
        return False, msg
def user_remove(identifier: str) -> tuple[bool, str | None]:
    """
    Removes a user's VIP assignment by SteamID (UserId) or Discord ID.

    Args:
        identifier (str): The player's SteamID (UserId) or Discord ID.

    Returns:
        (True, None): Removal succeeded.
        (False, str): Failed with an error message.
    """
    try:

        with get_session() as session:
            player = session.query(Player).filter(
                (Player.UserId == identifier) | (Player.DiscordId == identifier)
            ).first()

            if not player:
                msg = f"No player found with ID or DiscordID '{identifier}'."
                console_log(msg, "warning")
                return False, msg

            assignments = session.query(VipAssignment).filter_by(PlayerId=player.Id).all()
            if not assignments:
                msg = f"Player '{identifier}' has no VIP assigned."
                console_log(msg, "info")
                return False, msg

            for a in assignments:
                session.delete(a)
            session.commit()

            console_log(f"Removed all VIP assignments for '{identifier}'.", "info")
            return True, None

    except Exception as e:
        msg = f"Error while removing VIP: {e}"
        console_log(msg, "error")
        return False, msg