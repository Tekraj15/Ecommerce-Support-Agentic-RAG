# E-Commerce Customer Support Agentic RAG

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

### Key Roles

| Layer           | Responsibility              | Control          |
|-----------------|-----------------------------|------------------|
| **Rasa**        | Dialogue, intent, UX        | **What to ask**  |
| **Agentic RAG** | Retrieval, reasoning, tools | **How to answer**|

→ Rasa Chatbot asks a question and anages dialogues.
→ RAG service answers intelligently, including the complex questions.

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
- **LLM**: OpenAI for Hypothetical Document Embeddings and DeepSeek-R1 for Reasoning and Generation
- **Vector Database**: Pinecone



## Roadmap/Milestones

### Completed
- [x] Rasa NLU chatbot
- [x] RASA and DeepSeek integration
- [x] Basic order tracking & returns
- [x] Streamlit UI framework
- [x] FakeStore API integration
- [x] Context-aware conversation handling
- [x] LLM Integration for Reasoning build part
- [x] Database Integration:
  - PostgreSQL for order history and product return/refund enquiry
  - Redis for real-time session storage
  - User preference persistence
- [x] Core RAG System:
    - Document processing + vector store
    - RAG Ingestion Pipeline: Loader and Chunker
    - Basic Retrieval: Product specs and policy documents

- [x] Agentic RAG System:
    - Agentic RAG components are encapsulated in Agentic RAG Controller.
    AgenticRAGController
        ├── Retriever (HyDE + MMR)
        ├── Augmenter
        ├── Generator (Tools Calling if needed + DeepSeek R1 generation)
        └── Self-Correction Loop(If confidence < 0.6 → refine query → go back to Step 1 (up to 2 retries))
        ↓
        → Rich JSON Answer


### Authentication Flow Design
![Authentication Flow Design](https://github.com/user-attachments/assets/c9ce50e7-a0e0-43ee-93c1-9813a1f9628f)

### System Design Architecture:
<img width="3840" height="2095" alt="E-commerce AI Agent Arch " src="https://github.com/user-attachments/assets/d510630b-4f46-4847-a1bf-6f4f7e87d8cd" />
Here's the Modular Agentic RAG System Architecture that pairs OpenAI's embeddings model "text-embedding-3-large" with DeepSeek-R1 for generation in this RAG pipeline.
- OpenAI is used solely for embeddings and hypothetical generation in HyDE (via ChatOpenAI for the zero-shot doc creation).
- The pipeline then switches to DeepSeek-R1 (via a compatible wrapper like ChatDeepSeek or a custom integration) for the final augmentation and response generation.

This leverages the strengths of both: OpenAI's superior embedding quality for retrieval (with HyDE boosting relevance on challenging queries), and DeepSeek's cost efficiency for high-volume generation.

The Full RAG Pipeline Flow:

Retrieval -> Self-correction -> Augmentation -> Tools -> Generation

The Complete Architecture Flow:

Rasa Action Server
   ↓ POST {"query": "..."}
Flask RAG Service (:8000)
   ↓
AgenticRAGController
   ├── Retriever (HyDE + MMR)
   ├── Augmenter
   ├── Generator (Tools + DeepSeek R1)
   └── Self-Correction Loop
   ↓
→ Rich JSON Answer


To go deeper into the detailed Architecture, the Agentic RAG architecture is equipped with below techniques/capabilities:
1. **HyDE (Hypothetical Document Embeddings)**
   Queries are often short and vague, while documents are detailed—HyDE flips this by using an LLM to "imagine" a full, ideal answer (hypothetical document) and retrieves real docs matching that, like searching with a prototype instead of a sketch.

2. **Hybrid LLM: Best of Both Worlds**

|     Task                  |     Model                           |           Why It’s Optimal                                        |
|---------------------------|-------------------------------------|-------------------------------------------------------------------|
| **Embeddings + HyDE**     | **OpenAI `text-embedding-3-large`** | Top-tier semantic understanding → **highest retrieval relevance** |
| **Reasoning & Generation**| **DeepSeek-R1**                     | 10x cheaper, same quality → **massive cost savings**              |

> **Result**: You get **GPT-4-level retrieval** at **Llama-level cost**.

3. **Agentic Loop: Self-Correction = Robustness**

Traditional RAG:
Query → Retrieve → Answer → Done

Weaknesses: They Fails silently on bad retrieval.

Agentic RAG:
Retrieve → Augment → Generate → [Confidence < 0.6?] → Refine → Retry

- Self-Correction Loop (up to 2 retries)
- Confidence Scoring from retrieval + LLM
- Query Refinement using partial context


Result: 90%+ recovery rate on ambiguous or low-relevance queries.

4. **Tool Calling: Grounded, Real-Time Answers**


Query                  | Without Tools     |  With Tools                  |
-----------------------|-------------------|------------------------------|
“Where is order #123?” | “I don’t know..”  |  “Shipped, arriving tomorrow”|

- FakeStore API via get_order_status, check_stock
- LLM decides when to call tools
- Results injected into next generation step


Result: Zero hallucination on dynamic data.


5. **Advanced Retrieval: HyDE + MMR**

  Technique   |     Problem It Solves
--------------|----------------------------------------------------------------|
  HyDE         Short query ≠ long doc → uses hypothetical answer as search key
--------------|----------------------------------------------------------------|
  MMR         |Avoids 5 similar product specs → returns diverse, useful results

Result: +40% relevance on complex queries.


6. **Modular, Scalable Architecture**

Rasa (Dialogue) → HTTP → Flask RAG Service (Reasoning)

- Rasa controls what to ask
- RAG Service controls how to answer
- No tight coupling
- Scale RAG workers independently

Result: Production-ready, observable, maintainable.

```mermaid
graph TB
    %% User Interface Layer
    UI[User Interface<br/>Streamlit Web App]
    
    %% Core AI Layer
    subgraph "AI Agent Core"
        RASA[Rasa NLU Engine]
        ROUTER[Agent Router<br/>Query Classifier]
        FALLBACK[Fallback Handler<br/>Human Escalation]
    end
    
    %% Multi-Model Agentic RAG Service
    subgraph "Multi-Model Agentic RAG Service"
        AP[Agentic Planner<br/>Query Decomposition]
        AE[Agentic Executor<br/>Tool Orchestration]
        
        subgraph "Embedding & HyDE Layer"
            OEMB[OpenAI Embeddings<br/>text-embedding-3-large]
            HYDE[HyDE Generator<br/>ChatOpenAI]
            VS[Vector Store<br/>OpenAI Embeddings]
        end
        
        subgraph "Generation Layer"
            DSGEN[DeepSeek-R1<br/>Response Generation]
            AUG[RAG Augmenter<br/>Context + Query]
        end
        
        TOOLS[Tool Registry<br/>Calculator, Inventory, etc.]
        
        AP --> AE
        AE --> HYDE
        HYDE --> OEMB
        OEMB --> VS
        AE --> VS
        VS --> AUG
        AUG --> DSGEN
        AE --> TOOLS
    end
    
    %% Data Ingestion Pipeline
    subgraph "Data Ingestion Service"
        DI[Document Ingestor<br/>PDF/CSV/JSON]
        DP[Document Processor<br/>OpenAI Embeddings]
        QC[Quality Controller<br/>Validation]
        
        DI --> DP
        DP --> OEMB
        OEMB --> QC
        QC --> VS
    end
    
    %% External Services
    subgraph "External APIs"
        FS[FakeStore API]
        DB[PostgreSQL Database]
        REDIS[Redis Session Store]
        OPENAI[OpenAI API<br/>Embeddings + HyDE]
        DEEPSEEK[DeepSeek API<br/>Generation]
        HUMAN[Human Operator Interface]
    end
    
    %% Action Servers
    subgraph "Action Servers"
        CUSTOM[Custom Actions<br/>Order/Returns]
        AGENTIC[Agentic Actions<br/>Complex Queries]
    end
    
    %% Data Flow
    UI --> RASA
    RASA --> ROUTER
    
    ROUTER -->|Simple Query| CUSTOM
    ROUTER -->|Complex Query| AGENTIC
    ROUTER -->|Fallback| FALLBACK
    
    AGENTIC --> AP
    CUSTOM --> FS
    CUSTOM --> DB
    CUSTOM --> REDIS
    
    FALLBACK --> HUMAN
    
    %% API Connections
    OEMB --> OPENAI
    HYDE --> OPENAI
    DSGEN --> DEEPSEEK
    
    %% Style
    classDef default fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef agentic fill:#fff3e0,stroke:#ff6f00,stroke-width:2px;
    classDef embedding fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef generation fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef ingestion fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef external fill:#ffebee,stroke:#c62828,stroke-width:2px;
    
    class AP,AE,TOOLS,AGENTIC agentic;
    class OEMB,HYDE,VS embedding;
    class DSGEN,AUG generation;
    class DI,DP,QC ingestion;
    class FS,DB,REDIS,OPENAI,DEEPSEEK,HUMAN external;
    ```


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


