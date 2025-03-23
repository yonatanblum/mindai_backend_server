import json
import logging
from typing import Optional, Tuple

import aiofiles
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache

from schemas.query_service_schemas.query_schemas import QueryIntent
from services.query_service.constants import (
    API_KEY,
    COMMON_PHRASES,
    LLM_MODEL_NAME,
    LLM_TEMPERATURE,
    QUERY_CACHE_FILE,
)
from services.query_service.template_constants import QUERY_SYSTEM_TEMPLATE

# Initialize cache
set_llm_cache(InMemoryCache())

# Setup logging
logger = logging.getLogger(__name__)


class QueryProcessor:
    def __init__(self):
        # Initialize LangChain components
        self.llm = ChatOpenAI(
            temperature=LLM_TEMPERATURE, model_name=LLM_MODEL_NAME, api_key=API_KEY
        )

        self.parser = PydanticOutputParser(pydantic_object=QueryIntent)

        # Load query cache
        self.query_cache = self.load_query_cache()

        # Create prompt templates
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(
            QUERY_SYSTEM_TEMPLATE
        )
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(
            template="{input}"
        )

        # Create the chat prompt
        self.chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_message_prompt, self.human_message_prompt]
        )

        # Initialize chain using pipe syntax
        self.chain = self.chat_prompt | self.llm | self.parser

    async def save_query_cache(self):
        """Save the query cache to a JSON file asynchronously"""
        try:
            async with aiofiles.open("query_cache.json", "w") as cache_file:
                await cache_file.write(json.dumps(self.query_cache))
            logger.info("Query cache saved successfully")
        except Exception as e:
            logger.error(f"Error saving query cache: {str(e)}")

    def load_query_cache(self):
        """Load the query cache from a JSON file"""
        try:
            with open(QUERY_CACHE_FILE, "r") as cache_file:
                return json.load(cache_file)
        except FileNotFoundError:
            logger.info("Query cache file not found. Starting with empty cache")
            return {}
        except Exception as e:
            logger.error(f"Error loading query cache: {str(e)}")
            return {}

    def check_common_phrases(self, query: str) -> Optional[Tuple[str, dict]]:
        """Check if query matches any common phrases"""
        query_lower = query.lower().strip()
        return COMMON_PHRASES.get(query_lower)

    async def classify_query(self, question: str) -> Tuple[Optional[str], dict]:
        """Classify query intent and extract parameters using LangChain"""
        # Check cache first
        cache_key = question.lower().strip()
        if cache_key in self.query_cache:
            return self.query_cache[cache_key]

        # Check common phrases
        common_result = self.check_common_phrases(question)
        if common_result:
            return common_result

        try:
            # Run the chain with corrected input parameter
            result = await self.chain.ainvoke({"input": question})

            # Handle irrelevant queries
            if result.intent == "irrelevant":
                return None, {}

            # Process the result
            processed_result = await self._process_result(result)

            # Cache the result
            self.query_cache[cache_key] = processed_result
            await self.save_query_cache()

            return processed_result

        except Exception as e:
            logger.error(f"Error in query classification: {str(e)}")
            return None, {}

    async def _process_result(
        self, query_result: QueryIntent
    ) -> Tuple[Optional[str], dict]:
        """Process and validate the classification result"""
        try:
            intent = query_result.intent
            params = query_result.params

            # Apply business rules and defaults
            if "days" in params:
                if isinstance(params["days"], (int, float)):
                    params["days"] = min(max(params["days"], 1), 30)
                elif isinstance(params["days"], str):
                    try:
                        days = float(params["days"].split()[0])
                        params["days"] = min(max(days, 1), 30)
                    except:
                        params["days"] = 7

            return intent, params

        except Exception as e:
            logger.error(f"Error processing classification result: {str(e)}")
            return None, {}

    async def process_query(self, query: str) -> Tuple[Optional[str], dict]:
        """Main method to process user queries"""
        if not query or not isinstance(query, str):
            logger.error("Invalid query input")
            return None, {}

        # Clean and normalize query
        query = query.strip()
        if not query:
            return None, {}

        # Get classification and parameters
        intent, params = await self.classify_query(query)

        # Log the result
        logger.info(f"Query: {query}")
        logger.info(f"Classified intent: {intent}")
        logger.info(f"Extracted params: {params}")

        return intent, params
