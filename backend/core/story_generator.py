from sqlalchemy.orm import Session
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM
from core.config import settings


class StoryGenerator:

    @classmethod
    def _get_llm(cls):
        return ChatGoogleGenerativeAI(
            model="gemini-flash-latest",  
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7,
            # ✅ Increased max tokens to reduce JSON truncation errors
            max_output_tokens=4096, 
        )

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            ("system", STORY_PROMPT),
            ("human", f"Create the story with this theme: {theme}")
        ]).partial(format_instructions=story_parser.get_format_instructions())

        chain = prompt | llm
        raw_response = chain.invoke({})

        response_text = raw_response.content if hasattr(raw_response, 'content') else str(raw_response)
        story_structure = story_parser.parse(response_text)

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()

        # ✅ Access the root node using the Python snake_case name 'root_node'
        root_node_data = story_structure.root_node
        
        # Pydantic parsing ensures this is already a StoryNodeLLM object
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        
        # ✅ Access attributes using the corrected snake_case names
        content = node_data.content
        is_ending = node_data.is_ending       
        is_winning = node_data.is_winning_ending 
        options = node_data.options or []

        node = StoryNode(
            story_id=story_id,
            content=content,
            is_root=is_root,
            is_ending=is_ending,
            is_winning_ending=is_winning,
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and options:
            options_list = []
            for option_data in options:
                # ✅ option_data.next_node is now a StoryNodeLLM object (due to type fix in models.py)
                text = option_data.text
                next_node = option_data.next_node 
                
                # Removed redundant model_validate check since Pydantic parser handles it
                
                child_node = cls._process_story_node(db, story_id, next_node, is_root=False)

                options_list.append({
                    "text": text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node
