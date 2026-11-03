# Provider Account Setup, Credentials & Billing Governance Guide
**Project:** SK Sutras by Shri Shripad Kulkarni — Four-Agent AI-Assisted Platform  
**Technology Implementation Partner:** [Hiranyam AI Labs](https://hiranyamai.com/)  
**Document Standard:** Strictly Confidential & Proprietary  

---

> [!IMPORTANT]
> **Mandatory Distinction: Consumer Chatbot Subscriptions vs Developer API Access**  
> Consumer paid subscriptions (such as ChatGPT Plus, Claude Pro, or Google One AI Premium / Gemini Advanced) are designed solely for interactive consumer chat interfaces. **They do NOT include developer API access.**  
> Dedicated commercial developer API accounts must be established with Google, OpenAI, and Anthropic to enable autonomous agent execution.

---

## 1. Architectural Role Allocation

The SK Sutras platform coordinates four distinct scholarly agents through LangGraph:

| Agent Role | Model Allocation | Provider Platform | Primary Responsibility |
| :--- | :--- | :--- | :--- |
| **Agent 1: Narada Specialist** | Google Gemini 1.5 Pro | Google AI Studio / Vertex AI | 84 Narada Bhakti Sutras analysis, ecstatic devotion, word breakdown |
| **Agent 2: Shandilya Specialist** | OpenAI GPT-4o | OpenAI Platform | 100 Shandilya Bhakti Sutras analysis, epistemological inquiry |
| **Agent 3: Sutrakar Master Author** | Anthropic Claude 3.5 Sonnet | Anthropic Console | Synthesis arbitration, non-compulsory matching, original Sanskrit Udyoga Sutras composition |
| **Agent 4: Independent Validator** | OpenAI GPT-4o (Separately Configured) | OpenAI Platform | 7-gate critical verification, Anushtubh Chandas metre validation, targeted revision feedback |

---

## 2. Step-by-Step Provider Onboarding & API Key Generation

### A. Google Gemini (Agent 1)
1. **Portal URL:** Navigate to [Google AI Studio](https://aistudio.google.com/) or [Google Cloud Console](https://console.cloud.google.com/).
2. **Account Creation:** Sign in with your designated business Google Account (`notifications@hiranyamai.com` or project owner account).
3. **API Key Generation:**
   - Click **Get API key** > **Create API key in new project**.
   - Copy the generated key string securely.
4. **Billing & Spending Caps:**
   - Link an active payment method in Google Cloud Billing.
   - In Google Cloud Console, navigate to **Billing** > **Budgets & Alerts**.
   - Create a budget cap of ₹15,000 INR with threshold email alerts at 50%, 75%, 90%, and 100%.
5. **Environment Configuration:**
   ```bash
   GOOGLE_API_KEY=AIzaSy...your_google_key_here
   AGENT1_MODEL_ID=gemini-1.5-pro
   ```

---

### B. OpenAI (Agent 2 & Agent 4)
1. **Portal URL:** Navigate to the [OpenAI Platform](https://platform.openai.com/).
2. **Account Creation:** Create a commercial organization account.
3. **API Key Generation:**
   - Navigate to **Dashboard** > **API Keys**.
   - Create **Key 1 (Agent 2 Shandilya Specialist)**: `sk-proj-...`
   - Create **Key 2 (Agent 4 Independent Validator)**: Optional separate key with restricted permissions for complete auditing isolation.
4. **Billing & Hard Spending Limits:**
   - Navigate to **Settings** > **Billing** > **Usage Limits**.
   - Set **Soft Limit (Notification threshold)**: $150 USD (~₹12,500 INR).
   - Set **Hard Limit (Strict rejection cap)**: $240 USD (~₹20,000 INR). When reached, OpenAI automatically blocks further API requests.
5. **Environment Configuration:**
   ```bash
   OPENAI_API_KEY=sk-proj-...your_openai_key_here
   OPENAI_VALIDATOR_API_KEY=sk-proj-...your_validator_key_here
   AGENT2_MODEL_ID=gpt-4o
   AGENT4_MODEL_ID=gpt-4o
   ```

---

### C. Anthropic Claude (Agent 3)
1. **Portal URL:** Navigate to the [Anthropic Console](https://console.anthropic.com/).
2. **Account Creation:** Register an organization account.
3. **API Key Generation:**
   - Navigate to **API Keys** > **Create Key**.
   - Name the key: `SK_Sutras_Sutrakar_Production`.
4. **Billing & Monthly Spending Limits:**
   - Navigate to **Plans & Billing**.
   - Add commercial credits.
   - Configure **Spend Limit**: Set monthly maximum cap to $240 USD (~₹20,000 INR).
5. **Environment Configuration:**
   ```bash
   ANTHROPIC_API_KEY=sk-ant-api03-...your_anthropic_key_here
   AGENT3_MODEL_ID=claude-3-5-sonnet-20241022
   ```

---

## 3. Provider-Side vs Application-Side Budget Controls

> [!CAUTION]
> **Essential Safety Rule:**  
> The SK Sutras application implements strict pre-call cost reservation, token metering, and 100% hard stops in INR. **However, application-level checks cannot prevent provider-level overages if compromised credentials are leaked outside the system.**  
> Therefore, administrative hard spend limits MUST be configured in vendor billing dashboards before running live authoring workloads.

---

## 4. Token Efficiency & Prompt Caching Strategy

All four agent adapters support native prompt caching:
1. **Claude 3.5 Sonnet:** Static canonical instructions and Sanskrit grammar rules are tagged with ephemeral cache breakpoints (`cache_control: {"type": "ephemeral"}`), reducing repetitive prompt costs by up to 90%.
2. **Gemini 1.5 Pro:** Supports context caching for large corpora (all 84 Narada sutras cached in GPU context).
3. **GPT-4o:** Automatically caches prompt prefixes >= 1024 tokens at 50% discount.

---

## 5. Security & Key Rotation Mandate

1. **Zero Secret Leakage:** Never commit `.env` or API keys to Git repositories.
2. **Credential Storage:** Store credentials in Windows Credential Manager or AWS Secrets Manager / Vault in production.
3. **Rotation Schedule:** Rotate API keys every 90 days or immediately if any environment irregularity is suspected.
4. **Revocation Routine:** Upon project release or developer offboarding, revoke individual developer keys from provider dashboards without affecting production service keys.
