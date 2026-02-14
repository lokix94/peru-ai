# 🌐 Web Platform Research — Human-Agent Interaction
> Researched by Quipu 🪢 | 2026-02-11

---

## A) Web Frameworks — Best Stack for Rapid Prototyping

### Top 3 Options

#### 1. 🥇 **Next.js (React) + Node.js/Serverless** — RECOMMENDED
- **Frontend:** Next.js 15+ (App Router, Server Components, built-in API routes)
- **Backend:** Built-in API routes + optional FastAPI microservices
- **Pros:**
  - Largest ecosystem, most npm packages, most tutorials
  - Server-Side Rendering (SSR) + Static Generation (SSG) = great SEO for marketplace
  - Vercel deploys in seconds (free tier)
  - Supabase/Prisma for instant database
  - TypeScript native, huge community
  - Used by Chatbot UI (mckaywrigley), NextChat (80k+ ★), LobeHub
- **Cons:**
  - React can be verbose for simple UIs
  - Bundle size can grow without care
  - Vercel lock-in temptation
- **Time to MVP:** 3-5 days

#### 2. 🥈 **SvelteKit + Node.js**
- **Frontend:** SvelteKit (compiled, ultra-fast, minimal JS shipped)
- **Backend:** SvelteKit server routes + adapters for any host
- **Pros:**
  - Used by HuggingFace Chat UI (official) — battle-tested for AI chat
  - Smallest bundle sizes, fastest runtime performance
  - Built-in SSR, routing, form actions
  - Less boilerplate than React
  - MongoDB integration proven (HF Chat UI uses it)
- **Cons:**
  - Smaller ecosystem than React
  - Fewer pre-built component libraries
  - Harder to find developers
- **Time to MVP:** 3-5 days

#### 3. 🥉 **Python FastAPI + React/Vue SPA**
- **Frontend:** React (Vite) or Vue 3
- **Backend:** FastAPI (Python, async, OpenAPI docs auto-generated)
- **Pros:**
  - Python backend = direct access to AI/ML libraries
  - FastAPI is blazing fast, auto-docs with Swagger
  - Great for heavy backend logic (agent orchestration)
  - Can integrate edge-tts Python library directly
- **Cons:**
  - Two separate codebases (frontend + backend)
  - More deployment complexity (two services)
  - CORS setup needed
- **Time to MVP:** 5-7 days

### 💡 Recommendation
**Next.js** for the frontend + marketplace pages. If we need Python for AI/TTS logic, use a **FastAPI microservice** alongside it. This hybrid approach gives us the React ecosystem for UI and Python power for AI backends.

---

## B) Voice in Browser — Technologies & Integration

### Top 3 Approaches

#### 1. 🥇 **Web Speech API (Browser-Native)** — RECOMMENDED for MVP
- **What:** Built-in browser API for both Speech Recognition (STT) and Speech Synthesis (TTS)
- **Key interfaces:**
  - `SpeechRecognition` — voice-to-text (microphone input)
  - `SpeechSynthesis` — text-to-speech (browser voices)
  - `SpeechSynthesisUtterance` — speech request objects
- **Pros:**
  - **FREE** — no API key, no server, no cost
  - Zero dependencies
  - Works in Chrome, Edge, Safari, Firefox (partial)
  - Supports multiple languages including Spanish
  - On-device speech recognition now available (Chrome 128+)
  - Good enough for MVP demo
- **Cons:**
  - Voice quality varies by browser/OS
  - Limited voice selection (depends on OS)
  - Recognition requires internet on most browsers (sends to Google)
  - No custom voice cloning
- **Integration:** 5 lines of JavaScript:
  ```js
  const utterance = new SpeechSynthesisUtterance("Hola mundo");
  utterance.lang = "es-PE";
  speechSynthesis.speak(utterance);
  ```

#### 2. 🥈 **Edge TTS via Backend API**
- **What:** Microsoft Edge's neural TTS service, accessed via `edge-tts` Python library
- **Key facts:**
  - FREE, no API key needed
  - 400+ voices, 100+ languages
  - We already use `es-PE-CamilaNeural` for Peru!
  - High quality neural voices
- **Web integration pattern:**
  1. Backend (FastAPI/Node) runs `edge-tts` to generate MP3
  2. Serves audio file via API endpoint
  3. Frontend plays with `<audio>` element or Web Audio API
  4. Can stream chunks for real-time feel
- **Pros:**
  - Excellent voice quality (neural, natural-sounding)
  - Peruvian Spanish voice (CamilaNeural) already tested
  - Generates SRT subtitles alongside audio
  - Rate/pitch/volume control
- **Cons:**
  - Requires server-side processing
  - Slight latency (generate → serve → play)
  - Unofficial API (could change)
  - Not truly real-time streaming
- **Integration approach:** FastAPI endpoint `/api/tts` that accepts text, returns MP3 stream

#### 3. 🥉 **WebRTC for Real-Time Voice Chat**
- **What:** Peer-to-peer real-time communication standard
- **Key APIs:**
  - `RTCPeerConnection` — establish P2P connections
  - `getUserMedia()` — capture microphone/camera
  - `getDisplayMedia()` — screen sharing
- **Pros:**
  - True real-time, low-latency voice
  - Peer-to-peer (less server load)
  - Industry standard (used by Discord, Google Meet)
  - Can enable human-to-agent voice conversations
- **Cons:**
  - Complex to implement (signaling server needed)
  - Overkill for TTS playback
  - STUN/TURN servers needed for NAT traversal
  - Better for Phase 2 (real-time voice agent chat)
- **When to use:** Phase 2 — when we want live voice conversations with AI agents

### 💡 Recommendation
**MVP:** Use **Web Speech API** for browser STT (voice input) + **Edge TTS backend** for high-quality voice output (CamilaNeural). This gives us voice input AND output with zero cost. **Phase 2:** Add WebRTC for real-time agent voice calls.

---

## C) Chat UI Libraries — Open Source Options

### Top 3 Options

#### 1. 🥇 **LobeHub (lobehub)** — RECOMMENDED to study/fork
- **GitHub:** `lobehub/lobehub` (50k+ ★)
- **Stack:** Next.js, TypeScript, Ant Design
- **Features:**
  - Agent marketplace built-in ("Agent Market / GPTs")
  - MCP Plugin system + MCP Marketplace
  - TTS & STT voice conversation support
  - Multi-model support (OpenAI, Ollama, local)
  - Plugin system (function calling)
  - File upload / Knowledge base
  - Dark/light themes, responsive
  - PWA (Progressive Web App)
  - Multi-user management
  - Desktop app (Electron)
  - Agent Groups for collaboration
  - Personal memory system
- **Pros:**
  - Most feature-complete — already has marketplace + voice + chat
  - Active development, large community
  - Next.js based (our recommended stack)
  - One-click Vercel deploy
  - Agent-as-unit-of-work philosophy matches our vision
- **Cons:**
  - Complex codebase (may be hard to customize deeply)
  - Opinionated architecture
  - Heavy — many features we may not need initially

#### 2. 🥈 **Open WebUI**
- **GitHub:** `open-webui/open-webui` (90k+ ★)
- **Stack:** SvelteKit frontend + Python backend
- **Features:**
  - Voice/video call with multiple STT/TTS providers
  - Hands-free voice mode
  - RAG (Retrieval Augmented Generation)
  - Web search integration
  - Plugin/pipeline system (Python)
  - Model builder UI
  - RBAC + multi-user
  - 9 vector database options
  - Community model sharing
- **Pros:**
  - Extremely popular and battle-tested
  - Voice already built-in (Whisper, OpenAI, Edge TTS compatible)
  - Python backend = easy AI integration
  - Docker one-line deploy
  - `pip install open-webui` — dead simple
- **Cons:**
  - SvelteKit (smaller ecosystem than React)
  - No built-in marketplace for selling skills
  - More focused on personal/team use, not marketplace

#### 3. 🥉 **HuggingFace Chat UI**
- **GitHub:** `huggingface/chat-ui` (8k+ ★)
- **Stack:** SvelteKit, MongoDB
- **Features:**
  - Powers HuggingChat (production-grade)
  - OpenAI-compatible API support
  - MCP Tools integration
  - LLM Router (smart model selection)
  - Theming/branding customizable
  - Docker support with bundled MongoDB
- **Pros:**
  - Clean, minimal, production-proven
  - Easy to customize (SvelteKit)
  - MCP support for tool calling
  - Lightweight, fast
- **Cons:**
  - No marketplace features
  - No built-in voice
  - SvelteKit ecosystem smaller

### Honorable Mentions
| Library | Stars | Stack | Best For |
|---------|-------|-------|----------|
| **NextChat** | 80k+ ★ | Next.js | Lightweight chat, one-click deploy |
| **Ant Design X** | 3k+ ★ | React | Enterprise AI components (Bubbles, Prompts) |
| **LangUI** | 2k+ ★ | Tailwind/HTML | Copy-paste UI components (60+ pieces) |
| **Chatbot UI** | 29k+ ★ | Next.js + Supabase | Clean ChatGPT clone |
| **react-chat-elements** | 1k+ ★ | React | Low-level chat components |

### 💡 Recommendation
**Study LobeHub** deeply — it's the closest to what we want (chat + marketplace + voice + agents). For our MVP, we can either:
1. **Fork LobeHub** and customize it (faster but complex)
2. **Build fresh** with Next.js + **Ant Design X** components + **LangUI** for styling (more control, cleaner)

---

## D) Marketplace Patterns — How Skill Marketplaces Work

### Key Architecture Components

#### 1. **Payment Integration**

##### Stripe Connect (RECOMMENDED)
- **Model:** Platform marketplace with connected accounts
- **How it works:**
  - Platform (us) is merchant of record
  - Sellers create Stripe Express accounts
  - We process payments, take application fee (commission)
  - Stripe handles seller onboarding, KYC, payouts
- **Features:** Destination charges, application fees, automated payouts
- **Pricing:** 2.9% + $0.30 per transaction + Connect fees
- **Best for:** Professional marketplace with real money flow

##### Crypto (Phase 2+)
- Could use USDC/SOL on Solana for instant, low-fee payments
- Smart contracts for escrow and automated delivery
- Not needed for MVP

#### 2. **Listing, Search, Reviews**
- **Listing:** JSON schema for skills (name, description, price, category, agent compatibility, demo)
- **Search:** Full-text search (Algolia, Meilisearch, or PostgreSQL FTS)
- **Reviews:** Star ratings (1-5), text reviews, verified purchase badge
- **Categories:** By domain (coding, writing, research, legal, etc.) and by capability (TTS, image, data)

#### 3. **Digital Delivery**
- Skills are code/config bundles (not physical goods)
- Delivery = granting access (API key, download link, or repo access)
- Can use:
  - **Git-based:** Private repo access granted on purchase
  - **Package registry:** npm-style install after purchase
  - **API-based:** Usage credits/tokens
  - **OpenClaw-native:** ClawHub integration (skill install)

### Existing Marketplace Models to Learn From

| Platform | Model | Revenue | Key Insight |
|----------|-------|---------|-------------|
| **LobeHub MCP Marketplace** | Free plugins | Community-driven | Browse/install flow, categories |
| **OpenAI GPT Store** | Revenue sharing | 30% platform cut | Agent discovery, ratings, "try before buy" |
| **HuggingFace Spaces** | Free + paid compute | Compute pricing | Model hosting, demo-first approach |
| **Replicate** | Pay-per-run API | Usage-based pricing | Run any model via API, instant demos |
| **GitHub Marketplace** | Free + paid | Per-seat/usage | Verified publishers, categories, reviews |
| **Gumroad** | Digital sales | 10% + processing | Simple checkout, instant delivery |

### 💡 Recommendation
**MVP Marketplace:** Start simple.
1. **Listings page** — Grid of skills with search/filter
2. **Skill detail page** — Description, demo, author, reviews
3. **Install button** — Free skills first (ClawHub-style install)
4. **Phase 2:** Add Stripe Connect for paid skills + revenue sharing

---

## E) Existing Platforms to Learn From

### 1. 🏆 **LobeHub** — Best Reference Architecture
- **URL:** lobehub.com
- **What it does:** AI workspace with agent marketplace, plugins, voice, multi-model
- **Key learnings:**
  - "Agents as the unit of work" — exactly our philosophy
  - MCP Marketplace for plugins/skills
  - Agent Groups for collaboration
  - Personal memory system
  - Desktop + web + PWA
- **Tech:** Next.js, TypeScript, Ant Design
- **What to borrow:** Marketplace UI, agent card design, voice integration patterns

### 2. 📦 **Open WebUI** — Best Self-Hosted Chat
- **URL:** openwebui.com
- **What it does:** Self-hosted AI interface with voice, RAG, plugins
- **Key learnings:**
  - Pipeline/plugin system for extensibility
  - Voice/video call integration patterns
  - Community model sharing
  - Admin + user roles
- **Tech:** SvelteKit + Python
- **What to borrow:** Voice implementation, plugin architecture

### 3. 🤗 **HuggingFace Spaces** — Best Demo Platform
- **URL:** huggingface.co/spaces
- **What it does:** Host ML app demos (Gradio, Streamlit, Docker)
- **Key learnings:**
  - Demo-first approach (try before you use)
  - Community-driven content
  - "Discover amazing ML apps"
  - Categories: vision, text, audio, multimodal
  - Free tier + paid compute
- **What to borrow:** Discovery/browse UX, demo embedding

### 4. 🔄 **Replicate** — Best API Marketplace
- **URL:** replicate.com
- **What it does:** Run AI models via API, pay-per-use
- **Key learnings:**
  - Every model has a demo page
  - Collections for curation (e.g., "Try for free", "Vision models")
  - Usage-based pricing model
  - Featured models for discovery
- **What to borrow:** Model card layout, collections/curation

### 5. 🦉 **OpenClaw / ClawHub** — Our Own Ecosystem
- **What it does:** Skill marketplace for OpenClaw agents
- **Key learnings:**
  - CLI-first install (`clawhub install <skill>`)
  - Skill = folder with SKILL.md + code
  - Already has publish/install flow
- **What to borrow:** Native integration, skill format as foundation

---

## 🎯 MVP Plan — What We Can Build in 1 Week

### Vision
**Peru Hub** — A web platform where agents and humans discover, try, and use AI skills.

### Stack
| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | **Next.js 15** (App Router) | Fastest to prototype, largest ecosystem |
| UI Components | **Tailwind CSS** + **shadcn/ui** + **Ant Design X** | Beautiful, dark mode, AI-specific components |
| Chat UI | Custom with **Ant Design X** Bubble/Conversation components | Purpose-built for AI chat |
| Voice (TTS) | **Edge TTS** via API route | Free, high-quality CamilaNeural voice |
| Voice (STT) | **Web Speech API** | Free, browser-native |
| Database | **Supabase** (PostgreSQL + Auth + Storage) | Free tier, instant setup, auth included |
| Deployment | **Vercel** | Free, instant deploys from Git |
| Payments | None (Phase 1 = free skills) | Stripe Connect in Phase 2 |

### Day-by-Day Plan

#### Day 1-2: Foundation
- [ ] `npx create-next-app peru-hub --typescript --tailwind --app`
- [ ] Set up Supabase project (database + auth)
- [ ] Create base layout: header, sidebar, main content
- [ ] Dark/light mode toggle
- [ ] Landing page with hero section

#### Day 3: Chat Interface
- [ ] Chat page with message bubbles (Ant Design X or custom)
- [ ] Streaming message support
- [ ] Markdown rendering in messages
- [ ] Input area with send button + voice button
- [ ] Connect to OpenAI-compatible API

#### Day 4: Voice Integration
- [ ] Web Speech API for voice input (microphone button)
- [ ] Edge TTS API route (`/api/tts`) for voice output
- [ ] Audio playback in chat (play button on messages)
- [ ] Voice toggle (enable/disable auto-read)

#### Day 5: Skill Marketplace Page
- [ ] Skills listing page (grid of cards)
- [ ] Skill detail page (description, author, install)
- [ ] Search and category filter
- [ ] Seed with 5-10 existing OpenClaw skills
- [ ] "Install" button (links to ClawHub CLI)

#### Day 6: Polish & Connect
- [ ] User auth (Supabase Auth — email + GitHub)
- [ ] User profiles
- [ ] Responsive design (mobile-friendly)
- [ ] Connect chat to skill system (select active skill)
- [ ] Error handling, loading states

#### Day 7: Deploy & Demo
- [ ] Deploy to Vercel
- [ ] Custom domain setup
- [ ] README + screenshots
- [ ] Demo video
- [ ] Share on social media

### Post-MVP Roadmap (Weeks 2-4)
1. **Stripe Connect** — Paid skills + revenue sharing
2. **WebRTC Voice** — Real-time voice conversations with agents
3. **Agent profiles** — Public pages for each agent (like Peru 🇵🇪)
4. **Skill builder** — Create/publish skills from the web UI
5. **Reviews & ratings** — Community feedback system
6. **Multi-agent chat** — Chat rooms with multiple agents

---

## 📊 Summary Table

| Category | Recommendation | Confidence |
|----------|---------------|------------|
| Frontend Framework | **Next.js 15** | ⭐⭐⭐⭐⭐ |
| Backend | **Next.js API Routes** + **FastAPI** (for TTS) | ⭐⭐⭐⭐ |
| Chat UI | **Ant Design X** + custom components | ⭐⭐⭐⭐ |
| Voice TTS | **Edge TTS** (backend) + **Web Speech API** (fallback) | ⭐⭐⭐⭐⭐ |
| Voice STT | **Web Speech API** (browser native) | ⭐⭐⭐⭐ |
| Database | **Supabase** (PostgreSQL) | ⭐⭐⭐⭐⭐ |
| Marketplace | Custom + ClawHub integration | ⭐⭐⭐⭐ |
| Reference Platform | **LobeHub** (study/inspiration) | ⭐⭐⭐⭐⭐ |
| Deployment | **Vercel** (free tier) | ⭐⭐⭐⭐⭐ |
| Total MVP Cost | **$0** (all free tiers) | 💰 |

---

*Research complete. Ready to build.* 🚀
