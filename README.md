# E-Commerce Customer Support Agentic RAG (from scratch)

This repository contains the source code and project structure for a modular, scalable E-Commerce Customer Support AI Agent. The agent is designed to provide intelligent, automated support for customers and can integrate with various APIs and tools for seamless functionality.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Rasa](https://img.shields.io/badge/Rasa-3.x-orange)](https://rasa.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

# Introduction
An AI-powered customer support agentic RAG for e-commerce, built with **Rasa** and **FakeStore API** as chatbot framework and e-commerce API respectively. Handles order tracking, product inquiries, and returns, with seamless integration for mock data.


# Why Agentic RAG for Medical Chatbot?

Current Limitations:
- Static Retrieval: One-and-done knowledge fetching
- No Reasoning: Cannot chain multiple retrievals for complex queries
- Limited Validation: Basic safety checks but no iterative verification
- Passive Architecture: Doesn't adapt retrieval strategy to query complexity

Agentic RAG Advantages:
- Multi-hop Reasoning: "What's the best medication for hypertension in elderly patients with diabetes?"
- Self-Correction: Detects insufficient information and requeries
- Dynamic Source Selection: Chooses between KB, APIs, or vector search based on context
- Verification Loops: Cross-references multiple sources for critical information

**Live Demo** (WIP): 

![Demo](demo.gif) <!-- Add a GIF later -->

## Features ✨
- **Order Tracking**: "Where is my order #123?" → Real-time status from FakeStore API.
- **Product Stock Checks**: "Is the Fjallraven Backpack in stock?" → Inventory lookup.
- **Returns/Refunds**: Guided return process via dynamic forms.
- **RestockNotification**: Notify the customer when the product is back in stock
- **Rasa Integration**: NLP intents, entity extraction, and dialogue management.
- **Integrated LLM**: Integrated DeepSeek-R1 for Reasoning, i.e., to handle ambiguous queries and generate dynamic responses.
- **Mock Data**: No need for a real e-commerce backend.

## Tech Stack 🛠️
- **NLP & Dialogue**: Rasa (NLU + Core)
- **Backend**: Python, Flask, PostgreSQL
- **Integrations**:
    FakeStore API (mock data),
    Shopify/Stripe API connections,
    Gmail/SMTP email automation
- **Deployment**: Docker, AWS/Heroku
- **Frontend**: Streamlit with custom CSS design
- **LLM for Reasoning**: DeepSeek-R1


## 🚧 Roadmap

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

### Immediate Priorities/Work-in-progress Items:


- [ ] ** RAG Core System:
    - Document processing + vector store
    - Basic Retrieval: Product specs and policy documents
    - Fallback Mechanism: When RAG doesn't find relevant info


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
<img width="3840" height="2095" alt="E-commerce AI Agent Arch " src="https://github.com/user-attachments/assets/d510630b-4f46-4847-a1bf-6f4f7e87d8cd" />


### Future Exploration
- [ ] Have thought of 4 amazing features or further integrations that can be integrated in the future, but I'm not willing to disclose them now. If you're an Interviewer or a product owner, I would love to share those future scopes in an offline conversation.




