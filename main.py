from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
load_dotenv()

import asyncio

llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
# llm = ChatOpenAI(model="gpt-4o")
# planner_llm = ChatOpenAI(model='o3-mini')

browser_config = BrowserConfig(
    headless=False,
    disable_security=True,
)

browser = Browser(config=browser_config)


agent = Agent(
        task="What can you tell me about the theories displayed about game theory?",
        llm=llm,
        browser=browser
    )

async def main():
    try:
        result = await agent.run()
        print(result)
    except Exception as e:
        print(f"Error during agent execution: {e}")
    finally:
        input("Press Enter to close the browser...")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
