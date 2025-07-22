from typing import List, Optional
from pydantic import BaseModel
 
class Setting(BaseModel):
    location: Optional[str]
    worldStyle: Optional[str]
 

class Story(BaseModel):
    summary: Optional[str] = None
    gameplay: Optional[str] = None
    islandMapProgression: Optional[str] = None
    souvenirCollection: Optional[str] = None
    seasonalEvents: Optional[str] = None
    achievementBadgesTrophies: Optional[str] = None
    progressiveJackpot: Optional[str] = None
    monetizationStrategy: Optional[str] = None
    setting: Optional[Setting] = None

 
class Character(BaseModel):
    name: str
    description: str
 
class Symbol(BaseModel):
    name: str
    description: str
    type: str
 
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
    gameTitle: Optional[str]  = None
    platform: Optional[str]  = None
    slotSize: Optional[str]  = None
    tone: Optional[str]  = None
    characters: Optional[List[Character]]  = None
    symbols: Optional[Symbols]  = None
    story: Optional[Story]  = None
    bonusFeatures: Optional[List[BonusFeature]]  = None
    visualStyle: Optional[VisualStyle]  = None