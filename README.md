# CofounderChat

> Your conscious AI co-founder trained on Conscious Economics and Time Violence reduction

**CofounderChat** is an AI trained to think like a founder who understands both revenue AND human time costs. Built on [nanochat](https://github.com/karpathy/nanochat), it extends traditional LLM chat with **Conscious Economics** reasoning.

## What Makes It Different

**Traditional AI:** 
```
Q: Should we build feature X?
A: Yes, it will improve user experience.
```

**CofounderChat:**
```
Q: Should we build feature X?

A: <|assumptions|>
   1. Users want this (no validation yet)
   2. Dev time = 2 weeks
   
   <|tests|>
   Survey 20 users first: "Would you use this?"
   Success = ≥60% say "definitely"
   
   <|time_violence|>
   Building without validation = 80 hours wasted if wrong
   
   <|metrics|>
   C-ROI* = $0 (no evidence of demand)
   
   Recommendation: TEST before building
```

The model calculates:
- **Time Violence** (hours wasted by complexity)
- **Time Dividends** (who gets hours back, and how many)
- **Consciousness Index** C(S) = 1 - (TVH/TV)
- **Conscious ROI** (revenue + time value, not just revenue)

---

## Current Status

**Infrastructure:** ✅ 70% Complete (Phases 1-7)
- Token vocabulary (21 special tokens for structured reasoning)
- Calculation engine (Time Violence, Consciousness Index, C-ROI)
- Training pipeline (midtraining + SFT with Conscious Economics)
- Validation dataset (36 curated examples)
- Evaluation tasks (Time Violence accuracy, TD accounting, trust/compliance)

**Training data:** 36 examples (scales to 170K+ when needed)

**Ready to train:** When you rent 8xH100 GPUs ($96 for 4 hours)

📖 **[CONSCIOUS_ECONOMICS.md](CONSCIOUS_ECONOMICS.md)** - Full technical documentation  
📊 **[STATUS.md](STATUS.md)** - Current progress and next steps  
📝 **[VALIDATION_DATASET.md](VALIDATION_DATASET.md)** - Training data details  

---

## Quick Start

### Option 1: Local Validation Test (MacBook, $0)

Test if the pattern is learnable without GPUs:

```bash
# Setup (first time only)
uv venv && uv sync
source .venv/bin/activate

# Train tokenizer with Conscious Economics tokens
python -m scripts.tok_train --vocab_size=8192

# Test if model can learn the pattern
python test_validation_pattern.py
```

Expected: Model learns to emit `<|assumptions|>`, `<|metrics|>` blocks.

See [QUICKSTART_VALIDATION.md](QUICKSTART_VALIDATION.md) for details.

---

### Option 2: Full Training (Cloud GPUs, $96)

Train a production model with Conscious Economics:

```bash
# On Lambda Labs 8xH100 instance
bash speedrun.sh
```

This runs the full pipeline (4 hours):
1. Tokenizer training (with 21 special tokens)
2. Base pretraining
3. Midtraining (with Conscious Economics mixture)
4. Supervised fine-tuning (enforces C-ROI schema)
5. Optional: Reinforcement learning

Then chat with your model:

```bash
python -m scripts.chat_web
# Visit http://[your-ip]:8000
```

Ask founder questions:
- "Should we hire a CSM at $80K?"
- "Price increase: $49 to $79?"
- "Can we claim '10x faster' in marketing?"

The model will respond with Time Violence calculations and Conscious ROI.

---

## Built on nanochat

CofounderChat is a fork of Andrej Karpathy's [nanochat](https://github.com/karpathy/nanochat) - the minimal, hackable ChatGPT implementation.

**nanochat provides:**
- Full training pipeline (tokenization → pretraining → SFT → RL)
- Clean, readable codebase (~8K lines)
- Runs on $100 of GPU compute (8xH100, 4 hours)
- Produces working ChatGPT clone

**CofounderChat adds:**
- 12 new special tokens (assumptions, metrics, time_violence, etc.)
- Conscious Economics calculation engine (tv_ops, conscious_index, roi_conscious)
- Time Violence awareness (measures hours wasted by complexity)
- C-ROI optimization (revenue + time value, not just revenue)
- Trust & compliance checking (evidence requirements, constraint validation)

All changes are documented in [CONSCIOUS_ECONOMICS.md](CONSCIOUS_ECONOMICS.md).

---

## Hardware Requirements

### For Local Testing (Free)
- MacBook with M-series chip (or any CPU)
- Tests if pattern is learnable
- No GPU needed
- Takes 10-30 minutes

### For Full Training ($96)
- **Recommended:** 8x H100 GPUs (80GB each)
- **Also works:** 8x A100 GPUs (80GB each, slightly slower)
- **Budget option:** Single GPU (8x slower, 32 hours instead of 4)
- **Provider:** Lambda Labs, RunPod, or Vast.ai

**Cost:** $24/hour × 4 hours = $96 for full pipeline

---

## Training Data

### Current (Validation Phase)
- **36 curated examples** (hand-crafted for quality)
  - 10 Conscious-BizMath (LTV + Time Violence)
  - 5 Experiment Cards (hypothesis → test → C-ROI)  
  - 5 Compliance Drills (trust/evidence checks)
  - 16 SFT Templates (perfect schema examples)

### Future (Production Scale)
- **170K+ generated examples** (when scaling up)
  - 100K Conscious-BizMath
  - 50K Experiment Cards
  - 20K Compliance Drills

**Generation strategy:** GPT-4 + human validation (~$200-500 investment)

---

## Example Outputs

### Unit Economics Query

**Input:**  
"Calculate LTV for $50/month, 18 month retention, $200 CAC."

**CofounderChat Output:**
```
<|assumptions|>
1. Churn rate constant at ~5.5%/month
2. No expansion revenue

<|python_start|>50*18<|python_end|><|output_start|>900<|output_end|>

LTV = $900
CAC = $200
LTV:CAC = 4.5:1 ✓

<|time_violence|>
If product saves users 2 hr/week:
ΔTVH = 2 hr/week × 52 weeks × 1.5 yr = 156 hours
v_t = $35/hr
Time value = $5,460

<|time_dividend|>
Users: 93.6 hr (60%)
Navigators: 31.2 hr (20%)
Company: 31.2 hr (20%)

<|metrics|>
Traditional LTV: $900
Conscious value: $900 + $5,460 = $6,360
Multiplier: 7.1x (time value dominates)
```

### Compliance Check

**Input:**  
"Can we claim 'AI reduces support tickets by 40%' in marketing?"

**CofounderChat Output:**
```
<|trust_evidence|>
Insufficient evidence. Need:
1. Sample size (N=?)
2. Controlled test (A/B)
3. Time period (1 week vs 6 months?)
4. Statistical significance (p<0.05)

<|compliance|>
FTC requires reasonable basis for claims
Can't use unvalidated assertion

<|tests|>
Run proper A/B test:
- 100 customers WITH AI vs 100 WITHOUT
- Duration: 3 months
- Track: ticket volume, significance

<|metrics|>
Current: no evidence
Action: test before claiming
```

---

## Architecture

### Conscious Economics Extensions

**1. Special Tokens** (21 total)
```python
<|assumptions|>  # Ranked risks
<|tests|>        # Falsifiable experiments
<|time_violence|> # TV calculations
<|time_dividend|> # TD distribution
<|metrics|>      # C-ROI calculations
<|trust_evidence|> # Source citations
<|compliance|>   # Constraint checks
```

**2. Calculation Functions**
```python
from cofounderchat.conscious_tools import tv_ops, conscious_index, roi_conscious

# Calculate Time Violence
ops = tv_ops(arr_rate=10, svc_rate=12, var_arr=4, var_svc=2, tau=8)
# → 16.33 hours

# Calculate Consciousness Index
c = conscious_index(tv_human=20, tv_total=100)
# → 0.80 (80% automated)

# Calculate Conscious ROI
roi = roi_conscious(rev=5000, dtvh=15, v_t=35)
# → {'c_roi': 5542.80, 'time_value': 525.00}
```

**3. Tool-Augmented Generation**

Model emits parameters:
```
<|time_violence|> arr_rate=10, svc_rate=12, var_arr=4, var_svc=2, tau=8
```

Engine computes and injects:
```
Ops_Score = 16.33 hours
```

Result is auditable and non-hallucinated (like calculator tool).

---

## Files Changed from nanochat

### Modified
- `cofounderchat/tokenizer.py` (+12 special tokens)
- `cofounderchat/engine.py` (+150 lines, conscious tool integration)
- `scripts/mid_train.py` (added Conscious Economics data mixture)
- `scripts/chat_sft.py` (added SFT templates, schema validation)

### New
- `cofounderchat/conscious_tools.py` (calculation engine)
- `tasks/conscious_validation_data.py` (20 examples)
- `tasks/conscious_sft_templates.py` (16 perfect examples)
- `tasks/conscious_biz_math.py`, `experiment_cards.py`, `compliance_drills.py` (task wrappers)
- `tasks/founder_tv_eval.py`, `td_accounting_eval.py`, `trust_compliance_eval.py` (evaluation)
- `tests/test_conscious_tools.py` (34 unit tests)

See [CONSCIOUS_ECONOMICS.md](CONSCIOUS_ECONOMICS.md) for details.

---

## Testing

### Run Validation Test (Local, $0)

```bash
source .venv/bin/activate
python test_validation_pattern.py
```

Tests if a tiny model can learn to emit Conscious Economics blocks.

### Run Unit Tests

```bash
# Conscious tools tests (34 tests)
python -m pytest tests/test_conscious_tools.py -v

# Tokenizer tests
python -m pytest tests/test_rustbpe.py -v
```

### Verify Evaluation Tasks

```bash
python -m tasks.founder_tv_eval      # Time Violence calculation accuracy
python -m tasks.td_accounting_eval   # Time Dividend accounting
python -m tasks.trust_compliance_eval # Trust & compliance checks
```

---

## Questions & Support

cofounderchat is designed to be short and hackable. Package it up and ask your favorite LLM:

```bash
files-to-prompt . -e py -e md -e rs -e html -e toml -e sh --ignore "*target*" --cxml > packaged.txt
```

Or browse with [DeepWiki](https://deepwiki.com/) (change github.com → deepwiki.com in URL).

---

## Contributing

CofounderChat is actively being developed. Currently building:
- Full training dataset (170K+ examples)
- Advanced evaluation metrics
- RL optimization for Time Violence reduction

**Current focus:** Infrastructure complete (70%), data generation next.

---

## Acknowledgements

**CofounderChat is built on:**
- [nanochat](https://github.com/karpathy/nanochat) by Andrej Karpathy - minimal ChatGPT training pipeline
- [nanoGPT](https://github.com/karpathy/nanoGPT) - pioneered minimal, hackable LLM training  
- [modded-nanoGPT](https://github.com/KellerJordan/modded-nanogpt) - gamified training with metrics
- [HuggingFace](https://huggingface.co/) for fineweb and smoltalk datasets
- [Lambda](https://lambda.ai/service/gpu-cloud) for GPU compute
- Chief LLM whisperer 🧙‍♂️ Alec Radford for nanochat guidance

**Conscious Economics framework:**
- Developed by Leo Guinan / Bottega 1010
- Time Violence formalization
- Conscious ROI methodology
- Trust & compliance principles

---

## Cite

If you use CofounderChat in your research:

```bibtex
@misc{cofounderchat,
  author = {Leo Guinan},
  title = {CofounderChat: Conscious AI Co-founder trained on Time Violence reduction},
  year = {2025},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/leoguinan/cofounderchat}},
  note = {Built on nanochat by Andrej Karpathy}
}
```

For the base nanochat framework:

```bibtex
@misc{nanochat,
  author = {Andrej Karpathy},
  title = {nanochat: The best ChatGPT that $100 can buy},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/karpathy/nanochat}
}
```

---

## License

MIT (inherited from nanochat)
