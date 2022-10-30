from enum import IntEnum, Enum


class Language(Enum):
    English = "en"
    Spanish = "es"

    @property
    def label(self) -> str:
        return {
            Language.English: _("English"),
            Language.Spanish: _("Spanish"),
        }[self]


class Gain(IntEnum):
    G1 = 0
    G2 = 1
    G4 = 2
    G6 = 3
    G8 = 4
    G12 = 5
    G24 = 6

    @property
    def label(self) -> str:
        return {
            Gain.G1: "1",
            Gain.G2: "2",
            Gain.G4: "4",
            Gain.G6: "6",
            Gain.G8: "8",
            Gain.G12: "12",
            Gain.G24: "24",
        }[self]

    @property
    def settings(self) -> str:
        return {
            Gain.G1: "0",
            Gain.G2: "1",
            Gain.G4: "2",
            Gain.G6: "3",
            Gain.G8: "4",
            Gain.G12: "5",
            Gain.G24: "6",
        }[self]
