from pydantic import BaseModel
from typing import List, Optional


# -------- SYMBOLS & BONUS --------

class Symbol(BaseModel):
    name: str
    description: str
    payoutMultiplier: int


class Symbols(BaseModel):
    highValue: List[Symbol]
    midValue: List[Symbol]
    lowValue: List[Symbol]


class WildSymbol(BaseModel):
    name: str
    effect: str


class ScatterSymbol(BaseModel):
    name: str
    effect: str


class BonusTriggerSymbol(BaseModel):
    name: str
    effect: str


class BonusFeature(BaseModel):
    name: str
    trigger: str
    description: str
    mechanics: str
    storyIntegration: Optional[str] = None


# -------- GAMEPLAY --------

class Gameplay(BaseModel):
    reels: int
    rows: int
    paylines: int
    symbols: Symbols
    wildSymbol: WildSymbol
    scatterSymbol: ScatterSymbol
    bonusTriggerSymbol: BonusTriggerSymbol
    bonusFeatures: List[BonusFeature]


# -------- CHARACTERS & STORYLINE --------

class Character(BaseModel):
    name: str
    trait: str
    role: str
    symbolType: Optional[str] = None


class Progression(BaseModel):
    unlockableChapters: List[str]
    characterEvolution: str
    shiftingEnvironments: str


class Storyline(BaseModel):
    backstory: str
    mainRole: str
    characters: List[Character]
    conflict: str
    progression: Progression


# -------- VISUALS & AUDIO --------

class VisualStyle(BaseModel):
    backgroundArt: str
    animationIdeas: List[str]
    symbolDesign: str
    uiElements: str


class AudioStyle(BaseModel):
    soundtrack: str
    soundEffects: List[str]
    musicSuggestions: List[str]


# -------- ROOT MODEL --------

class SlotMachineGame(BaseModel):
    slotMachineTitle: str
    storyline: Storyline
    gameplay: Gameplay
    visualStyle: VisualStyle
    audioStyle: AudioStyle