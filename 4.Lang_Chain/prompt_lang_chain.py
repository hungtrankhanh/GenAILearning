from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from output_parsers import person_intel_parser, PersonIntel
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from agents.linkedin_agent import lookup as linkedin_lookup_agent
from agents.twitter_agent import lookup as twitter_lookup_agent

load_dotenv()


def ice_break(name: str):
    summary_template = """
            given the Linkedin information {linkedin_information} and twitter {twitter_information} about a person from I want you to create:
            1. a short summary
            2. two interesting facts about them
            3. A topic that may interest them
            4. 2 creative Ice breakers to open a conversation with them 
            \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    print("linkedin step 1......")
    linkedin_url = linkedin_lookup_agent(name=name)
    print("linkedin step 2......")
    linkedid_data = scrape_linkedin_profile("")

    print("twitter step 1......")
    twitter_name = twitter_lookup_agent(name=name)
    print("twitter step 2......")
    twitter_data = scrape_user_tweets(username=twitter_name)

    res1 = chain.invoke(input={"linkedin_information": linkedid_data, "twitter_information": twitter_data})
    res2 = person_intel_parser.parse(res1.get('text'))
    return res2, linkedid_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Hello Lang Chain")
    ice_break(name="Hung Tran")
