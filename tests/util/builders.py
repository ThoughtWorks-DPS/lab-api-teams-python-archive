from api.models.team import Team

class TeamBuilder:
    def with_name(self, name: str):
        self.name = name
        return self

    def build(self) -> Team:
        return Team(name=self.name)
