# Griffin: Financial Data Q&A Assistant using Graph RAG

A financial question-answering system using Retrieval-Augmented Generation (RAG) powered by LangGraph.

## Table of Contents

- [Motivation](#motivation)
- [Overview](#overview)
- [Why Graph RAG?](#why-graph-rag)
- [Key Capabilities](#key-capabilities)

## Motivation

Traditional financial Q&A systems suffer from two fundamental limitations: they either rely on static, rapidly outdated training data, or they retrieve flat, disconnected text chunks that lack the relational context critical to financial analysis. A question like _"How does Company X's debt-to-equity ratio compare to its sector peers over the last four quarters?"_ requires traversing relationships across entities, time periods, and metrics — something conventional vector-similarity RAG handles poorly.

Griffin addresses this gap by combining **graph-based knowledge representation** with **retrieval-augmented generation**, enabling structured reasoning over interconnected financial data rather than keyword-matched document fragments.

## Overview

Griffin is an intelligent financial assistant built on a Graph RAG architecture orchestrated by [LangGraph](https://github.com/langchain-ai/langgraph). It models financial entities (companies, sectors, indicators, instruments) and their relationships as a knowledge graph, then leverages that structure at query time to retrieve contextually rich, multi-hop evidence for grounded LLM responses.

### Why Graph RAG?

| Approach | Limitation | Griffin's Advantage |
|---|---|---|
| **Parametric LLM** | Stale training data; hallucination risk on numerical facts | Grounds responses in retrieved, up-to-date structured data |
| **Vector RAG** | Flat chunk retrieval; no relational reasoning | Traverses entity relationships for multi-hop, contextual answers |
| **SQL/API lookup** | Rigid queries; no natural-language interface | Accepts freeform questions and dynamically constructs graph traversals |

## Key Capabilities

- **Market Data** — Stock prices, trading volumes, financial ratios
- **Company Analysis** — Revenue trends, earnings reports, financial health
- **Economic Indicators** — GDP, inflation, interest rates, market trends
- **Investment Concepts** — Portfolio theory, risk management, trading strategies
- **Financial Education** — Definitions, explanations, best practices
