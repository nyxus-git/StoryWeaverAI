from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story node")
    
    is_ending: bool = Field(alias='isEnding', description="whether this node is an ending node")
    
    is_winning_ending: bool = Field(alias='isWinningEnding', description="whether this ending is a winning ending")
    
    options: Optional[List['StoryOptionLLM']] = Field(default=None, description="the options for this node")

    model_config = ConfigDict(populate_by_name=True)


class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text for this option shown to the user")
    
    next_node: StoryNodeLLM = Field(alias='nextNode', description="the next node content and its options")
    
    model_config = ConfigDict(populate_by_name=True)


class StoryLLMResponse(BaseModel):
    title: str = Field(description="the title of the story")
    
    root_node: StoryNodeLLM = Field(alias='rootNode', description="the root node of the story")
    
    model_config = ConfigDict(populate_by_name=True)

StoryNodeLLM.model_rebuild()
