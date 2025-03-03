

### Task 1: Articulate problem, solution, audience /

#### Problem

 Platform teams in a company build tools, frameworks, infrastructure that other developers can build on top of that. 
 As the adoption of these tools grow within the org, company there will be a lot of queries, support that the platform engineers 
 need to provide their customers (who are none other than the peer software engineers)  

 Often times, a same questions might be asked, a similar fire needs to be put off, a documentation should be referred to etc. Understanding the context of the problem,  
 replying back with a solution or rather conversing a solution back and forth would consume a lot of time. Often times, a similar type of question needs to be re-answered.

#### Solution

 All the conversations are slack conversations via threads. We can use all these conversations and develop a RAG application so that for any new question,  
our LLM application will get any of the related conversations and their summarized solution for the customers to try.
 We can adapt this to being a agentic solution as well, if we need to get information from external sources like developer documentation, API logs etc.

This will be insanely helpful for: \
 1) customers who can get quick responses and be able to decode, fix any of their issues with the responses from the application. /  They need not wait for the engineer to start the conversation, explain their context etc. 
 2) give time back to the platform engineering teams. 


We will build with the following stack: 

 * LLM: gpt-4o
 Any good reasoning model would work fine for our use-case. But this specific implementation will use OpenAI's gpt-4o* models 
 * Embedding Models: text-embedding-3-small snowflake-arctic-embed-l
 Vector size of 1536 would be more than sufficient for the prototype. We will also be fine tuning with the snowflake embedding models. The primary purpose is to make sure our prototype works as expected.
 Also using larger embedding models would mean greater compute and more $$$$ which we are trying to avoid for this attempt.
 * Vector Store: Qdrant
 A cloud instance of Qdrant database would be necessary. Loading most of the slack messages into memory might be an overfit. We can get away with an open-sourced DB with a free instance version for the prototype. 
 * Monitoring: LangSmith 
 Langsmith will be helpful in any of the Operations oversight e.g. how many calls to openAI, what is the latency, how much did it cost us to train, retrieve and answer questions etc. 
 * Evaluation: RAGAS
 RAGAS evaluation metrics would be necessary as we iteratively improve our model via fine tuning, updating chunks etc. This would be a first level sanity check before we make any iterative releases. 
 * User iterface: Streamlit
 For this prototype, we are using streamlit deploy and playaround with our application. Its a simple python UI and we can get it up and running within few lines of configuration 
 * Hosting: Hugging Face
 We need our application to be running in some server for users to be able to play with it. HuggingFace provides this option and its easy to use with 1 click deployments, host our fine-tuned models etc. 

#### Audience

 As described, the audience would be internal peer teams trying to build on top of any platform features.   


### Task 2: Describing your data \

We pick few slack conversations with the type of questions that were most frequently asked, if used in context, will help customers get back with the proper responses on how they can get unblocked.
This is just for this prototype. Ideally, we should be using all the slack conversations, rahter than handpicking them 

For each slack convesation, we get the summary of the responses from the LLM. We prepare the data as {question, summary(conversation)} tuples and create embedding
We would start with the baseline recursive character text splitter chunking strategy and have a chunk size of 2048 for this prototype. This is the sweet spot as most questions are 2-3 lines. 

We can give access to developer documentation and logs as well if required for an agentic work flow.


### Task 3: Building an End-to-End Agentic RAG prototype \

We would develop a quick and simple prototype with few hand-picked slack messages and threads. We would create embedding on this data and store then in a vector DB.  
Hopefully an in-memory DB would be sufficient for this purpose. Later we would develop a RAG application that will query the vector DB to find '3' closest Q&A pairs and inject them into the context
Finally we ask LLM to answer the question based on the context provided. We would definitely need to fine tune the embeddinds for better performance. 
We would like fetch additional data from logs API or documentation API later down.

We will be fronting this application with Chainlit (a UI framework) that is used for prototyping purposes. We would dockerize this entire fullstack and host it on huggingface spaces, so that the users can play with it. 

Ideally, we would want this application to be accessed via a slackbot itself. So that we a peer team asks questions internally, the slack bot will ask our RAG application and send back the responses as slack conversations. 


### Task 4: Creating a Golden Test Data Set \







