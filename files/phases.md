# Development Phases — 5-Day Plan

Team of 6. Tracks run in parallel; each day ends with a short sync so no track drifts out of step with the others.

**Suggested track ownership** (adjust to actual skills in the room):
- **Backend (2 people)** — FastAPI routing, LLM client + fallback, streaming, Dockerfile
- **Frontend (2 people)** — dashboard shell, shared components, 5 persona views, responsiveness
- **Prompt engineering (1 person)** — writes/tests all 5 system prompts, owns `prompt-design.md` updates
- **AWS + docs (1 person)** — deployment, budget alerts, security pass, assembles Concept Note + Report

---

## Day 1 — Setup & Skeleton

**Goals**: everyone unblocked to start real work by end of day.

- [ ] Repo created, branch strategy agreed, everyone has access
- [ ] Frontend framework decided (React recommended) and AWS deployment target decided (App Runner recommended) — resolve at the team meeting
- [ ] Gemini + Groq API keys obtained; each tested with a bare `curl`/script call outside the app
- [ ] Backend: FastAPI skeleton running locally, `/health` route working
- [ ] Frontend: skeleton app running locally, routing stubbed for 5 persona pages
- [ ] Prompts: first draft of all 5 system prompts written (from `prompt-design.md`)
- [ ] AWS account confirmed, budget alerts configured immediately

**Definition of done**: `git clone` + one setup command gets any team member a running local skeleton.

---

## Day 2 — Core Integration (First Persona End-to-End)

**Goals**: prove the whole pipeline works for one persona before replicating it four more times.

- [ ] Backend: LLM client built (Gemini call + Groq fallback + streaming)
- [ ] Backend: persona config pattern implemented; Study Mentor wired as the first persona
- [ ] Frontend: dashboard with 5 persona cards; Study Mentor's chat view fully working end-to-end (streamed response visible in the UI)
- [ ] Prompts: Study Mentor and Code Reviewer prompts tested against real inputs, refined based on output quality

**Definition of done**: a user can open the app, pick Study Mentor, send a message, and see a streamed response from the real backend.

---

## Day 3 — Remaining Four Personas

**Goals**: all five personas functional locally.

- [ ] Backend: Code Reviewer and Resume Reviewer wired (JSON-schema output personas — simpler, single-turn)
- [ ] Backend: Document Analyzer — PDF upload, chunking, keyword retrieval pipeline built and connected
- [ ] Backend: Research Assistant — multi-source input (PDFs + pasted text) and synthesis prompt wired
- [ ] Frontend: all 5 persona views connected to their respective endpoints; structured-output personas rendered as categorized cards, not raw JSON
- [ ] Prompts: Document Analyzer, Resume Reviewer, Research Assistant prompts tested and refined

**Definition of done**: all 5 personas work locally end-to-end, including file upload for Document Analyzer and Research Assistant.

---

## Day 4 — Containerize, Deploy, Harden

**Goals**: live on AWS with a public URL.

- [ ] Dockerfile written; full app builds and runs correctly in a local container
- [ ] Deployed to AWS (App Runner or Elastic Beanstalk per Day 1 decision); public HTTPS URL obtained
- [ ] Env vars configured on AWS (not in the image, not in git)
- [ ] Security pass: confirm no keys anywhere in frontend code or git history; CORS locked to the real frontend origin
- [ ] Mobile responsiveness pass across all 5 persona views
- [ ] AWS budget alert thresholds double-checked against actual usage so far

**Definition of done**: anyone on the team can open the public URL on their phone and use all 5 personas.

---

## Day 5 — Polish, Docs, Submit

**Goals**: submission-ready.

- [ ] Full bug bash across all 5 personas, desktop and mobile
- [ ] Live AWS URL added to Concept Note and Report
- [ ] Project Report written: overview/tech stack, prompting strategy with sample prompts (pull from `prompt-design.md`), phase-by-phase summary (pull from this file), architecture (pull from `architecture.md`), challenges + fixes, key learnings
- [ ] Every team member does a quick pass reviewing personas they didn't build — the brief requires each member to be able to explain any technical/design decision independently
- [ ] Final check: all 3 deliverables (Concept Note PDF, live app, Report) complete and consistent with each other
- [ ] Submit

**Definition of done**: all three deliverables submitted; every team member has at least skimmed every persona's code and prompt.

---

## Daily Sync Format (5 minutes, end of day)

1. What got done today (each track, 30 seconds)
2. What's blocked
3. Anything that needs to move to tomorrow

## Risk Notes

- **Biggest risk**: Document Analyzer's retrieval pipeline is the most novel piece — if it's not working by end of Day 3, consider simplifying (e.g. smaller top-k, looser scoring) rather than letting it block Day 4's deployment work.
- **Second risk**: AWS deployment issues eating into Day 5 — front-load a throwaway "hello world" deploy on Day 1 if there's any spare capacity, so the real Day 4 deploy isn't the team's first time touching App Runner/Beanstalk.
