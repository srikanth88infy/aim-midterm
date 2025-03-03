import os

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langsmith import Client
from dotenv import load_dotenv
from ragas.testset.graph import KnowledgeGraph
from ragas.testset.graph import Node, NodeType
from ragas.testset.transforms import apply_transforms
from ragas.testset import TestsetGenerator
from app import compiled_graph
import nltk

docs = []
load_dotenv()
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

def generate_sdg():

    # load_docs("data/")
    # print("##### docs #####")
    # print(docs)
    # print("#####")
    #
    # generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
    # generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
    #
    # from ragas.testset import TestsetGenerator
    #
    # generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)
    # dataset = generator.generate_with_langchain_docs(docs, testset_size=10)

    loader = TextLoader('data/unix-so.csv')
    docs = loader.load()

    generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
    generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

    generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)
    dataset = generator.generate_with_langchain_docs(docs, testset_size=2)

    print(dataset.to_pandas())

    evaluate_sdg(dataset)


def evaluate_sdg(dataset):
    print("Evaluating SDG")

    for test_row in dataset:
        response = compiled_graph.invoke({"messages": [HumanMessage(content=test_row.eval_sample.user_input)]})
        print(response["context"])
        test_row.eval_sample.response = response["messages"][-1].content
        test_row.eval_sample.retrieved_contexts = [context.page_content for context in response["context"]]

    print(dataset.to_pandas())
    from ragas import EvaluationDataset, evaluate, RunConfig
    from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, ResponseRelevancy, \
        ContextEntityRecall, NoiseSensitivity


    evaluation_dataset = EvaluationDataset.from_pandas(dataset.to_pandas())
    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))

    result = evaluate(
        dataset=evaluation_dataset,
        metrics=[LLMContextRecall(), Faithfulness(), FactualCorrectness(), ResponseRelevancy(), ContextEntityRecall(),
                 NoiseSensitivity()],
        llm=evaluator_llm
    )

    print(result)

if __name__ == '__main__':
    generate_sdg()

