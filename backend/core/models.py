from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

# StoryNodeLLM is recursively referenced, so define it first
class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story node")
    
    # Alias isEnding to is_ending (snake_case in Python)
    is_ending: bool = Field(alias='isEnding', description="whether this node is an ending node")
    
    # Alias isWinningEnding to is_winning_ending (snake_case in Python)
    is_winning_ending: bool = Field(alias='isWinningEnding', description="whether this ending is a winning ending")
    
    # Options will use the StoryOptionLLM structure
    options: Optional[List['StoryOptionLLM']] = Field(default=None, description="the options for this node")

    # Required for Pydantic V2 to look at aliases when parsing input
    model_config = ConfigDict(populate_by_name=True)


class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text for this option shown to the user")
    
    # Alias nextNode to next_node. Crucially, its type is StoryNodeLLM, not Dict
    next_node: StoryNodeLLM = Field(alias='nextNode', description="the next node content and its options")
    
    # Required for Pydantic V2 to look at aliases when parsing input
    model_config = ConfigDict(populate_by_name=True)


class StoryLLMResponse(BaseModel):
    title: str = Field(description="the title of the story")
    
    # Alias rootNode to root_node
    root_node: StoryNodeLLM = Field(alias='rootNode', description="the root node of the story")
    
    # Required for Pydantic V2 to look at aliases when parsing input
    model_config = ConfigDict(populate_by_name=True)

# Required to resolve forward references in Pydantic V2 (like 'StoryNodeLLM' inside StoryOptionLLM)
StoryNodeLLM.model_rebuild()
