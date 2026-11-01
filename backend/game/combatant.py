
class Combatant:
    def __init__(self, character):
        self.character = character

        # Battle-specific health.
        self.current_health = character.max_health

        # Temporary battle protection.
        self.shield = 0

        # Battle status.
        self.is_alive = True

    @property
    def max_health(self):
        return self.character.max_health

    @property
    def attack(self):
        return self.character.attack

    def take_damage(self, amount):
        if type(amount) is not int or amount < 0:
            raise ValueError("Damage must be a non-negative integer.")

        if not self.is_alive:
            return 0

        remaining_damage = amount

        # Shield absorbs damage before health.
        absorbed = min(self.shield, remaining_damage)
        self.shield -= absorbed
        remaining_damage -= absorbed

        actual_damage = min(self.current_health, remaining_damage)
        self.current_health -= actual_damage

        if self.current_health == 0:
            self.is_alive = False

        return actual_damage

    def heal(self, amount):
        if type(amount) is not int or amount < 0:
            raise ValueError("Healing must be a non-negative integer.")

        if not self.is_alive:
            return 0

        actual_healing = min(
            amount,
            self.max_health - self.current_health
        )

        self.current_health += actual_healing
        return actual_healing

    def add_shield(self, amount):
        if type(amount) is not int or amount < 0:
            raise ValueError("Shield must be a non-negative integer.")

        if self.is_alive:
            self.shield += amount

        return self.shield

    def __str__(self):
        return (
            f"{self.character.name}: "
            f"HP {self.current_health}/{self.max_health}, "
            f"Shield {self.shield}"
        )
