# Exercise 2: LangChain Tools & Retrieval Chain

### Estimated Duration: 30 Minutes

## Overview

In this exercise, you will integrate Azure AI Search with LangChain by wrapping your search index as a retriever and building a RetrievalQA chain powered by Azure OpenAI. These steps will enable your chatbot to fetch relevant context from indexed content and use it to generate accurate, grounded responses.

## Objectives

You will be able to complete the following tasks:

- Task 1: Implement Search Retriever Tool

- Task 2: Build RetrievalQA Chain

## Task 1 : Define & Populate Search Index

In this task, you will install the necessary LangChain community package and import the AzureSearchVectorStore class. This allow you to wrap your Azure AI Search index as a retriever, making it accessible for downstream question-answering workflows within LangChain.

1. Once you have setup Azure Index in previous task, now its time to develop a retriver using langchain.

1. Navigate to **Visual Studio Code**  from the desktop of JumpVM.

1. From the top menu, click on **file** and select **Open Folder** option.

1. From the open folder pane, navigate to `C:\langchain-codefiles` and click on open folder.

1. In the pop up window click on Trust.

1. Now, you can see that there are some files present in this folder. In these further tasks, you will complete these code files.

1. From the **explorer**, select and open `exercise2_retrieval.py`.

1. Once you are in the file, review the file once then navigate to **Task 1: Implement Search Retriever Tool** comment.

1. Under the comment, add the following code snippet.

   ```python
   class InvoiceSearchTool:
    """Tool wrapper for invoice search functionality"""
    
    def __init__(self):
        self.retriever = AzureAISearchRetriever()
    
    def search_invoices(self, query: str) -> str:
        """Search for invoices based on query"""
        documents = self.retriever.get_relevant_documents(query, k=5)
        
        if not documents:
            return "No relevant invoices found."
        
        results = []
        for i, doc in enumerate(documents, 1):
            results.append(f"Result {i}:\n{doc.page_content}")
        
        return "\n\n".join(results)
    
    def get_langchain_tool(self):
        """Return LangChain Tool object"""
        return Tool(
            name="invoice_search",
            description="Search for invoice information. Use this when you need to find specific invoices, customer information, products, or financial data.",
            func=self.search_invoices
        )
   ```

   >The InvoiceSearchTool class enables invoice searching using Azure AI Search.

   >It initializes with an AzureAISearchRetriever to fetch relevant documents.
     
   >The search_invoices method takes a query, retrieves the top 5 matching documents, and formats them into a string.

   >If no documents are found, it returns "No relevant invoices found."

   >The get_langchain_tool method wraps this functionality into a LangChain Tool for broader use.

   >Use it to find specific invoices, customer details, products, or financial data efficiently.

## Task 2: Build RetrievalQA Chain

In this task, you will create a RetrievalQA chain by connecting your search retriever to an Azure OpenAI language model. You will configure the chain to retrieve top-k search snippets and pass them along with user queries to the model, enabling the chatbot to provide informed, relevant answers.

1. Once the Search Retriever Tool is implemented, the next step is to create a chain that combines the retrieved data and passes it to the LLM. The LLM will then process this input and return a meaningful response.

1. In the same file, scroll down to the comment - **Task 2: Build RetrievalQA Chain** and add the provided snippet under that.

    ```python
    class InvoiceRetrievalQA:
    """RetrievalQA chain for invoice queries"""
    
    def __init__(self):
        # Initialize Azure OpenAI
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
            temperature=0.1
        )
        
        # Initialize retriever
        self.retriever = AzureAISearchRetriever()
        
        # Create RetrievalQA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            verbose=True
        )
    
    def query(self, question: str):
        """Query the RetrievalQA chain"""
        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result["source_documents"]
            }
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "source_documents": []
            }
   ```
   >The InvoiceRetrievalQA class enables question-answering about invoices by integrating document retrieval and language model generation.

   >It leverages Azure AI Search to retrieve relevant invoice documents and Azure OpenAI to generate answers based on them.

   >In the __init__ method, it initializes an Azure OpenAI language model with specific settings (e.g., low temperature for consistent responses) and sets up an AzureAISearchRetriever.

   >The query method takes a question, uses the retriever to find documents, generates an answer with the language model, and returns both the answer and source documents.

   >It includes robust error handling, returning an error message and empty document list if something fails.

   >This class provides an efficient way to get detailed, context-based answers to invoice-related queries.

1. Once done editing, use **CTRL + S** to save the file.

1. Now, use the create option and create file with name `.env`.

1. Once created, add the following content.

   ```
   # Azure OpenAI Configuration
   AZURE_OPENAI_ENDPOINT=https://openai-<inject key="Deployment ID" enableCopy="false"/>.openai.azure.com/
   AZURE_OPENAI_KEY=
   AZURE_OPENAI_DEPLOYMENT=gpt-35-turbo
   AZURE_OPENAI_API_VERSION=

   # Azure AI Search Configuration
   AZURE_SEARCH_ENDPOINT=https://aisearch-<inject key="Deployment ID" enableCopy="false"/>.search.windows.net
   AZURE_SEARCH_KEY=
   AZURE_SEARCH_INDEX_NAME=invoice-index
   ```

1. Navigate to the **openai-<inject key="Deployment ID" enableCopy="false"/>** Azure OpenAI Service.

1. From the top menu, select **...** and click on **Terminal** and from the list, select **New terminal**.

1. Run the following command in the terminal to install all the requirements.

1. 

## Summary

In this exercise, you connected Azure AI Search with LangChain by wrapping your search index as a retriever and building a RetrievalQA chain using Azure OpenAI. These components worked together to enable the chatbot to retrieve relevant content and generate context-aware answers based on your indexed data.