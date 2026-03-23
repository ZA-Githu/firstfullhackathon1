---
id: topic-01
title: "ابھرتے ہوئے پیٹرن اور ٹولز"
sidebar_label: "ابھرتے ہوئے پیٹرن اور ٹولز"
---

## ابھرتے ہوئے پیٹرن اور ٹولز

سب سے اہم آرکیٹیکچرل تبدیلی AI ایجنٹس ہیں جو آپریٹنگ سسٹمز کے طور پر کام کرتے ہوئے خصوصی ماڈلز اور ٹولز کو مربوط کرتے ہیں۔

### ایجنٹس بطور آپریٹنگ سسٹمز

ایک orchestrator ایجنٹ منصوبہ بندی، تحقیق، نفاذ، تشخیص، اور ابلاغی ایجنٹس کو مربوط کرتا ہے۔ ہر ایک کے پاس مخصوص ٹولز، ایک واضح انٹرفیس، اور ڈومین سے متعلقہ میموری ہے۔ انسان اعلی سطح کا ارادہ طے کرتا ہے اور اہم فیصلوں کو منظور کرتا ہے۔

```
TextbookMasterAgent (orchestrator)
├── RAGQuerySkill       → search textbook content
├── ChapterGenerationSkill → write/expand chapters
├── PersonalizationSkill   → adapt to learner profile
├── TranslationSkill       → Urdu translation
└── IngestionSkill         → embed new content
```

یہ بالکل اسی طرح ہے جیسے اس نصابی کتاب کا بیک اینڈ بنایا گیا ہے — `TextbookMasterAgent` Claude کی tool-use API کے ذریعے پانچ قابل استعمال skills کو مربوط کرتا ہے۔

### Context Windows اور Multimodal AI

128K سے ۱ ملین tokens تک context windows سسٹم ڈیزائن کو نئی شکل دیتے ہیں:

| Context سائز | بہترین استعمال |
|---|---|
| 8K–32K | معیاری chat، کوڈ جائزہ |
| 128K | لمبی دستاویزات، مکمل codebases |
| 1M | پوری نصابی کتابیں، ویڈیو تجزیہ |

لمبا context RAG کو **ختم نہیں** کرتا۔ لمبا context اس وقت استعمال کریں جب درستگی سب سے زیادہ اہمیت رکھتی ہو اور RAG اس وقت جب پیمانہ اور لاگت سب سے زیادہ اہمیت رکھتے ہوں۔

### Vision-Language-Action (VLA) ماڈلز

VLA ماڈلز فزیکل AI کے لیے اگلی سرحد ہیں۔ وہ بصری ان پٹ لیتے ہیں، زبان کی ہدایات سمجھتے ہیں، اور روبوٹ اقدامات آؤٹ پٹ کرتے ہیں۔

```
Camera Input → Vision Encoder
                    ↓
Language Instruction → Language Model → Action Output → Robot
```

اہم VLA ماڈلز:
- **RT-2** (Google): robotics transformer، web-scale training
- **OpenVLA**: open-source، Jetson Orin Nano پر چلتا ہے
- **π0** (Physical Intelligence): dexterous manipulation

### کوڈ جنریشن پختگی منحنی

ٹیمیں پانچ مراحل سے گزرتی ہیں:

1. **Autocomplete** — IDE میں tab completion
2. **فنکشن جنریشن** — ایک وقت میں ایک فنکشن تیار کریں
3. **جزء جنریشن** — مکمل components تیار کریں
4. **خصوصیت جنریشن** — spec سے پوری خصوصیات تیار کریں
5. **نظام جنریشن** — ارادے سے نظام تیار کریں

معروف AI-Native ٹیمیں اچھی طرح سے وضاحت شدہ خصوصیات کے لیے مرحلہ ۵ تک پہنچتی ہیں۔ ٹولز پر نہیں، پیٹرن پر داؤ لگائیں۔ پیٹرن باقی رہتے ہیں جبکہ مخصوص ٹولز ہر ۱۸ ماہ میں بدلتے ہیں۔
