import enum


class TurnParts(enum.Enum):
    UNTAP = 0
    UPKEEP = 1
    DRAW = 2
    PRECOMBAT_MAIN = 3
    BEGIN_COMBAT = 4
    DECLARE_ATTACKERS = 5
    DECLARE_BLOCKERS = 6
    FIRST_STRIKE_DAMAGE = 7
    COMBAT_DAMAGE = 8
    END_COMBAT = 9
    POSTCOMBAT_MAIN = 10
    END_STEP = 11
    CLEANUP = 12
