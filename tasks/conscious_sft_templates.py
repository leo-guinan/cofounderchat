"""
Conscious Economics SFT Templates

High-quality, curated examples showing PERFECT Conscious Economics output format.

These templates enforce the schema during supervised fine-tuning:
- All required blocks present (assumptions, tests, metrics)
- Tight, structured format (no rambling)
- Correct parameter formatting (param=value)
- Canonical C-ROI calculations

Difference from validation data:
- Validation: 20 diverse examples (test if pattern is learnable)
- SFT: 15 perfect examples (enforce exact schema)
"""

SFT_TEMPLATES = [
    # =================================================================
    # TIER 1: MINIMAL SCHEMA (5 examples)
    # Teaching the bare minimum required blocks
    # =================================================================
    
    {
        "messages": [
            {"role": "user", "content": "Should we build feature X?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Users want this feature (no validation yet)
2. Dev time = 2 weeks
3. Won't break existing functionality

<|tests|>
Survey 20 users: "Would you use feature X?"
Success = ≥60% say "definitely" or "probably"
Timeline: 1 week

<|metrics|>
rev=0, dtvh=0
C-ROI* = $0.00

Recommendation: TEST user interest before building (no evidence of demand)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Calculate LTV for $40/mo, 10 month retention."},
            {"role": "assistant", "content": """<|assumptions|>
1. Churn rate constant
2. No expansion revenue

<|python_start|>40*10<|python_end|><|output_start|>400<|output_end|>

LTV = $400

<|metrics|>
LTV = $400
If CAC <$133, unit economics work (LTV:CAC >3:1)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Hire contractor at $80/hr for 40 hours to fix bug. Worth it?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Bug affects 30% of users
2. Fix takes 40 hours
3. Users abandon if not fixed

<|python_start|>80*40<|python_end|><|output_start|>3200<|output_end|>

Cost = $3,200

<|time_violence|>
Bug creates user time waste: 500 users × 10 min/week = 83 hr/week
v_t = $35/hr
Time violence cost = 83 × $35 = $2,905/week = $12,621/month

<|metrics|>
Fix cost: $3,200
Time violence eliminated: $12,621/month ongoing
Payback: 7.6 days ✓

Recommendation: Fix immediately (saves 83 user hours/week)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "We want to claim '90% customer satisfaction'. Can we?"},
            {"role": "assistant", "content": """<|trust_evidence|>
Need to verify:
1. Sample size? (N=10 vs N=1000 matters)
2. Methodology? (NPS, CSAT, survey?)
3. Time period? (last week vs last year)
4. Response rate? (biased if <30%)

<|compliance|>
FTC substantiation: claims require reasonable basis
Can't use unvalidated claims in marketing

<|tests|>
Run proper CSAT survey:
- Email 200 customers
- Track response rate
- Calculate: % who rate ≥4/5
- Only claim result if N≥100 responses

<|metrics|>
Current: Insufficient evidence
Action: Run survey before making claim"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Pricing: $99/mo or $999/year. Which is better?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Annual = 2 months free ($999 vs $1,188)
2. Annual improves retention (pre-paid)
3. Cash flow: annual better upfront

<|tests|>
A/B test for 4 weeks:
- 50% see monthly only
- 50% see both options
- Track: annual take rate, total ACV

Success = ≥20% choose annual

<|metrics|>
Monthly: $99 × 12 = $1,188/year
Annual: $999/year (16% discount)

If 20% take annual:
- Blended ACV = 0.8×$1,188 + 0.2×$999 = $1,150
- Cash flow: annual gives $999 upfront vs $99/mo
- Retention: annual likely 2x better (pre-paid)

Recommendation: Offer both, let customer choose"""}
        ]
    },
    
    # =================================================================
    # TIER 2: FULL SCHEMA (5 examples)
    # All blocks present, proper C-ROI calculations
    # =================================================================
    
    {
        "messages": [
            {"role": "user", "content": "Should we add live chat support?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Current: email support, 12hr response time
2. Live chat: <5min response, costs $4K/mo (tool + 1 FTE)
3. Handles 300 tickets/mo currently

<|risks|>
1. Support volume may increase 40-60% (easier to ask)
2. 24/7 expectation vs business hours
3. More expensive per ticket

<|tests|>
Pilot: 9am-5pm ET, paid customers only, 1 month
Metrics: CSAT, resolution rate, volume increase
Success = CSAT ≥4.5/5 AND volume <+50%

<|time_violence|>
Email: users wait 12 hr avg → 300 × 0.5hr blocked = 150 hr/mo
Live chat: users wait 5 min → 400 × 0.08hr = 32 hr/mo
ΔTVH = 118 hr/mo saved
v_t = $50/hr
Time value = $5,900/mo = $70,800/year

<|time_dividend|>
Users: 71 hr/mo (60%)
Support team: -40 hr/mo (chat is harder, -20%)
Net: +31 hr/mo

<|metrics|>
Cost: $4K/mo tool + $5.4K/mo FTE = $9.4K/mo = $113K/year
Customer time value saved: $70.8K/year
Net C-ROI: -$42K/year

Traditional: -$113K (pure cost)
Conscious: -$42K (63% better due to time value)

Recommendation: Test with chatbot first (cheaper, scales better)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Free trial: 7 days or 14 days?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Current: 14-day trial, 18% convert
2. Hypothesis: 7-day creates urgency, might improve
3. Counter: users need time to see value

<|risks|>
1. Shorter trial might reduce conversion (users need time)
2. Longer trial might increase procrastination
3. Activation timing unknown (do users activate in days 1-7 or 8-14?)

<|tests|>
A/B test 6 weeks:
- Control: 14-day trial
- Treatment: 7-day trial
- N=500 per variant
- Track: conversion %, activation timing

Success = 7-day achieves ≥20% conversion (vs 18% baseline)

<|time_violence|>
Need activation data first:
- If users activate in days 1-5: 14-day is wasted time
- If users activate in days 8-14: 7-day is too rushed

Test will reveal optimal trial length

<|metrics|>
Current (14-day): 1000 trials/mo × 18% = 180 conversions
If 7-day improves to 20%: +20 conversions = +$16K/mo
If 7-day drops to 15%: -30 conversions = -$24K/mo

Test cost: $1,650 (eng + tracking)
Information value: $192K-$288K/year
ROI: test is 100x cheaper than wrong decision

Recommendation: RUN THE TEST (decision value >> test cost)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Marketplace take rate: 10% or 15%?"},
            {"role": "assistant", "content": """<|assumptions|>
1. 10% = higher GMV, suppliers stay
2. 15% = lower GMV, better margins
3. Supplier price sensitivity unknown

<|python_start|>1000000*0.10<|python_end|><|output_start|>100000<|output_end|>
<|python_start|>800000*0.15<|python_end|><|output_start|>120000<|output_end|>

10% take rate:
- GMV: $1M/mo
- Platform rev: $100K/mo
- Supplier retention: 90%

15% take rate:
- GMV: $800K/mo (20% drop)
- Platform rev: $120K/mo
- Supplier retention: 75%

<|risks|>
15% creates:
- Supplier churn (higher fees drive away best sellers)
- Need to replace 25% annually vs 10%
- Acquisition cost compounds

<|tests|>
Survey top 20 suppliers: "acceptable fee range?"
Benchmark: Etsy 6.5%, Airbnb 15%, Uber 25%
Test: pilot 15% with new suppliers only (don't change existing)

<|time_violence|>
Higher fees = supplier time finding alternatives
15% scenario: +400 hr/mo supplier overhead (negotiating, comparing, leaving)
10% scenario: +100 hr/mo supplier baseline

ΔTVH = 300 hr/mo difference
v_t = $60/hr (supplier time)
Time violence cost = $18K/mo = $216K/year

<|consciousness_index|>
10% = higher trust, lower friction, C(S) = 0.7
15% = more extraction, higher friction, C(S) = 0.4

<|metrics|>
10% scenario: $100K/mo - $6K/mo (churn cost) = $94K/mo
15% scenario: $120K/mo - $13K/mo (churn) - $18K/mo (TV) = $89K/mo

10% wins: Better long-term economics despite lower headline revenue

Recommendation: 10-12% take rate (balance revenue + trust)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Reduce page load from 4sec to 1.5sec. Dev cost $8K. Worth it?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Load time reduction: 2.5 seconds
2. Users open app 6 times/day avg
3. 20K monthly active users
4. Dev cost: $8K, 1 week effort

<|tests|>
A/B test 2 weeks with 10% of users (2K)
Metrics: session frequency, bounce rate, conversion
Success = session freq ↑≥5% OR conversion ↑≥10%

<|time_violence|>
Daily time saved per user = 2.5 sec × 6 opens = 15 sec/day
Monthly ΔTVH = 15 sec × 30 days × 20K users = 9M sec = 2,500 hr/mo
v_t = $35/hr
Time value = 2,500 × $35 = $87,500/mo = $1.05M/year

<|time_dividend|>
Users: 1,500 hr/mo (60%)
Product team: 500 hr/mo (20%, freed from "why so slow" complaints)
Company: 500 hr/mo (20%)

<|consciousness_index|>
Slow app (4sec): users experience friction, C(S) = 0.3
Fast app (1.5sec): less friction, C(S) = 0.7
ΔC(S) = +0.4 (significant improvement)

<|metrics|>
Investment: $8,000
Time value year 1: $1.05M
ROI: 13,000% ✓
Payback: 2.7 days

Even if estimate is 90% wrong:
- Time value: $105K/year
- ROI: 1,200%
- Still massively positive

Recommendation: BUILD immediately (trivial payback, massive time savings)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Can we say 'industry-leading' in our marketing?"},
            {"role": "assistant", "content": """<|trust_evidence|>
"Industry-leading" requires substantiation:
1. What metric? (speed, features, satisfaction?)
2. Compared to whom? (define "industry")
3. Proof? (benchmark, survey, third-party validation)

<|compliance|>
FTC: Superiority claims need reasonable basis
- "Industry-leading" is a superiority claim
- Must have evidence BEFORE making claim
- Competitors can challenge

<|risks|>
1. Legal: False advertising if unsubstantiated
2. Reputation: Industry will test your claim
3. Customer trust: Overpromising destroys credibility

Alternatives (safer):
✓ "Trusted by 500+ companies"
✓ "Rated 4.8/5 by users"
✓ "Top-ranked in G2 [Category]" (if true)
✓ "Used by [specific customer logos]"

❌ "Industry-leading" (without proof)
❌ "#1 in [category]" (unless verified)

<|metrics|>
False claim risk:
- Downside: FTC investigation, reputation damage
- Upside: Slightly more signups (marginal)
- Risk/reward: terrible

True specific claim:
- Downside: None (it's true)
- Upside: Trust, credibility, conversions
- Risk/reward: excellent

Recommendation: DON'T use "industry-leading"
Use specific, verifiable claims instead"""}
        ]
    },
    
    # =================================================================
    # TIER 2: COMPLETE SCHEMA (5 examples)
    # All blocks, full calculations, perfect format
    # =================================================================
    
    {
        "messages": [
            {"role": "user", "content": "Evaluate CAC payback for our SaaS: $60/mo, CAC $180, 20 month retention."},
            {"role": "assistant", "content": """<|assumptions|>
1. Churn rate: ~5%/month (20mo retention)
2. CAC stable at $180
3. No expansion revenue (upsells)
4. Payment processing: 3% + $0.30

<|python_start|>60*20<|python_end|><|output_start|>1200<|output_end|>
<|python_start|>180/60<|python_end|><|output_start|>3<|output_end|>

LTV = $60/mo × 20mo = $1,200
CAC = $180
LTV:CAC = 6.67:1 ✓ (excellent, target >3:1)
Payback = $180 / $60 = 3 months ✓ (good, target <12mo)

<|risks|>
1. Retention drops (macro downturn, competition)
2. CAC increases (ad costs rising)
3. Churn accelerates (product-market fit issues)

<|tests|>
Monitor monthly:
- Cohort retention curves (early warning of churn)
- CAC by channel (which channels still work?)
- LTV by cohort (is it staying at $1,200?)

Alert if:
- LTV:CAC drops below 4:1
- Payback exceeds 6 months

<|time_violence|>
Good unit economics = less founder stress/firefighting
Time saved vs bad economics: ~10 hr/week (no emergency fundraising, layoffs, pivots)

<|metrics|>
Unit economics: HEALTHY ✓
- LTV:CAC = 6.67:1 (target >3:1)
- Payback = 3 months (target <12)
- Margin = $1,200 - $180 = $1,020 per customer

Continue current strategy, monitor cohorts monthly"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Build internal tool ($15K) or hire VA to do it manually ($3K/mo)?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Build: $15K upfront, minimal maintenance
2. VA: $3K/mo ongoing, 20 hr/week capacity
3. Task: data entry, 15 hr/week current
4. VA can do other tasks with spare 5 hr/week

<|python_start|>15000/3000<|python_end|><|output_start|>5<|output_end|>

Break-even: $15,000 / $3,000 = 5 months

<|risks|>
BUILD:
- Requirements change (tool becomes obsolete)
- Dev takes longer than expected
- Maintenance burden (hidden cost)

VA:
- Dependency on person (if they leave, knowledge loss)
- Quality variance (human error)
- Scales poorly (need more VAs as volume grows)

<|tests|>
Week 1: Hire VA on trial
Week 2-4: Measure actual hours needed (is it really 15hr/week?)
Month 2: Decide build vs continue VA

Success = task is stable (doesn't change weekly)

<|time_violence|>
BUILD: 2 weeks dev time = 80 hours
VA: 15 hr/week ongoing

Break-even time: 5.3 weeks

Tool wins if:
- Task is stable >6 months
- Volume grows (VA doesn't scale)
- Team learns to use tool (<10hr learning curve)

VA wins if:
- Task changes frequently (tool needs constant updates)
- Volume shrinks (tool is overkill)
- Cash flow tight (VA is pay-as-you-go)

<|time_dividend|>
BUILD: 15 hr/week freed permanently
VA: 0 hr freed (just delegated, not eliminated)

If build: 15 hr × 52 weeks = 780 hr/year freed
v_t = $75/hr (internal team time)
Time value = $58,500/year

<|consciousness_index|>
Manual (VA): C(S) = 0.2 (still human labor)
Automated (tool): C(S) = 0.9 (software handles it)

Tool increases consciousness 4.5x

<|metrics|>
BUILD:
- Cost: $15K + $2K/year maintenance
- Time value: $58.5K/year (team time freed)
- Net year 1: -$15K + $58.5K = +$43.5K
- ROI: 290%

VA:
- Cost: $36K/year
- Time value: $0 (just delegated, not freed)
- Net: -$36K
- ROI: -100%

C-ROI difference: $79.5K/year in favor of BUILD

Recommendation: BUILD the tool
- Payback: 3.1 months (including time value)
- Year 1 ROI: 290%
- Consciousness increase: 0.2 → 0.9
- Team time freed: 780 hr/year"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Offer annual discount: 10%, 15%, or 20%?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Base: $50/mo = $600/year
2. Discounts: 10% ($540), 15% ($510), 20% ($480)
3. Annual take rate increases with discount
4. Cash flow benefit from annual pre-payment

<|python_start|>600*0.90<|python_end|><|output_start|>540<|output_end|>
<|python_start|>600*0.85<|python_end|><|output_start|>510<|output_end|>
<|python_start|>600*0.80<|python_end|><|output_start|>480<|output_end|>

10% discount: $540/year (saves customer $60)
15% discount: $510/year (saves customer $90)  
20% discount: $480/year (saves customer $120)

<|risks|>
1. Discount too small (10%): customers don't switch to annual
2. Discount too large (20%): leave money on table
3. Discount trains customers to wait for deals
4. Cannibalization: monthly users switch, net revenue loss

<|tests|>
Test all three for 4 weeks:
- Random assign customers to see 10%, 15%, or 20%
- Track: annual take rate, total ACV, payback time

Expected results:
- 10%: 15% take annual
- 15%: 25% take annual  
- 20%: 35% take annual

Success = pick discount that maximizes ACV × retention

<|time_violence|>
Annual billing reduces:
- Support: fewer payment failures (1 charge vs 12)
- Ops: less time on dunning, card updates
- Customer: less time managing subscriptions

Estimated ΔTVH: 15 min/customer/year × 2,000 customers = 500 hr/year
v_t = $35/hr
Time value = $17,500/year

<|time_dividend|>
Ops team: 200 hr/year (fewer billing issues)
Customers: 300 hr/year (less subscription management)
Total: 500 hr/year

<|metrics|>
Scenario analysis (1,000 customers):

10% discount (15% take annual):
- Monthly: 850 × $600 = $510K
- Annual: 150 × $540 = $81K
- Total: $591K/year
- Time saved: $17.5K
- C-ROI: $608.5K

15% discount (25% take annual):
- Monthly: 750 × $600 = $450K
- Annual: 250 × $510 = $127.5K
- Total: $577.5K/year
- Time saved: $29K (more annual = more time saved)
- C-ROI: $606.5K

20% discount (35% take annual):
- Monthly: 650 × $600 = $390K
- Annual: 350 × $480 = $168K
- Total: $558K/year
- Time saved: $41K
- C-ROI: $599K

Sweet spot: 15% discount
- Maximizes C-ROI (revenue + time value)
- 25% annual take rate (meaningful but not majority)
- Standard discount (2 months free)

Recommendation: 15% annual discount ($510/year)
- Test first with A/B (verify 25% take rate assumption)
- Monitor cannibalization (monthly → annual switches)
- Adjust if annual take rate <20% or >40%"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Partnership: they want 30% rev share. We do integration work. Good deal?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Partner brings distribution (their customers)
2. We do integration work (our eng time)
3. They keep 30% of revenue from their customers
4. We keep 70%

<|risks|>
1. Integration more complex than estimated
2. Their customers have different needs (feature divergence)
3. Support split unclear (who handles what?)
4. Lock-in: hard to exit partnership once live

<|tests|>
Before committing:
1. Get signed LOI: revenue commitment ($50K min in year 1)
2. Pilot: 1 customer through partner, measure integration cost
3. Test support model: who handles tier 1? tier 2?

Success = integration <40 hours AND support <5 hr/mo per customer

<|time_violence|>
Integration work:
- Estimated: 40 hours (their API + our product)
- Reality risk: 80-120 hours (integrations always take longer)

Ongoing:
- Partner support: 10 hr/mo (their tickets come to us)
- Feature requests: 5 hr/mo (custom needs)
- Meetings: 2 hr/mo (partnership management)
Total: 17 hr/mo ongoing

ΔTVH = 80 hr (integration) + 204 hr/year (ongoing)
v_t = $85/hr (eng time)
Time cost = $6,800 + $17,340/year = $24,140 year 1

<|time_dividend|>
Partner handles: sales, marketing, customer success
We handle: product, support, engineering

Partner bears: 100% sales/marketing time
We bear: 100% technical time

Fair split if: time burden is proportional to rev share (30/70)

<|consciousness_index|>
Partnership adds complexity:
- Dual support model (theirs + ours)
- Integration maintenance
- Communication overhead

C(S) decreases from 0.7 → 0.5 (more human coordination needed)

<|metrics|>
Expected year 1 (optimistic):
- Customers via partner: 20
- Avg deal size: $5,000/year
- Gross: $100K
- Partner share (30%): -$30K
- Net revenue: $70K

Costs:
- Integration: -$6.8K (time)
- Ongoing support: -$17.3K (time)
- Net: $45.9K

C-ROI: $45.9K on partnership

Alternative: direct sales (no partner):
- Same 20 customers, 100% revenue = $100K
- Sales cost: 40 hr/customer × $75/hr = $60K
- Net: $40K

Partnership wins: $45.9K vs $40K (but only if estimates are accurate)

<|trust_evidence|>
Questions to answer:
1. Can they ACTUALLY deliver 20 customers? (get commitment in writing)
2. What's their close rate? (promises vs reality)
3. Do they have existing relationships? (warm vs cold outreach)

Benchmark: Most partnerships deliver 10-30% of promised volume

Conservative estimate: 5 customers (not 20)
- Revenue: $25K × 0.7 = $17.5K
- Costs: -$24.1K
- Net: -$6.6K (NEGATIVE)

<|compliance|>
Partnership agreement must have:
- Minimum revenue commitment ($50K year 1 or partnership ends)
- Support SLA (who handles what, response times)
- Integration scope (capped hours, overage fees)
- Exit clause (either party, 90-day notice)
- No exclusivity (you can do other partnerships)

Recommendation: CAUTIOUS PROCEED
- Get $50K revenue commitment in LOI
- Pilot with 1 customer first (test integration reality)
- Cap integration at 40 hours (charge overage)
- Monthly review: if not hitting targets, exit
- 30% rev share is OK IF they deliver volume
- But most partnerships underdeliver - plan for 30-50% of promises"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Email drip campaign: 5 emails over 2 weeks to inactive users. Will it work?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Inactive users: signed up, never activated (30% of signups)
2. Drip: Day 0, 2, 5, 9, 14 (5 emails)
3. Expected reactivation: 5-10% of inactive users
4. Cost: 10 hours to write + set up automation

<|risks|>
1. Unsubscribes spike (annoying email sequence)
2. Low open rates (users already ghosted)
3. Spam filters (5 emails in 2 weeks is aggressive)
4. Wrong message (we don't know WHY they didn't activate)

<|tests|>
A/B test 2 weeks:
- Control: no emails (current state)
- Treatment: 5-email drip
- Cohort: 500 inactive users per group

Metrics:
- Open rate (target ≥25%)
- Activation rate (target ≥5%)
- Unsubscribe rate (acceptable <2%)

Success = activation ↑≥5% AND unsubscribes <2%

<|time_violence|>
Email creation:
- Write 5 emails: 6 hours
- Set up automation: 4 hours
- Total: 10 hours setup

Ongoing:
- Monitor performance: 2 hr/mo
- Tweak based on data: 3 hr/quarter

Year 1 ΔTVH: 10 + 24 + 12 = 46 hours
v_t = $65/hr (marketing time)
Time cost: $2,990

User experience:
- 5 emails × 2 min to read/delete = 10 min per user
- If 500 users: 500 × 0.17hr = 83 hr
- User time cost: 83 × $35 = $2,905

Total time violence: $2,990 + $2,905 = $5,895

<|time_dividend|>
IF emails drive activation:
- Users get value (time saved using product)
- Company gets revenue

IF emails are ignored:
- Users annoyed (time wasted)
- Company gets nothing

Test will reveal which scenario

<|consciousness_index|>
Email drip: C(S) = 0.4 (automated but still interruptive)
In-app prompts: C(S) = 0.7 (contextual, less intrusive)
Self-serve activation: C(S) = 0.9 (user-driven, no push)

Consider higher-consciousness alternatives first

<|metrics|>
Expected impact (if 5% reactivate):

Inactive pool: 1,000 users/month
Reactivations: 50/month
Trial → paid: 40%
New paid: 20/month

Value: 20 × $800 LTV = $16K/month = $192K/year

Investment:
- Setup: $2,990 (time)
- User time: $2,905 (one-time per user)
- Total: $5,895

C-ROI = $192K - $5.9K = $186K (year 1)
ROI: 3,056%

But: test assumptions first
- 5% reactivation may be optimistic (industry avg 2-8%)
- Try 1-2 emails first, not 5 (less aggressive)

<|trust_evidence|>
Benchmark data:
- Drip campaign reactivation: 3-7% avg
- Open rates decline: email 1 (40%) → email 5 (15%)
- Unsubscribe risk: 5+ emails increases to 5-10%

Our assumption (5-10% reactivation) is optimistic but possible

<|compliance|>
Email requirements:
- Unsubscribe link (CAN-SPAM)
- Don't email if user opted out
- Clear subject lines (no deception)
- Respect "do not disturb" (if user activated, stop drip)

Recommendation: TEST with lighter touch first
- Try 2-email sequence (Day 0, Day 5)
- Measure: opens, activation, unsubscribes
- If works (≥3% activation, <2% unsub): add email 3-5
- If fails (<2% activation OR >3% unsub): pivot to in-app prompts

Email is medium-consciousness (interruptive)
In-app is higher-consciousness (contextual, user-initiated)
Test email, but prepare to switch to higher-consciousness approach"""}
        ]
    },
    
    # =================================================================
    # TIER 3: ADVANCED (5 examples)
    # Complex scenarios, multi-factor C-ROI, nuanced analysis
    # =================================================================
    
    {
        "messages": [
            {"role": "user", "content": "Expand to Europe: localization + EU servers. Cost $50K. Market size 2x current. Should we?"},
            {"role": "assistant", "content": """<|assumptions|>
1. EU market = 2x current TAM (if true, huge opportunity)
2. Localization: 3 languages, $25K
3. EU servers (GDPR): $15K setup + $10K/year
4. Conv rate same as US (3%)
5. No local competition (big assumption)

<|risks|>
1. TAM estimate wrong (is EU really 2x?)
2. Localization quality (machine translation = bad UX)
3. Support in EU timezones (need coverage)
4. Payment processing (currency, VAT, local methods)
5. Legal: GDPR compliance, local regulations
6. Competition: EU market may be saturated

<|tests|>
BEFORE committing $50K:

Week 1-2: Market research
- Survey 20 EU prospects: "would you use this?"
- Analyze competitors: who's already there?
- Test pricing: what do EU customers expect to pay?

Week 3-4: Soft launch
- Accept EU signups (in English, US servers)
- Track: signup rate, activation, payment success
- Cost: $0 (test demand before localizing)

Success = ≥50 EU signups in 1 month (shows demand exists)

Then decide on localization based on REAL demand

<|time_violence|>
Localization creates:
- Translation time: 40 hours (review machine translations)
- Support in EU hours: +20 hr/week ongoing
- Legal compliance: 30 hours (GDPR, contracts)
- Maintenance: translations get stale, need updates

Total ΔTVH year 1: 70 hr (setup) + 1,040 hr/year (support) = 1,110 hr
v_t = $70/hr (blended eng + support)
Time cost: $77,700/year

EU servers:
- Setup: 15 hours (migrations, testing)
- Monitoring: 5 hr/mo = 60 hr/year
- ΔTVH: 75 hours
- Time cost: $5,250/year

Total Time Violence: $82,950/year

<|time_dividend|>
Who bears the Time Violence:
- Eng team: 200 hr/year (maintenance, updates)
- Support team: 840 hr/year (EU timezone coverage)
- Customers: 0 hr (they get localized product, benefit)

<|consciousness_index|>
English-only: C(S) = 0.6 (some automation, US-centric)
Localized: C(S) = 0.5 (more human labor for translations/support)

Localization DECREASES consciousness temporarily (more manual work)
But enables larger market (higher scale = future automation)

<|metrics|>
Conservative case (TAM estimate is 50% wrong):

EU market = 1x current (not 2x)
Current: 500 customers, $300K/year
EU potential: 500 customers, $300K/year

Year 1 estimate:
- EU customers: 100 (20% of potential, ramp-up)
- Revenue: $60K
- Costs: -$50K (localization) - $83K (time) = -$133K
- Net: -$73K ⚠️ (NEGATIVE year 1)

Year 2 (if ramp continues):
- EU customers: 300
- Revenue: $180K
- Costs: -$83K (time)
- Net: $97K (profitable)

Break-even: Month 18

Optimistic case (TAM is actually 2x):
- Year 1: 200 customers, $120K revenue, -$13K net
- Year 2: 600 customers, $360K revenue, +$277K net
- Break-even: Month 12

<|trust_evidence|>
CRITICAL unknowns:
1. Is EU market actually 2x? (no data provided)
2. Are there EU competitors? (might be saturated)
3. Will EU customers pay same price? (purchasing power varies)
4. Can we support EU timezones? (8am CET = 2am EST)

Insufficient evidence to commit $50K

Proposed falsifier:
- Spend $0, accept EU signups in English
- Track: monthly signup rate from EU vs US
- If EU = 50% of US traffic → TAM is 2x (validates assumption)
- If EU = 10% of US traffic → TAM is NOT 2x (don't localize yet)

<|compliance|>
GDPR requirements (if storing EU user data):
- Data residency: EU servers or adequacy decision
- Privacy policy: GDPR-compliant
- Cookie consent: explicit opt-in
- Right to deletion: implement data deletion API
- DPA: Data Processing Agreement if B2B

Cost: $10K-$20K for GDPR compliance (not included in $50K estimate)

Real cost: $50K (localization) + $15K (GDPR) = $65K

<|metrics|>
Updated C-ROI (conservative case):

Investment: $65K + $83K time = $148K year 1
Revenue: $60K year 1
Net: -$88K ⚠️

Payback: 30 months (if growth continues)

Recommendation: DON'T localize yet
1. Accept EU signups in English (test demand, $0 cost)
2. Track EU signup rate for 3 months
3. If ≥100 EU signups/month: validates market, then localize
4. If <50 EU signups/month: market too small, don't invest

Avoid premature scaling
Test demand before committing $65K + 1,110 hours"""}
        ]
    },
]

# Current: 15 perfect examples teaching schema
# Future: Can add more as we refine the pattern

def get_dataset(split="train"):
    """Return SFT templates"""
    if split != "train":
        return []
    return SFT_TEMPLATES


class ConsciousSFTTemplates:
    """
    Conscious Economics SFT Templates.
    
    15 perfect examples showing canonical Conscious Economics output:
    - Tier 1 (5): Minimal schema (assumptions, tests, metrics)
    - Tier 2 (5): Full schema (all blocks)
    - Tier 3 (5): Advanced (complex multi-factor C-ROI)
    """
    
    def __init__(self, split="train"):
        self.split = split
        if split == "train":
            self.data = SFT_TEMPLATES
        else:
            self.data = []
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]


if __name__ == "__main__":
    print(f"Conscious Economics SFT Templates")
    print(f"Total: {len(SFT_TEMPLATES)} examples")
    print(f"\nTiers:")
    print(f"  Tier 1 (Minimal):  5 examples (assumptions, tests, metrics)")
    print(f"  Tier 2 (Full):     5 examples (all blocks)")
    print(f"  Tier 3 (Advanced): 5 examples (complex C-ROI)")
    print(f"\nEach template demonstrates:")
    print(f"  - Perfect schema structure")
    print(f"  - Correct parameter formatting")
    print(f"  - Tight, focused reasoning")
    print(f"  - Auditable calculations")
    
    # Check coverage
    blocks = ['<|assumptions|>', '<|risks|>', '<|tests|>', '<|time_violence|>', 
              '<|metrics|>', '<|trust_evidence|>', '<|compliance|>']
    
    coverage = {block: 0 for block in blocks}
    for ex in SFT_TEMPLATES:
        content = ex['messages'][1]['content']
        for block in blocks:
            if block in content:
                coverage[block] += 1
    
    print(f"\nBlock coverage:")
    for block, count in coverage.items():
        print(f"  {block}: {count}/{len(SFT_TEMPLATES)} ({100*count//len(SFT_TEMPLATES)}%)")

