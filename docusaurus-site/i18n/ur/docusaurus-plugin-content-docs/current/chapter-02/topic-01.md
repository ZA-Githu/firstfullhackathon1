---
id: topic-01
title: "AI کے ساتھ Spec-Driven ترقی"
sidebar_label: "Spec-Driven ترقی"
---

## AI کے ساتھ Spec-Driven ترقی

AI-Native ٹیموں کی سب سے بڑی ناکامی کا طریقہ یہ ہے کہ وہ بہت جلد کوڈ لکھنا شروع کر دیتی ہیں۔ آپ اپنا IDE کھولتے ہیں، Claude چلاتے ہیں، اور prompt کرنا شروع کرتے ہیں: "میرے لیے ایک login page بناؤ۔" AI کچھ بناتا ہے۔ آپ اسے ٹھیک کرتے ہیں۔ آپ محسوس کرتے ہیں کہ auth flow غلط ہے۔ دو گھنٹے بعد آپ کے پاس ایک کام کرنے والا prototype ہے جو غلط مسئلہ حل کرتا ہے۔

اس کا حل **Spec-Driven ترقی** ہے — یہ ایک ایسا اصول ہے جس میں کوڈ کی ایک بھی سطر لکھنے سے پہلے ایک منظم وضاحت میں *کیا* بنایا جا رہا ہے اور *کیوں* اسے پکڑا جاتا ہے۔

### Spec-Driven ورک فلو

```
User Intent
    ↓
/sp.specify → spec.md  (WHAT + WHY)
    ↓
/sp.plan    → plan.md  (HOW)
    ↓
/sp.tasks   → tasks.md (WHAT ORDER)
    ↓
/sp.implement → code   (DO IT)
```

ہر مرحلہ اگلے کو فیڈ کرتا ہے۔ AI مسودہ سازی چلاتا ہے؛ انسان منظوری چلاتا ہے۔

### Spec کیا ہے؟

ایک وضاحت بیان کرتی ہے:
- **کون** اس خصوصیت سے فائدہ اٹھاتا ہے (ترجیحات کے ساتھ user stories)
- **کیا** نظام کو کرنا چاہیے (فنکشنل ضروریات)
- **کب** خصوصیت کامیاب ہے (قبولیت معیار اور کامیابی کے اشارے)
- **کیا** واضح طور پر دائرے سے باہر ہے (non-goals)

اہم بات یہ ہے کہ spec یہ نہیں بتاتی کہ اسے *کیسے* بنایا جائے۔ وہ منصوبے میں ہوتا ہے۔

### ایک مضبوط Spec Prompt لکھنا

**کمزور ارادہ:**
```
Build a contact form
```

**مضبوط ارادہ:**
```
/sp.specify Contact Page
Intent: Build a waitlist capture form for visitors who want
updates about the book. The form collects name, email, and
an optional message. Save submissions to localStorage (no
backend). Show a success confirmation after submit.
Success Criteria:
- Form validates email format before submission
- Submissions persist across page refreshes
- Form is keyboard-accessible
Non-goals: Email sending, backend API, authentication
```

### ایک اچھی Spec کی ساخت

**ترجیحات کے ساتھ User Stories**
ہر story آزادانہ طور پر قابل جانچ ہے۔ P1 (اہم)، P2 (ضروری)، P3 (اچھا ہو تو) تفویض کریں۔

**فنکشنل ضروریات**
نمبر دار (`FR-001`، `FR-002`...)۔ ناقابل گفتگو ضروریات کے لیے "MUST" استعمال کریں۔

**کامیابی کے معیار**
قابل پیمائش نتائج، ٹیکنالوجی سے آزاد۔

**مفروضے اور Non-Goals**
وہ لکھیں جو آپ نے مان لیا اور جو آپ نے واضح طور پر خارج کیا۔

:::info انگوٹھے کا اصول
ایک spec مکمل ہے جب وہ ڈویلپر جس نے آپ سے کبھی بات نہیں کی، صرف اس دستاویز سے خصوصیت کو درست طریقے سے نافذ کر سکے۔
:::

### Specs AI کو بہتر کیوں بناتے ہیں

جب آپ AI کو نافذ کرنے کے لیے ایک spec دیتے ہیں:

1. **آؤٹ پٹ زیادہ درست ہوتے ہیں** — ٹھوس قبولیت معیار جن کی طرف نشانہ بنانا ہے
2. **آؤٹ پٹ زیادہ مستقل ہوتے ہیں** — دستاویز کردہ مفروضے جن سے کام کرنا ہے
3. **جائزہ تیز ہوتا ہے** — AI آؤٹ پٹ کو مخصوص، نمبر دار ضروریات کے خلاف جانچیں

### Spec کی عام غلطیاں

- **بہت زیادہ نفاذ تفصیل** — اگر آپ کا spec کہتا ہے "PostgreSQL استعمال کریں"، یہ بہت مخصوص ہے
- **مبہم کامیابی معیار** — "صارفین خوش ہوں" کامیابی کا معیار نہیں ہے
- **غائب non-goals** — واضح اخراج کے بغیر، دائرہ خاموشی سے پھیلتا ہے
- **کوئی ترجیحی ترتیب نہیں** — اگر سب کچھ P1 ہے، تو کچھ بھی نہیں ہے
