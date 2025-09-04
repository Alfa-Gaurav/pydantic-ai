import asyncio
from datetime import date

from pydantic import BaseModel, ValidationError
from typing_extensions import TypedDict


from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()




class City(TypedDict, total=False):
    name: str
    country: str

class Cities(TypedDict, total=False):
    cities: list[City]

agent = Agent('openai:gpt-4o', output_type=Cities)


async def main():
    user_input = 'List 10 cities in the world.'
    async with agent.run_stream(user_input) as result:
        async for message, last in result.stream_responses(debounce_by=0.01):  
            try:
                profile = await result.validate_response_output(  
                    message,
                    allow_partial=not last,
                )
            except ValidationError:
                continue
            print(profile)

if __name__ == '__main__':
    asyncio.run(main())