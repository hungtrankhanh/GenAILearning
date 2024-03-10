from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_agent import lookup as linkedin_lookup_agent
if __name__ == "__main__":
    print("Hello Lang Chain")
    load_dotenv()
    info = """
    William Henry Gates III (born October 28, 1955) is an American businessman, investor, philanthropist, and writer best known for co-founding the software giant Microsoft, along with his childhood friend Paul Allen. During his career at Microsoft, Gates held the positions of chairman, chief executive officer (CEO), president, and chief software architect, while also being its largest individual shareholder until May 2014.[2][a] He was a prominent pioneer of the microcomputer revolution of the 1970s and 1980s.

Gates was born and raised in Seattle, Washington. In 1975, he and Allen founded Microsoft in Albuquerque, New Mexico. Gates led the company as its chairman and chief executive officer until stepping down as CEO in January 2000, succeeded by Steve Ballmer, but he remained chairman of the board of directors and became chief software architect. During the late 1990s, he was criticized for his business tactics, which were considered anti-competitive. This opinion has been upheld by numerous court rulings.[5] In June 2008, Gates transitioned into a part-time role at Microsoft and full-time work at the Bill & Melinda Gates Foundation, the private charitable foundation he and his then-wife Melinda had established in 2000.[6] He stepped down as chairman of the Microsoft board in February 2014 and assumed the role of technology adviser to support newly appointed CEO Satya Nadella.[7] In March 2020, Gates left his board positions at Microsoft and Berkshire Hathaway to focus on his philanthropic efforts on climate change, global health and development, and education.[8]

Since 1987, Gates has been included in the Forbes list of the world's billionaires. From 1995 to 2017, he held the Forbes title of the richest person in the world every year except in 2008 and from 2010 to 2013. In October 2017, he was surpassed by Amazon founder Jeff Bezos, who had an estimated net worth of US$90.6 billion compared to Gates's net worth of US$89.9 billion at the time.[9] In the Forbes 400 list of wealthiest Americans in 2023, he was ranked sixth with a wealth of $115.0 billion.[10] As of March 2024, Gates has an estimated net worth of US$150 billion, making him the fifth-richest person in the world according to the Bloomberg Billionaires Index.[11]

Later in his career and since leaving day-to-day operations at Microsoft in 2008, Gates has pursued other business and philanthropic endeavors. He is the founder and chairman of several companies, including BEN, Cascade Investment, TerraPower, bgC3, and Breakthrough Energy. He has donated sizable amounts of money to various charitable organizations and scientific research programs through the Bill & Melinda Gates Foundation, reported to be the world's largest private charity. Through the foundation, he led an early 21st century vaccination campaign that significantly contributed to the eradication of the wild poliovirus in Africa. In 2010, Gates and Warren Buffett founded The Giving Pledge, whereby they and other billionaires pledge to give at least half of their wealth to philanthropy.[12]
    """

    summary_template = """
    Given the information {info} about a person, I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(input_variables=["info"], template=summary_template)
    llm  = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    print("step 1......")
    linkedin_url = linkedin_lookup_agent("hung tran")
    print("step 2......")
    linkedid_data = scrape_linkedin_profile("")
    res = chain.invoke(input={"info": linkedid_data})
    # res = chain.run(info=linkedid_data)
    print(res.get('text'))

