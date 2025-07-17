# schemas.py
from pydantic import BaseModel
from typing import List

class SymbolEffect(BaseModel):
    name: str
    effect: str

class SpecialSymbols(BaseModel):
    WildSymbol: SymbolEffect
    ScatterSymbol: SymbolEffect
    BonusSymbol: SymbolEffect

class ReelSymbols(BaseModel):
    regularSymbols: List[str]
    specialSymbols: SpecialSymbols

class Setting(BaseModel):
    location: str
    worldStyle: str

class Backstory(BaseModel):
    summary: str
    mainCharacter: str
    supportingCharacters: List[str]

class BonusFeature(BaseModel):
    name: str
    trigger: str
    description: str

class VisualStyle(BaseModel):
    artStyle: str
    animation: str
    audio: str

class GameLoop(BaseModel):
    baseGame: str
    metaProgression: str

class UserExperience(BaseModel):
    UXFocus: str
    Accessibility: str

class GameDesignSchema(BaseModel):
    gameTitle: str
    theme: str
    platforms: List[str]
    reelLayout: str
    targetAudience: str
    tone: str
    setting: Setting
    backstory: Backstory
    reelSymbols: ReelSymbols
    bonusFeatures: List[BonusFeature]
    visualStyle: VisualStyle
    gameLoop: GameLoop
    userExperience: UserExperience
