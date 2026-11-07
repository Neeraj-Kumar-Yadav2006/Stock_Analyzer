# Product Requirements Document (PRD)

# Autonomous Multi-Agent Financial Research & Intelligence System

---

## 1. Problem Statement

Financial analysts manually:
- check stock prices
- read multiple news articles
- summarize information
- prepare daily reports

This process is:
- slow
- repetitive
- not scalable

There is a need for an automated AI system that can collect financial data, analyze it, and generate reports with minimal human effort.

---

## 2. Goal

Build an Agentic AI system that:

- fetches stock data automatically
- collects related news
- summarizes insights using LLMs
- performs sentiment analysis
- generates structured reports
- displays everything in a dashboard

---

## 3. Target Users

Primary:
- finance students
- retail investors
- analysts

Secondary:
- research teams
- investment firms (simulation)

---

## 4. Success Metrics

Project is successful if:

- Report generated in < 10 seconds
- Summaries are relevant and readable
- Works for multiple stocks
- Fully automated pipeline
- Multi-agent workflow implemented
- Stable demo

---

## 5. Scope

### In Scope
- Stock API integration
- News API integration
- LLM summarization
- Sentiment analysis
- Report generation
- FastAPI backend
- Streamlit dashboard
- Multi-agent pipeline

### Out of Scope
- Training ML models
- Stock price prediction
- Trading bots
- Complex deep learning research
- Fancy UI

---

## 6. Functional Requirements

### FR1 – Stock Data Retrieval
System must:
- accept stock ticker
- fetch latest price
- fetch basic metrics

Output:
{
  "price": 180.2,
  "change": 1.3
}

---

### FR2 – News Collection
System must:
- fetch top N articles
- extract headlines and content

---

### FR3 – Summarization Agent
System must:
- summarize multiple articles
- generate 3–5 line summary

---

### FR4 – Sentiment Agent
System must:
- classify sentiment (positive/neutral/negative)
- provide confidence score

---

### FR5 – Report Agent
System must:
- combine price + news + sentiment
- generate structured financial report

Example:

Stock: AAPL  
Price: $180  
Sentiment: Positive  
Summary: ...  

---

### FR6 – Dashboard
User must:
- input stock ticker
- view report
- view past reports

---

### FR7 – Multi-Agent Workflow
System must include:
- Data Agent
- Analysis Agent
- Report Agent

Agents execute sequentially.

---

## 7. Non-Functional Requirements

Performance:
- Response < 10 seconds

Reliability:
- Handle API failures gracefully

Scalability:
- Support multiple stocks

Maintainability:
- Modular code
- Separate agent files
- Structured Audit Logging
- Traceability
- Error Attribution

Usability:
- Simple UI

---

## 8. System Architecture

User
  ↓
Frontend (Streamlit)
  ↓
FastAPI Backend
  ↓
Planner Agent
  ↓
Data Agent → Stock API + News API
  ↓
Analysis Agent → LLM
  ↓
Report Agent → LLM
  ↓
Database
  ↓
Return Report

---

## 9. Tech Stack

Backend:
- Python
- FastAPI

AI:
- LLM API
- LangChain (optional)

Data:
- yfinance / news API
- SQLite

Frontend:
- Streamlit

Deployment:
- Docker (optional)

---

## 10. Milestones

### Milestone 1 (10 days – 20%)
- Stock API
- News API
- Summarization
- FastAPI endpoint
- Simple UI

### Milestone 2 (Month 1)
- Sentiment agent
- Report generator
- Agent pipeline

### Milestone 3 (Month 2)
- Multi-agent system
- Database
- Automation
- Final polish

---

## 11. Team Roles

Member 1:
Backend + APIs

Member 2:
Data + storage

Member 3:
LLM + Agents + Orchestration

Member 4:
Frontend + Dashboard

---

## 12. Risks & Mitigation

API Limits: Use TTL-based caching.

Slow Responses: Optimize prompts and use parallel execution.

Data Reliability: Use schema validation and circuit breakers.

AI Hallucinations: Use "Grounding" (require source citations).

Security: Use environment variables and sanitize logs.

Scope Creep: Strictly follow PRD milestones.

Complexity: Build incrementally.

---

## 13. Resume Value

This project demonstrates:

- Agentic AI systems
- LLM integration
- Backend engineering
- API orchestration
- Automation pipelines
- System design

Suitable for enterprise and finance tech roles.