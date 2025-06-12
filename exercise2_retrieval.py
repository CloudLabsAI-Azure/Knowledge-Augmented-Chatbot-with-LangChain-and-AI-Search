# exercise2_retrieval.py
# Exercise 2: LangChain Tools & Retrieval Chain

import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain.schema import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from typing import List, Any
from pydantic import Field

# Load environment variables
load_dotenv()

class AzureAISearchRetriever(BaseRetriever):
    """Custom retriever class that wraps Azure AI Search functionality"""
    
    search_endpoint: str
    search_key: str
    index_name: str
    search_client: Any = Field(exclude=True)  # Exclude from serialization
    
    class Config:
        arbitrary_types_allowed = True  # Allow SearchClient type
    
    def __init__(self, **kwargs):
        # Get environment variables
        search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        search_key = os.getenv("AZURE_SEARCH_KEY")
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
        
        # Create search client
        search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(search_key)
        )
        
        # Initialize with the required fields
        super().__init__(
            search_endpoint=search_endpoint,
            search_key=search_key,
            index_name=index_name,
            search_client=search_client,
            **kwargs
        )
    
    def _get_relevant_documents(
        self, 
        query: str, 
        *,
        run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Retrieve relevant documents from Azure AI Search"""
        try:
            results = self.search_client.search(
                search_text=query,
                top=5,
                include_total_count=True
            )
            
            documents = []
            for result in results:
                content = self._extract_content_from_result(result)
                doc = Document(
                    page_content=content,
                    metadata=dict(result)
                )
                documents.append(doc)
            
            return documents
        
        except Exception as e:
            print(f"Error retrieving documents: {str(e)}")
            return []
    
    def get_relevant_documents(self, query, k=5):
        """Retrieve relevant documents from Azure AI Search (legacy method)"""
        try:
            results = self.search_client.search(
                search_text=query,
                top=k,
                include_total_count=True
            )
            
            documents = []
            for result in results:
                content = self._extract_content_from_result(result)
                doc = Document(
                    page_content=content,
                    metadata=dict(result)
                )
                documents.append(doc)
            
            return documents
        
        except Exception as e:
            print(f"Error retrieving documents: {str(e)}")
            return []
    
    def _extract_content_from_result(self, result):
        """Extract meaningful content from search result for invoice data"""
        # If there's a 'content' field, use it directly
        if 'content' in result and result['content']:
            return result['content'].strip()
        
        # Otherwise, try to construct from individual fields
        content_parts = []
        
        # Map common field names (adjust based on your index schema)
        field_mappings = {
            'invoice_id': 'Invoice ID',
            'date': 'Date',
            'customer_name': 'Customer',
            'address': 'Address',
            'product': 'Product',
            'quantity': 'Quantity',
            'unit_price': 'Unit Price',
            'total_amount': 'Total Amount',
            'payment_method': 'Payment Method',
            'status': 'Status'
        }
        
        for field, label in field_mappings.items():
            if field in result and result[field]:
                content_parts.append(f"{label}: {result[field]}")
        
        return " | ".join(content_parts) if content_parts else str(result)

# Task 1: Implement Search Retriever Tool


# Task 2: Build RetrievalQA Chain


def test_exercise2():
    """Test Exercise 2 components"""
    print("=== Testing Exercise 2: LangChain Tools & Retrieval Chain ===\n")
    
    # Test Task 1: Search Retriever Tool
    print("Task 1: Testing Search Retriever Tool")
    search_tool = InvoiceSearchTool()
    
    test_query = "Alice Johnson"
    print(f"Search Query: {test_query}")
    result = search_tool.search_invoices(test_query)
    print(f"Search Result:\n{result}\n")
    
    # Test Task 2: RetrievalQA Chain
    print("Task 2: Testing RetrievalQA Chain")
    qa_system = InvoiceRetrievalQA()
    
    test_question = "What is the total amount for Alice Johnson's invoice?"
    print(f"Question: {test_question}")
    qa_result = qa_system.query(test_question)
    print(f"Answer: {qa_result['answer']}")
    print(f"Sources: {len(qa_result['source_documents'])} documents found\n")

if __name__ == "__main__":
    test_exercise2()