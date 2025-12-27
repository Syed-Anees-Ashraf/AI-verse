Good catch — you’re right. What you want now is **not a design doc**, but a **machine-executable build manual**.
I’m going to rewrite this as a **STRICT, UNAMBIGUOUS, CHECKLIST-DRIVEN INSTRUCTION SET** that a **vibe coding agent** (or junior dev) can follow *literally*, without “interpreting intent”.

I will:

* Specify **exact files to create**
* Specify **exact functions/classes**
* Specify **exact inputs & outputs**
* Specify **how to test each thing**
* Specify **when to STOP if wrong**

No abstractions. No “shoulds”. Only **DO THIS → EXPECT THIS**.

---

# VENTUREPILOT AI

## 🔒 LOCKED BUILD INSTRUCTIONS (ULTRA-SPECIFIC)

> **Assumptions (NON-NEGOTIABLE):**
>
> * Data is already collected and stored locally
> * LLM access is available
> * Vector DB is available
> * Backend is Python
> * Frontend can be basic (React or simple HTML is fine)

---

# PHASE 0 — REPOSITORY & BOOTSTRAP (DO EXACTLY THIS)

## 0.1 Create Folder Structure

Create **exactly** this:

```
venturepilot-ai/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   │
│   ├── storage/
│   │   ├── vector_store.py
│   │   ├── metadata_store.py
│   │
│   ├── rag/
│   │   ├── retriever.py
│   │
│   ├── agents/
│   │   ├── startup_agent.py
│   │   ├── policy_agent.py
│   │   ├── investor_agent.py
│   │   ├── market_agent.py
│   │   ├── news_agent.py
│   │   ├── strategy_agent.py
│   │
│   ├── orchestration/
│   │   └── orchestrator.py
│   │
│   └── api/
│       ├── onboarding.py
│       ├── dashboard.py
│       └── chat.py
│
├── data/
│   ├── policies/
│   ├── investors/
│   ├── news/
│   └── reports/
│
└── README.md
```

❌ Do not rename anything
❌ Do not merge folders

---

## 0.2 Boot Server

**backend/main.py**

* Create FastAPI app
* Add a `/health` endpoint returning `{ "status": "ok" }`

### TEST

Run server → visit `/health`
✔️ Response must be exactly `{ "status": "ok" }`
❌ If server fails → STOP

---

# PHASE 1 — VECTOR STORAGE & RETRIEVAL (ABSOLUTE FOUNDATION)

## 1.1 Implement Vector Storage

**File:** `backend/storage/vector_store.py`

Create a class:

```
class VectorStore:
    def add_documents(documents: list[dict]) -> None
    def search(query: str, filters: dict, k: int) -> list[dict]
```

Each document **MUST** have:

```
{
  "text": str,
  "category": "policy" | "investor" | "news" | "report",
  "timestamp": ISO_DATE,
  "geography": str,
  "source": str
}
```

❌ If any document is missing metadata → reject it

---

## 1.2 Load Data into Vector Store

In `main.py`, on startup:

* Load ALL files from:

  * `/data/policies` → category = policy
  * `/data/investors` → category = investor
  * `/data/news` → category = news
* Chunk text BEFORE embedding

---

## 1.3 Implement Retriever

**File:** `backend/rag/retriever.py`

Create function:

```
def retrieve_context(
    query: str,
    category: str | None,
    geography: str | None,
    recency_days: int | None
) -> list[str]
```

Filtering rules:

* If category provided → only that category
* If recency provided → timestamp must be within range
* Sort by semantic relevance + recency

---

### TEST (MANDATORY)

Run these queries:

* “Indian fintech government schemes”
* “AI SaaS seed stage investors”

✔️ Results must match category
✔️ Recent docs must appear first

❌ If irrelevant text appears → STOP

---

# PHASE 2 — STARTUP UNDERSTANDING AGENT (NO GUESSWORK)

## 2.1 Input Schema

**Input JSON (STRICT):**

```
{
  "description": string,
  "domain": string,
  "stage": string,
  "geography": string,
  "customer_type": string
}
```

---

## 2.2 Startup Agent

**File:** `backend/agents/startup_agent.py`

Create function:

```
def analyze_startup(input_data: dict) -> dict
```

LLM MUST output **ONLY JSON**:

```
{
  "problem": string,
  "value_proposition": string,
  "market_category": string,
  "target_customers": string,
  "assumed_competitors": list[string],
  "risk_factors": list[string]
}
```

❌ If output is not valid JSON → retry once → else FAIL

---

### TEST

Give 2 different startup descriptions.

✔️ Output fields must always exist
✔️ Competitors must differ per domain

---

# PHASE 3 — DOMAIN AGENTS (ONE BY ONE)

## 3.1 Policy Agent

**File:** `policy_agent.py`

Function:

```
def analyze_policy(startup_profile: dict) -> dict
```

Steps:

1. Call retriever with:

   * category = "policy"
   * geography = startup geography
2. Pass retrieved text to LLM
3. Output JSON:

```
{
  "relevant_policies": list[string],
  "eligible_schemes": list[string],
  "regulatory_risks": list[string]
}
```

---

### TEST

Change startup domain → output MUST change.

---

## 3.2 Investor Agent

**File:** `investor_agent.py`

Function:

```
def match_investors(startup_profile: dict) -> list[dict]
```

Each investor entry:

```
{
  "name": string,
  "match_score": number (0–100),
  "reason": string,
  "past_investments": list[string]
}
```

Sort descending by `match_score`.

---

### TEST

Ensure:
✔️ Scores vary
✔️ Reasons reference past investments

---

## 3.3 Market Agent

**File:** `market_agent.py`

Output:

```
{
  "market_size_estimate": string,
  "growth_signals": list[string],
  "saturation_risks": list[string],
  "emerging_trends": list[string]
}
```

---

## 3.4 News Agent

**File:** `news_agent.py`

Output:

```
{
  "opportunities": list[string],
  "risks": list[string],
  "recent_events": list[string]
}
```

Recency MUST be enforced.

---

# PHASE 4 — STRATEGY SYNTHESIS (NO DIRECT RETRIEVAL)

## 4.1 Strategy Agent

**File:** `strategy_agent.py`

Input:

* Outputs of ALL other agents

Output:

```
{
  "fundraising_readiness": "low|medium|high",
  "key_recommendations": list[string],
  "next_actions": list[string]
}
```

❌ This agent must NOT call retriever
❌ It only reasons over agent outputs

---

# PHASE 5 — ORCHESTRATION (STRICT ORDER)

**File:** `orchestrator.py`

Execution order (DO NOT CHANGE):

1. Startup Agent
2. Policy Agent
3. Investor Agent
4. Market Agent
5. News Agent
6. Strategy Agent

Final output:

```
{
  "startup_profile": {...},
  "policy": {...},
  "investors": [...],
  "market": {...},
  "news": {...},
  "strategy": {...}
}
```

---

### TEST

Log each agent call.
✔️ All agents must run exactly once.

---

# PHASE 6 — API CONTRACT (NO LOGIC HERE)

Endpoints:

### `/onboard`

* Input: raw startup input
* Output: structured startup profile

### `/dashboard`

* Input: startup profile
* Output: full orchestrated output

### `/chat`

* Input: user question + startup profile
* Output: LLM response using retriever + agents

---

# PHASE 7 — FRONTEND (MINIMUM VIABLE)

Pages:

1. Startup input form
2. Confirmation page
3. Dashboard (cards)
4. Chat box

---

# FINAL SYSTEM ACCEPTANCE TEST (NON-NEGOTIABLE)

✔️ Startup understanding is editable
✔️ Investor list is ranked + explainable
✔️ Policies are geography-specific
✔️ News is recent
✔️ Strategy references multiple agents
✔️ Removing data does NOT crash system


