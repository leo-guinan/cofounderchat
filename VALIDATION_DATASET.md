# Conscious Economics Validation Dataset

## Overview

20 gold-standard examples for testing if a model can learn the Conscious Economics pattern.

**Purpose:** Validate the approach before investing 200-500 hours in generating 100K+ training examples.

## Dataset Composition

### Conscious-BizMath (10 examples)
Teaching unit economics + Time Violence calculations:

1. **SaaS LTV/CAC:** `$50/mo × 18mo = $900 LTV` + `156hr saved = $5,460 time value`
2. **App load time:** Investment vs cumulative time savings analysis
3. **Marketplace take rate:** 15% vs 20%, Time Violence comparison
4. **Freemium CAC:** Effective CAC calculation, payback analysis
5. **Customer success ROI:** Traditional -64% vs Conscious +107%
6. **Build vs buy:** Total economic cost including Time Violence
7. **Price increase:** Revenue gain vs Time Violence cost
8. **White-label decision:** High revenue but catastrophic Time Violence
9. **Referral program:** CAC efficiency + willing time analysis
10. **Live chat support:** Customer time saved vs team time increased

### Experiment Cards (5 examples)
Teaching hypothesis → test → C-ROI workflow:

11. **Free tier test:** A/B design, success metrics, Time Violence analysis
12. **Personalized emails:** Expected impact, C-ROI calculation, minimal investment
13. **Pricing page redesign:** Conversion improvement, visitor Time Violence reduction
14. **Video tutorials:** Support deflection, production cost vs value
15. **Trial length test:** 7-day vs 14-day, decision framework

### Compliance Drills (5 examples)
Teaching trust/evidence/constraint checking:

16. **AI claims:** "40% reduction" - insufficient evidence, FTC standards
17. **Competitive claims:** "10x faster" - benchmark requirements, Lanham Act
18. **Data selling:** Legal/ethical analysis, GDPR/CCPA compliance
19. **Model version lying:** "GPT-5" when using GPT-4 - false advertising
20. **HIPAA compliance:** Healthcare launch, BAA requirements, penalties

## Coverage Statistics

| Block | Count | Coverage |
|-------|-------|----------|
| `<|metrics|>` | 19/20 | 95% |
| `<|assumptions|>` | 15/20 | 75% |
| `<|time_violence|>` | 14/20 | 70% |
| `<|trust_evidence|>` | 14/20 | 70% |
| `<|compliance|>` | 14/20 | 70% |
| `<|tests|>` | 14/20 | 70% |
| `<|risks|>` | 13/20 | 65% |
| `<|time_dividend|>` | 9/20 | 45% |

**Average assistant response:** 3,125 characters (detailed, not trivial)

## What The Model Should Learn

### 1. When to Use Conscious Economics
- Founder/product questions (pricing, features, hiring)
- ROI/investment decisions
- Compliance/trust questions
- NOT: general chat, coding help, creative writing

### 2. Output Schema
```
<|assumptions|>
[Ranked list, riskiest first]

<|risks|>
[Explicit failure modes]

<|tests|>
[1-week falsifiable experiments]
Success metrics: [specific, measurable]

<|time_violence|>
ΔTVH = [hours saved]
v_t = $[shadow price]/hr
Time value = $[calculation]

<|time_dividend|>
Users: [hours] ([%])
Navigators: [hours] ([%])
Company: [hours] ([%])

<|metrics|>
C-ROI* = $[calculation]
Traditional ROI vs Conscious ROI
```

### 3. Parameter Formatting
```python
# Correct:
arr_rate=10, svc_rate=12, var_arr=4

# Also correct:
revenue: 5000, hours_saved: 15

# Wrong:
"arrival rate is approximately ten" ❌
```

### 4. Trust/Evidence Standards
- Don't make claims without data
- Specify sample size, timeframe, methodology
- Acknowledge uncertainty
- Propose falsifiable tests

## Usage

### Load Dataset
```python
from tasks.conscious_validation import ConsciousValidation

dataset = ConsciousValidation(split="train")
print(f"Loaded {len(dataset)} examples")  # 20

# Access example
ex = dataset[0]
user_msg = ex['messages'][0]['content']
assistant_msg = ex['messages'][1]['content']
```

### Test SFT (Next Step)
```bash
# Minimal SFT test - just to see if pattern is learnable
torchrun --standalone --nproc_per_node=1 -m scripts.chat_sft \
    --source=base \
    --num_epochs=10 \
    --max_iterations=100 \
    --eval_every=20
```

Expected outcome:
- Model starts emitting `<|assumptions|>`, `<|tests|>` blocks
- Parameters formatted correctly (`param=value`)
- C-ROI calculations appear (even if initially wrong)
- Proves pattern is learnable from small dataset

## Success Criteria

### Minimum (proves concept works):
- [ ] Model emits ≥1 conscious economics block unprompted
- [ ] Parameters formatted correctly (not natural language)
- [ ] Blocks appear in logical order
- [ ] No catastrophic failures (infinite loops, crashes)

### Good (pattern is learnable):
- [ ] Model emits 3+ blocks per response
- [ ] Calculations attempted (even if wrong)
- [ ] Schema maintained across examples
- [ ] Can generalize to new founder questions

### Excellent (ready to scale):
- [ ] Full schema coverage (assumptions → metrics)
- [ ] Calculations mostly correct
- [ ] Natural integration with reasoning
- [ ] Coherent multi-step logic

## Next Steps

### If Validation Succeeds
1. Generate 10K examples (GPT-4 + validation)
2. Test SFT on 10K dataset
3. If still working, scale to 100K+
4. Full midtraining + SFT pipeline

### If Validation Fails
1. Analyze failure mode:
   - Model ignores blocks? (schema too complex)
   - Calculations wrong? (need more math examples)
   - Natural language instead of params? (need more formatting examples)
2. Iterate on schema/examples
3. Retest with updated validation set
4. Don't scale until pattern works

## Files

### Created
- `tasks/conscious_validation_data.py` - 20 example definitions
- `tasks/conscious_validation.py` - Dataset wrapper
- `VALIDATION_DATASET.md` - This file

### To Create (if validation succeeds)
- `tasks/conscious_biz_math.py` - 100K LTV+TV examples
- `tasks/experiment_cards.py` - 50K experiment examples
- `tasks/compliance_drills.py` - 20K compliance examples

## Testing

### Verify Dataset Loads
```bash
python -m tasks.conscious_validation
```

Expected output:
```
✓ Loaded 20 examples
✓ All 20 examples have correct structure
Conscious economics blocks found:
  <|assumptions|>: 15/20 examples (75%)
  <|metrics|>: 19/20 examples (95%)
  ...
```

### Integration Test
```bash
python test_conscious_pipeline.py  # If torch installed
```

Tests:
1. Dataset loading
2. Tokenizer has special tokens
3. Conscious tools work
4. Engine parsing works
5. Example quality verified

## Philosophy

**Why start with 20 examples?**

Traditional ML wisdom: "More data = better"

Conscious Economics wisdom: "Test assumptions before scaling"

- 20 examples costs: 6-8 hours (manual curation)
- 100K examples costs: 200-500 hours (GPT-4 + validation)

**ROI of validation:**
- Investment: 8 hours
- Risk reduction: Prevents 200-500 hour waste if pattern doesn't work
- Information value: Tells us if schema is learnable
- Expected value: 25x-60x return on time investment

Test fast. Fail fast. Iterate.

---

**Status:** ✅ Validation dataset complete  
**Next:** Test SFT on validation set  
**Decision point:** Scale to 100K+ only if validation succeeds

