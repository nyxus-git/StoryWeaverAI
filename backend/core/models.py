from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story node")
    
    # FIX: Made optional
    is_ending: Optional[bool] = Field(default=None, alias='isEnding', description="whether this node is an ending node")
    
    # FIX: Made optional
    is_winning_ending: Optional[bool] = Field(default=None, alias='isWinningEnding', description="whether this ending is a winning ending")
    
    options: Optional[List['StoryOptionLLM']] = Field(default=None, description="the options for this node")

    model_config = ConfigDict(populate_by_name=True)


class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text for this option shown to the user")
    
    # FIX: Made optional
    next_node: Optional[StoryNodeLLM] = Field(default=None, alias='nextNode', description="the next node content and its options")
    
    model_config = ConfigDict(populate_by_name=True)


class StoryLLMResponse(BaseModel):
    title: str = Field(description="the title of the story")
    
    root_node: StoryNodeLLM = Field(alias='rootNode', description="the root node of the story")
    
    model_config = ConfigDict(populate_by_name=True)

# Rebuild the model to apply the fixes
StoryNodeLLM.model_rebuild()