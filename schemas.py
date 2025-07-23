from typing import List, Optional
from pydantic import BaseModel
 
class Story(BaseModel):
    summary: str
    gameplay: str
    baseSpinMechanics: str
    bonusTriggersCollectionSystems: str
    unlockableAreasOrLevels: str
    progressiveJackpot: str
    achievementBadgesTrophies: str
    monetizationStrategy: str


class Character(BaseModel):
    name: str
    description: str
 
class Symbol(BaseModel):
    name: str
    description: str
 
class Symbols(BaseModel):
    lowPaySymbols: List[Symbol]
    royalSymbols: List[Symbol]
    highPaySymbols: List[Symbol]
    wildSymbols: List[Symbol]
    scatterSymbols: List[Symbol]
 
class BonusFeature(BaseModel):
    name: str
    type: str
    trigger: str
    description: str
 
class VisualStyle(BaseModel):
    artStyle: str
 
 
 
class GameDesignSchema(BaseModel):
    gameTitle: str
    platform: str
    slotSize: str
    tone: str
    story: Story
    characters: List[Character]
    symbols: Symbols
    bonusFeatures: List[BonusFeature]
    visualStyle: VisualStyle