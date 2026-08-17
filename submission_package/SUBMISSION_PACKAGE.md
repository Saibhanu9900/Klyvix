# 🎯 Klyvix — Internship Project Submission Package
**Course / Track:** Gen AI & Cloud Computing — Vibe Coding Project  
**Team Composition:** Team of 6  
**Project Title:** Klyvix: AI Command Center — Multi-Persona Intelligence Platform  
**Live Production URL:** [https://klyvix-177846015206.europe-west1.run.app/](https://klyvix-177846015206.europe-west1.run.app/)  
**Interactive API Documentation:** [https://klyvix-177846015206.europe-west1.run.app/docs](https://klyvix-177846015206.europe-west1.run.app/docs)  
**Source Code Repositories:** [https://github.com/Saibhanu9900/Klyvix](https://github.com/Saibhanu9900/Klyvix) | [https://github.com/Ysaibhanu99/Klyvix](https://github.com/Ysaibhanu99/Klyvix)  
**Date of Submission:** August 2026  

---

## 📌 Executive Summary

**Klyvix** is a high-performance, multi-persona AI command center designed to eliminate the limitations of generic chatbots. Built on **FastAPI (Python 3.12)**, **Vanilla JS**, and **Google Cloud Run**, Klyvix orchestrates **6 specialized AI personas** across academic, engineering, and career workflows:

1. **📚 Study Mentor:** Dual-mode tutor (Socratic step-by-step guidance & Direct exam preparation with LaTeX math).
2. **🔍 Code Reviewer:** Multi-dimensional code audit emitting structured JSON across Bugs, Security, Performance, and Style.
3. **👥 Code Colleague:** Collaborative pair-programming partner providing production code and surgical refactorings.
4. **📄 Document Analyzer:** Qdrant Cloud dense vector RAG (768-dim Gemini embeddings) with 0% hallucination grounding.
5. **📋 Resume Reviewer:** Actionable ATS resume optimization with concrete before/after bullet rewrites.
6. **🔬 Research Assistant:** Real-time web-grounded research synthesis with Google Search integration and conflict detection.

The platform is fortified with an **Intelligent Multi-LLM Failover Router** that catches upstream rate limits (HTTP 429) or timeouts on Google Gemini / Mistral and seamlessly switches to **Groq Llama 3.3 70B** without breaking the active Server-Sent Events (SSE) token stream.

---

## 📂 Deliverables Index in This Package

| # | File Name | Document Type | Description |
| :--- | :--- | :--- | :--- |
| **1** | [**`Klyvix_Executive_Summary.pdf`**](file:///E:/klyvix/submission_package/Klyvix_Executive_Summary.pdf) | 1-Page PDF | Executive Pitch Sheet, Core Value Proposition, Metrics & Evaluator Reference. |
| **2** | [**`Klyvix_Concept_Note.pdf`**](file:///E:/klyvix/submission_package/Klyvix_Concept_Note.pdf) | 3-Page PDF | Complete Concept Note, Problem Statement, Stack Rationale & Feature Comparison Matrix. |
| **3** | [**`Klyvix_Project_Report.pdf`**](file:///E:/klyvix/submission_package/Klyvix_Project_Report.pdf) | 3-Page PDF | Final Technical Project Report, Challenges, Solutions, Learnings & Future Roadmap. |
| **4** | [**`Klyvix_Architecture_Document.pdf`**](file:///E:/klyvix/submission_package/Klyvix_Architecture_Document.pdf) | 2-Page PDF | System Topology, SSE Streaming Pipeline, Qdrant Vector RAG & Cloud Run Blueprint. |
| **5** | [**`Klyvix_Testing_Report.pdf`**](file:///E:/klyvix/submission_package/Klyvix_Testing_Report.pdf) | 2-Page PDF | QA Test Suite Results (100% Pass), Persona Benchmarks & Failover Stress Tests. |
| **6** | [**`Klyvix_API_Guide.pdf`**](file:///E:/klyvix/submission_package/Klyvix_API_Guide.pdf) | 2-Page PDF | REST & SSE API Specification, Endpoints Reference, JSON Schemas & Error Codes. |
| **7** | [**`screenshots/`**](file:///E:/klyvix/submission_package/screenshots) | 16 PNGs | High-Resolution Desktop (1920x1080), Mobile, Live Interaction & Swagger Docs Screenshots. |
| **8** | [**`Klyvix_Internship_Submission.zip`**](file:///E:/klyvix/Klyvix_Internship_Submission.zip) | ZIP Archive | Complete single-file archive containing all documents, code references, and screenshots. |

---

## ⚡ Quick Evaluation & Testing Guide

Reviewers can verify all aspects of the live project using the following steps:

1. **Visit Live Web App:** [https://klyvix-177846015206.europe-west1.run.app/](https://klyvix-177846015206.europe-west1.run.app/)
2. **Test Theme & Responsive Layout:** Toggle Dark/Light mode using the `[*] theme` button in the sidebar. Resize to mobile viewport to verify the mobile hamburger navigation.
3. **Test Study Mentor:** Enter `study_mentor` &rarr; Ask *"Explain Binary Search"* &rarr; Observe Socratic guidance and LaTeX math equations.
4. **Test Code Reviewer:** Enter `code_reviewer` &rarr; Paste a sample Python/JS snippet &rarr; Observe structured JSON cards categorized into Bugs, Security, Performance, and Style.
5. **Test Document Analyzer:** Enter `document_analyzer` &rarr; Attach any PDF &rarr; Ask questions strictly grounded in the document.
6. **Test API Documentation:** Navigate to [https://klyvix-177846015206.europe-west1.run.app/docs](https://klyvix-177846015206.europe-west1.run.app/docs) to execute endpoints interactively.

---

## 🏆 Project Rubric & Self-Assessment

| Evaluation Criteria | Target Standard | Achieved in Klyvix | Status |
| :--- | :--- | :--- | :--- |
| **GenAI Innovation** | Meaningful Prompt Engineering beyond cosmetic roleplay | 6 functionally differentiated personas with custom schemas & RAG grounding | **Exceeds Expectations** |
| **Cloud Deployment** | Production cloud hosting with HTTPS & auto-scaling | Deployed on Google Cloud Run (`europe-west1`) with Docker & TLS 1.3 | **Exceeds Expectations** |
| **Vector RAG Implementation** | Dense semantic vector database retrieval | Qdrant Cloud with 768-dim Gemini embeddings and chunk citations | **Exceeds Expectations** |
| **Fault Tolerance & Reliability** | Zero downtime during LLM quota spikes | Automated multi-provider failover (Gemini &rarr; Mistral &rarr; Groq) | **Exceeds Expectations** |
| **UI/UX & Responsiveness** | Fast, responsive interface | Sub-50ms render, real-time SSE token streaming, LaTeX & syntax highlighting | **Exceeds Expectations** |
| **Documentation & Quality** | Comprehensive documentation package | Complete suite of 6 executive PDF reports, testing audits, and 16 screenshots | **Exceeds Expectations** |
