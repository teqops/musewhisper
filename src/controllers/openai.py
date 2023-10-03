from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.output_parsers import CommaSeparatedListOutputParser
from flask import current_app


def generate_project_names(idea_description, creativity_level, keywords):
    llm = OpenAI(
        openai_api_key=current_app.config['OPENAI_KEY'],
        temperature=0.7)

    output_parser = CommaSeparatedListOutputParser()
    prompt_template_name_ideas = PromptTemplate(
        input_variables=['idea_description', 'creativity_level', 'keywords'],
        template="""
            I am cultivating a project and urgently require a distinctive, unregistered .com domain name. Here is an encapsulation of the project:

                {idea_description}

            Construct 5 .com domain names that are highly abstract, avant-garde, and, to the best of your ability, unregistered. The names should conform to a creativity level of {creativity_level}, where 1 is rooted in professionalism and formality, and 10 is highly inventive, whimsical, and non-conventional.

            Keywords: If provided, intertwine the following keywords in a revolutionary manner: "{keywords}". Absence of keywords indicates freedom to fabricate domain names without any lexical limitations.

            Special Instructions:
            - Synthesize domain names by amalgamating unrelated, unconventional words, prefixes, suffixes, or by forging entirely uncharted terms.
            - Refrain from deploying common lexical combinations and commonplace words; select rare, esoteric, or concocted terms instead.
            - Ensure a subtle resonance with the project concept, even while venturing into avant-garde creativity levels.

            Response Format: return the generated domain names as a comma-separated list, e.g. "domain1.com, domain2.com, domain3.com, domain4.com, domain5.com"
        """,  # noqa: E501
        output_parser=output_parser,
    )
    name_ideas_chain = LLMChain(
        llm=llm,
        prompt=prompt_template_name_ideas,
    )

    chain = SequentialChain(
        chains=[name_ideas_chain],
        input_variables=['idea_description', 'creativity_level', 'keywords'],
    )

    output = chain.run({
        'idea_description': idea_description,
        'creativity_level': creativity_level,
        'keywords': keywords
    })

    if ':' in output:
        output = output.split(':')[1]
    output = output.split(',')

    output = [name.strip() for name in output]
    return output
