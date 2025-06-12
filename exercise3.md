# Exercise 3: Agent Assembly & Memory

### Estimated Duration: 30 Minutes

## Overview

In this exercise, you will assemble a LangChain agent that can plan, remember, and explain its actions. You will configure a structured agent with tool access, integrate memory to support multi-turn dialogue, and instrument callbacks to trace and debug each step of the agent’s reasoning.

An **AI agent** is a software program designed to act on behalf of a user or another system. It can perform tasks, make decisions, or automate processes independently. Essentially, it’s like a digital assistant that understands queries, takes actions, and may even learn from interactions to improve over time. For example, a chatbot that answers your questions or an AI in an invoice system that finds specific invoices qualifies as an AI agent.

**Contextual memory** refers to an AI system’s ability to retain and recall information from previous interactions or contexts. This capability allows the AI to deliver more personalized and relevant responses by leveraging the history of a conversation or a user’s past behavior. For instance, if you ask a chatbot about your invoices and later ask a follow-up question, contextual memory enables it to remember the earlier discussion and respond coherently.

## Objectives

You will be able to complete the following tasks:

- Task 1: Choose & Configure an Agent

- Task 2: Add Conversation Memory

- Task 3: Instrument Callbacks for Observability

## Task 1: Choose & Configure an Agent

In this task, you will select a Structured Agent using LangChain’s create_react_agent function and register your Search and OCR tools. This will allow the agent to dynamically choose tools based on user input and execute them in sequence.

1. Navigate to the **Visual Studio Code** window, which you opened in the previous exercise.

1. Once you are in the **Visual Studio Code**, from the explorer, select `exercise3_agent_memory` file.

1. Once opened, navigate to `# Task 1: Choose & Configure an Agent` comment.

   ![](./media/ex2img3.png)

1. Add the following code snippet under the comment.

   ```python
   class InvoiceAgent:
    """Structured agent with tool access and memory"""
    
    def __init__(self, enable_memory=True, enable_callbacks=True):
        # Initialize LLM
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
            temperature=0.1
        )
        
        # Initialize tools
        self.search_tool = InvoiceSearchTool()
        self.retrieval_qa = InvoiceRetrievalQA()
        self.ocr_tool = OCRTool()
        
        # Create tools list
        self.tools = [
            self.search_tool.get_langchain_tool(),
            Tool(
                name="qa_retrieval",
                description="Answer detailed questions about invoices using retrieval and AI analysis. Use this for complex questions that need contextual understanding and reasoning.",
                func=self._qa_tool_wrapper
            ),
            self.ocr_tool.get_langchain_tool()
        ]
   ```
   > The InvoiceAgent class creates an AI agent for invoice-related tasks with tool access and optional memory.

   >It initializes an Azure OpenAI language model (AzureChatOpenAI) with low temperature for consistent responses.

   >It integrates two tools: InvoiceSearchTool for searching, InvoiceRetrievalQA for detailed Q&A.

   >The tools are wrapped into a LangChain-compatible list, with qa_retrieval handling complex invoice questions via a custom wrapper.

   >The agent supports enable_memory and enable_callbacks for conversation history and event tracking, respectively.

   >It enables efficient invoice data handling, from search to contextual analysis.

1. Once after adding, the snippet will look similar to this. Verify and use **CTRL + S** to save the changes.

   ![](./media/ex2img7.png)

## Task 2: Add Conversation Memory

In this task, you will add ConversationBufferMemory to your agent so it can retain and reference prior conversation turns. This enables more natural, context-aware dialogue where earlier inputs influence future responses.

1. Now that you’ve configured the agent, it’s time to add memory to it.

1. In the same file i.e `exercise3_agent_memory`, navigate to `# Task 2: Add Conversation Memory` comment.

   ![](./media/ex2img9.png)

1. Add the following code snippet below the comment.

   ```python
        self.memory = None
        if enable_memory:
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="output"
            )
   ```

   >This code snippet manages conversation memory for the InvoiceAgent class.

   >It initializes self.memory as None by default.

   >If enable_memory is True, it creates a ConversationBufferMemory object.

   >The memory stores chat history with memory_key="chat_history", returns messages, and uses output_key="output".

   >This enables the agent to retain and reference past interactions for context-aware responses.

1. Once added, the code will look similar to this. Verify it and use **CTRL + S** to save the file.

   ![](./media/ex2img10.png)

## Task 3: Instrument Callbacks for Observability

In this task, you will integrate LangChain’s CallbackHandler to monitor the agent’s execution. You will log each step—including planning, tool use, and response—to the console or Application Insights for transparency and easier debugging.

1. Now that the agent is set up, it’s time to log each step—including planning, tool usage, and responses—to the console or Application Insights for better transparency and easier debugging.


1. Navigate to `#Task 3: Setup callbacks` comment.

   ![](./media/ex2img11.png)

1. Add the following code snippet below the comment.

   ```python
        self.callbacks = []
        if enable_callbacks:
            self.callback_handler = CustomCallbackHandler()
            self.callbacks = [self.callback_handler]
   ```

   >This code snippet manages callbacks for the InvoiceAgent class.

   >It initializes an empty self.callbacks list.

   >If enable_callbacks is True, it creates a CustomCallbackHandler instance.

   >The handler is added to the self.callbacks list.

   >Callbacks enable tracking or logging of events during the agent's operations.

1. Once added, the code will look similar to this. Verify it and use **CTRL + S** to save the file.

   ![](./media/ex2img12.png)

run the following command in the terminal to run the retriever.

   ```
   python exercise2_retrieval.py
   ```

   ![](./media/ex2img30.png)

1. Once you run it, you'll see the results. In the first step, the retriever fetches the relevant documents. In the next step, the LLM processes these documents and generates a meaningful answer based on the example prompts provided in the code files.

   ![](./media/ex2img31.png)

   ![](./media/ex2img32.png)

1. Now you have successfully completed the RetrievalQA Chain.

## Summary

In this exercise, you assembled a LangChain agent with dynamic planning, memory, and observability. You configured a Structured Agent with access to your tools, enabled memory to support multi-turn interactions, and used callbacks to trace each step in the agent's decision-making process.