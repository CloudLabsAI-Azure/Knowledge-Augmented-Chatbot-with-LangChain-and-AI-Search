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

## Task 2: Build RetrievalQA Chain

In this task, you will create a RetrievalQA chain by connecting your search retriever to an Azure OpenAI language model. You will configure the chain to retrieve top-k search snippets and pass them along with user queries to the model, enabling the chatbot to provide informed, relevant answers.

## Summary

In this exercise, you connected Azure AI Search with LangChain by wrapping your search index as a retriever and building a RetrievalQA chain using Azure OpenAI. These components worked together to enable the chatbot to retrieve relevant content and generate context-aware answers based on your indexed data.