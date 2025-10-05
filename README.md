# E-Commerce Customer Support Agentic RAG (from scratch)

This repository contains the source code and project structure for a modular, scalable E-Commerce Customer Support AI Agent. The agent is designed to provide intelligent, automated support for customers and can integrate with various APIs and tools for seamless functionality.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Rasa](https://img.shields.io/badge/Rasa-3.x-orange)](https://rasa.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

# Introduction
An AI-powered customer support agentic RAG for e-commerce, built with **Rasa** and **FakeStore API** as chatbot framework and e-commerce API, respectively. It handles order tracking, product inquiries(as a customer support bot), and order returns, with seamless integration for mock data.

What is Agentic RAG?
Agentic RAG transforms passive retrieval into active, multi-step reasoning where the system:
- Autonomously decides what information to retrieve
- Plans multi-hop queries across knowledge sources
- Self-corrects and iteratively refines searches
- Uses tools (calculators, APIs, databases) to enhance responses


# Why Agentic RAG for E-Commerce Support AI?

Current Limitations
- Traditional RAG: Single-pass retrieval -> limited context
- Static responses -> no dynamic problem-solving
- No cross-document reasoning

Agentic RAG Advantages
- Complex Query Handling: "Find me a laptop under $1000 that's better than my current Dell XPS 13"
- Multi-Step Reasoning: Check specs → compare prices → verify compatibility → suggest alternatives
- Self-Correction: "That didn't work, let me try a different approach."
- Tool Usage: Calculate discounts, check inventory, estimate shipping

**Live Demo** (WIP):

## Features
- **Order Tracking**: "Where is my order #123?" → Real-time status from FakeStore API.
- **Product Stock Checks**: "Is the Fjallraven Backpack in stock?" → Inventory lookup.
- **Returns/Refunds**: Guided return process via dynamic forms.
- **RestockNotification**: Notify the customer when the product is back in stock
- **Rasa Integration**: NLP intents, entity extraction, and dialogue management.
- **Integrated LLM**: Integrated DeepSeek-R1 for Reasoning, i.e., to handle ambiguous queries and generate dynamic responses.
- **Mock Data**: No need for a real e-commerce backend.

## Tech Stack
- **NLP & Dialogue**: Rasa (NLU + Core)
- **Backend**: Python, Flask, PostgreSQL
- **Integrations**:
    FakeStore API (mock data),
    Shopify/Stripe API connections(Future Work)
    Gmail/SMTP email automation(Future Work)
- **Deployment**: Docker, AWS/Heroku
- **Frontend**: Streamlit with custom CSS design
- **LLM for Reasoning**: DeepSeek-R1
- **Vector Database**: Pinecone



## Roadmap/Milestones

### Completed
- [x] Core Rasa/DeepSeek integration
- [x] Basic order tracking & returns
- [x] Streamlit UI framework
- [x] FakeStore API integration
- [x] Context-aware conversation handling
- [x] LLM Integration for Reasoning build part(deployment WIP)
- [x] Database Integration:
  - PostgreSQL for order history and product return/refund enquiry
  - Redis for real-time session storage
  - User preference persistence

### Work-in-progress Items:


- [ ] ** RAG Core System:
    - Document processing + vector store
    - RAG Ingestion Pipeline
    - Basic Retrieval: Product specs and policy documents
    - Fallback Mechanism: When RAG doesn't find relevant info
    - Agentic RAG: To add by adding decision-making capabilities to its own search refinement.


### Advanced Features that are in plan
- [ ] **Self-Improvement System (Part of Long-term Optimization)**
  - Rasa Interactive Learning integration
  - Hugging Face Transformers fine-tuning
  - User feedback analysis pipeline

- [ ] **External Service Integration**
  - Shopify/Stripe API connections
  - Gmail/SMTP email automation
  - Warehouse inventory system hooks

- [ ] **Enhanced Autonomy**
  - Automated refund processing
  - Proactive shipment updates
  - Smart cart recovery workflows

- [ ] **Production Readiness**
  - Docker/Kubernetes deployment
  - Prometheus/Grafana monitoring
  - Load testing & scaling

  ### Authentication Flow Design
![Authentication Flow Design](https://github.com/user-attachments/assets/c9ce50e7-a0e0-43ee-93c1-9813a1f9628f)

### System Design Architecture:
Here's the Modular Agentic RAG System Architecture that pairs OpenAI's embeddings model "text-embedding-3-large" with DeepSeek-R1 for generation in this RAG pipeline.
- OpenAI is used solely for embeddings and hypothetical generation in HyDE (via ChatOpenAI for the zero-shot doc creation).
- The pipeline then switches to DeepSeek-R1 (via a compatible wrapper like ChatDeepSeek or a custom integration) for the final augmentation and response generation.
This leverages the strengths of both: OpenAI's superior embedding quality for retrieval (with HyDE boosting relevance on challenging queries), and DeepSeek's cost efficiency for high-volume generation.

<img width="3840" height="3715" alt="updated_Architecture_RAG " src="https://github.com/user-attachments/assets/8a3b43ae-ced8-44a0-ae01-3dbfea85f2ed" />





