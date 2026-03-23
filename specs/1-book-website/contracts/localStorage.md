# localStorage Contract: AI-Native Book Website

**Date**: 2026-03-06
**Feature**: 1-book-website

This document defines all localStorage keys used by the application.
No backend API exists — localStorage is the sole persistence layer for user data.

---

## Key: `waitlist`

| Field | Value |
|---|---|
| **Type** | JSON string — serialised `WaitlistEntry[]` |
| **Set by** | `lib/localStorage.ts → saveWaitlistEntry()` |
| **Read by** | `lib/localStorage.ts → getWaitlist()` |
| **Default** | Key absent (treated as `[]` by `getWaitlist()`) |

**Schema**:

```json
[
  {
    "name": "Ismat Zehra",
    "email": "ismat@example.com",
    "message": "Looking forward to reading!",
    "submittedAt": "2026-03-06T14:30:00.000Z"
  }
]
```

**Write behaviour**:
1. Read existing value → parse JSON → push new entry → `JSON.stringify` → write back.
2. If key absent: write `[newEntry]`.
3. If `localStorage.setItem` throws `SecurityError` (storage blocked): return
   `{ success: false, storageBlocked: true }` — do NOT re-throw.

**Read behaviour**:
1. Read key → parse JSON → return array.
2. If key absent or parse error: return `[]` — never throw.

---

## Key: `theme`

| Field | Value |
|---|---|
| **Type** | String — `"dark"` or `"light"` |
| **Set by** | `next-themes` library (automatically) |
| **Read by** | `next-themes` library (automatically on load) |
| **Default** | Key absent → OS `prefers-color-scheme` is used |

**Note**: This key is managed entirely by `next-themes`. Application code MUST NOT read or write
this key directly — use the `useTheme()` hook from `next-themes` instead.

---

## Error Handling Summary

| Scenario | Behaviour |
|---|---|
| `localStorage` blocked (private mode / strict browser) | `saveWaitlistEntry` returns `{ success: false, storageBlocked: true }`; UI shows success + warning |
| Corrupt JSON in `waitlist` key | `getWaitlist` returns `[]`; corrupt data is effectively discarded on next write |
| `theme` key absent on first load | `next-themes` falls back to `prefers-color-scheme` OS value |
| `theme` key has unexpected value | `next-themes` falls back to `system` default |
