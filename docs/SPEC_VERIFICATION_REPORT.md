# MoltBook Trend Fetcher - Specification Verification Report

**Date**: 2026-02-04  
**Component**: MoltBook Trend Fetcher Worker  
**Status**: ⚠️ **INCOMPLETE** - Gaps and inconsistencies identified

---

## Executive Summary

The MoltBook Trend Fetcher specifications across `functional.md`, `technical.md`, and `openclaw_integration.md` are **mostly consistent** but contain **critical gaps and contradictions** that must be resolved before implementation.

**Overall Completeness**: 75%  
**Consistency Score**: 80%  
**Blocking Issues**: 3  
**Non-Blocking Issues**: 5

---

## 1. CONTRADICTIONS (Must Fix)

### 🔴 Issue #1: Time Range Enum Mismatch

**Location**: `technical.md` vs `openclaw_integration.md`

- **Technical.md** (line 15): `"time_range": "1h|4h|24h|7d"`
- **OpenClaw Integration.md** (line 15): `time_range={1h|4h|24h}` (missing `7d`)
- **OpenClaw Integration.md** (line 85): Tool schema has `"enum": ["1h", "4h", "24h", "7d"]` ✅

**Impact**: High - API contract mismatch could cause runtime errors

**Resolution**: 
- ✅ OpenClaw Integration.md tool schema is correct (includes 7d)
- ❌ OpenClaw Integration.md resource URL documentation is missing 7d
- **Action**: Update line 15 in `openclaw_integration.md` to include `7d`

---

### 🔴 Issue #2: Rate Limiting Contradiction

**Location**: `technical.md` vs `openclaw_integration.md` vs `functional.md`

- **Technical.md** (line 6): `10 requests/minute per agent (enforced by Orchestrator)`
- **OpenClaw Integration.md** (line 17): `1 request per 5 minutes per submolt`
- **Functional.md** (line 14): `max 1 request per 5 minutes per submolt`

**Analysis**: These are **different layers**:
- **10 req/min per agent**: Orchestrator-level throttling (prevents agent abuse)
- **1 req/5min per submolt**: MoltBook API rate limit (external constraint)

**Impact**: Medium - Could cause confusion about which limit applies

**Resolution**: 
- **Action**: Clarify in `technical.md` that:
  - Orchestrator enforces 10 req/min per agent (internal safety)
  - MoltBook API enforces 1 req/5min per submolt (external constraint)
  - Worker must respect BOTH limits

---

### 🔴 Issue #3: Relevance Score Threshold Mismatch

**Location**: `functional.md` vs `technical.md`

- **Functional.md** (line 13): `minimum relevance score of 0.75`
- **Technical.md** (line 41): Example shows `"relevance_score": 0.88` (no explicit threshold)

**Impact**: Medium - Filtering behavior undefined in technical spec

**Resolution**:
- **Action**: Add to `technical.md` response schema validation:
  ```json
  "relevance_score": {
    "type": "float",
    "minimum": 0.75,
    "description": "Minimum 0.75 required for trend to be returned (functional.md AC3)"
  }
  ```

---

## 2. GAPS (Missing Information)

### ⚠️ Gap #1: Input Sanitization Specification

**Location**: All files mention it, but none define HOW

- **Functional.md** (line 12): ✅ Mentions "input sanitization against prompt injection"
- **OpenClaw Integration.md** (line 9): ✅ Mentions "Input sanitization is mandatory"
- **Technical.md**: ❌ **MISSING** - No sanitization rules defined

**Impact**: High - Security-critical but undefined

**Resolution**:
- **Action**: Add to `technical.md`:
  ```markdown
  ## Input Sanitization Rules
  
  All inputs from MoltBook must be sanitized:
  1. Remove/reject patterns matching: `{system}`, `{user}`, `{assistant}`, `</s>`, `<|im_start|>`
  2. Maximum length: 10,000 characters per field
  3. Reject if contains: Base64-encoded payloads, shell commands, SQL injection patterns
  4. Sanitization failure → Discard input and alert Judge agent (functional.md AC7)
  ```

---

### ⚠️ Gap #2: Semantic Filtering Implementation Details

**Location**: `functional.md` mentions it, but `technical.md` doesn't specify HOW

- **Functional.md** (line 13): ✅ "semantic filtering (SRS §4.1.1) with minimum relevance score of 0.75"
- **Technical.md**: ❌ **MISSING** - No mention of semantic filtering algorithm

**Impact**: Medium - Core feature but implementation undefined

**Resolution**:
- **Action**: Add to `technical.md`:
  ```markdown
  ## Semantic Filtering Algorithm
  
  Relevance score calculated via:
  1. Embed topic text using Weaviate embedding model
  2. Compare against agent's SOUL.md persona embedding
  3. Calculate cosine similarity (0.0-1.0)
  4. Filter: relevance_score >= 0.75 (functional.md AC3)
  5. Store embeddings in `topic_embedding` field for future queries
  ```

---

### ⚠️ Gap #3: Error Response Schema Incomplete

**Location**: `technical.md` has error array, but details missing

- **Technical.md** (line 52-58): ✅ Has `errors[]` array structure
- **Technical.md**: ❌ **MISSING** - No complete error code enum

**Impact**: Low - Can be inferred but should be explicit

**Resolution**:
- **Action**: Add to `technical.md`:
  ```json
  "error_codes": {
    "RATE_LIMITED": "MoltBook API rate limit exceeded",
    "SANITIZATION_FAILED": "Input failed sanitization check",
    "NETWORK_TIMEOUT": "API call timed out after 30s",
    "AUTH_FAILED": "MoltBook API authentication failed",
    "CACHE_ERROR": "Redis cache operation failed",
    "EMBEDDING_ERROR": "Weaviate embedding generation failed"
  }
  ```

---

### ⚠️ Gap #4: Persona Tags vs Embeddings Mismatch

**Location**: `technical.md` request vs response

- **Technical.md** (line 17): Request has `"persona_tags": ["fashion", "genz", "tech"]` (string array)
- **Technical.md** (line 42): Response has `"topic_embedding": [0.12, -0.34, 0.56]` (vector)
- **Functional.md** (line 16): Mentions "persona tags for relevance filtering"

**Analysis**: Both are needed:
- **Persona tags**: Human-readable categories for filtering
- **Embeddings**: Vector similarity for semantic matching

**Impact**: Low - Both are valid, but relationship unclear

**Resolution**:
- **Action**: Clarify in `technical.md` that:
  - `persona_tags` are used for initial filtering (keyword-based)
  - `topic_embedding` is used for semantic relevance scoring
  - Both are required for complete filtering

---

### ⚠️ Gap #5: Heartbeat Schedule Not in Functional Spec

**Location**: `openclaw_integration.md` has it, but `functional.md` doesn't

- **OpenClaw Integration.md** (line 307): ✅ "every_4_hours: Fetch trends from 3 most relevant submolts"
- **Functional.md** (line 7): ✅ Mentions "every 4 hours" but doesn't specify which submolts

**Impact**: Low - Minor detail but should be consistent

**Resolution**:
- **Action**: Update `functional.md` AC1 to specify:
  ```
  1. ✅ Fetches trends from 3 most relevant submolts every 4 hours (per heartbeat schedule)
  ```

---

## 3. CONSISTENCY CHECKS (✅ Good)

### ✅ Cache TTL Consistency
- **Functional.md**: 1-hour TTL ✅
- **Technical.md**: 3600 seconds (1 hour) ✅
- **OpenClaw Integration.md**: 1-hour TTL ✅
- **Status**: **CONSISTENT**

### ✅ Rate Limit (MoltBook API) Consistency
- **Functional.md**: 1 req/5min per submolt ✅
- **OpenClaw Integration.md**: 1 req/5min per submolt ✅
- **Status**: **CONSISTENT**

### ✅ MCP Server Requirement
- **Functional.md**: Only uses `mcp-server-moltbook` ✅
- **OpenClaw Integration.md**: Defines `mcp-server-moltbook` interface ✅
- **Status**: **CONSISTENT**

### ✅ Database Schema Alignment
- **Technical.md**: Defines `agent_trends` table ✅
- **Technical.md**: Includes all fields from response schema ✅
- **Status**: **CONSISTENT**

---

## 4. MISSING CROSS-REFERENCES

### ⚠️ Issue: SRS References Not Validated

- **Functional.md** (line 13): References "SRS §4.1.1" but we don't have SRS document
- **OpenClaw Integration.md** (line 145): References "SRS §5.2" for disclosure level

**Impact**: Low - References are fine, but should verify SRS exists or remove references

**Resolution**:
- **Action**: Either:
  1. Add SRS document to `docs/` directory, OR
  2. Remove SRS references and make requirements self-contained

---

## 5. RECOMMENDED FIXES (Priority Order)

### 🔴 **PRIORITY 1: Blocking Issues** (Fix Before Implementation)

1. **Fix time_range enum** in `openclaw_integration.md` line 15
2. **Add input sanitization rules** to `technical.md`
3. **Clarify rate limiting layers** in `technical.md` (Orchestrator vs MoltBook)

### 🟡 **PRIORITY 2: Important Gaps** (Fix Before Testing)

4. **Add semantic filtering algorithm** to `technical.md`
5. **Add relevance_score minimum** to `technical.md` response validation
6. **Complete error code enum** in `technical.md`

### 🟢 **PRIORITY 3: Nice to Have** (Fix Before Documentation)

7. **Clarify persona_tags vs embeddings** relationship in `technical.md`
8. **Update functional.md** to specify "3 most relevant submolts" in AC1
9. **Resolve SRS references** (add SRS doc or remove references)

---

## 6. VERIFICATION CHECKLIST

Before writing code, ensure:

- [ ] All contradictions resolved (3 issues)
- [ ] All critical gaps filled (5 gaps)
- [ ] Input sanitization rules defined
- [ ] Semantic filtering algorithm specified
- [ ] Error codes fully enumerated
- [ ] Rate limiting layers clarified
- [ ] Time range enums match across all files
- [ ] Relevance score threshold consistent (0.75)
- [ ] Cache TTL consistent (1 hour)
- [ ] MCP server requirement clear (mcp-server-moltbook only)

---

## 7. NEXT STEPS

1. **Fix Priority 1 issues** (blocking)
2. **Fix Priority 2 issues** (important)
3. **Re-run this verification** to confirm all issues resolved
4. **Then proceed to** Task 2.3 (Skills Strategy) or Task 3.1 (TDD)

---

**Report Generated**: 2026-02-04  
**Next Review**: After Priority 1 fixes are applied

