from typing import List, Optional
from pydantic import BaseModel
 
class Setting(BaseModel):
    location: str
    worldStyle: str
 
class Story(BaseModel):
    summary: str
    gameplay: str
    setting: Setting
 
class Character(BaseModel):
    name: str
    description: str
 
class Symbol(BaseModel):
    name: str
    description: str
 
class Symbols(BaseModel):
    regularSymbols: List[Symbol]
    specialSymbols: List[Symbol]
 
class BonusFeature(BaseModel):
    name: str
    type: str
    trigger: str
    description: str
 
class VisualStyle(BaseModel):
    artStyle: str
 
class GameDesignSchema(BaseModel):
    gameTitle: str
    story: Optional[Story] = None
    characters: Optional[List[Character]] = None
    symbols: Optional[Symbols] = None
    bonusFeatures: Optional[List[BonusFeature]] = None
    visualStyle: Optional[VisualStyle] = None