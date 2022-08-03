from api.services.team_service import TeamService


def get_team_service() -> TeamService:
    return TeamService()
