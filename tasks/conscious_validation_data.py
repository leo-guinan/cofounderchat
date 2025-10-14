"""
Conscious Economics Validation Dataset

20 gold-standard examples for testing if the model can learn 
to emit Conscious Economics blocks correctly.

Dataset breakdown:
- 10 Conscious-BizMath examples (unit economics + Time Violence)
- 5 Experiment Card examples (hypothesis → test → C-ROI)
- 5 Compliance Drill examples (trust/evidence requirements)
"""

# Gold-standard examples teaching Conscious Economics reasoning
VALIDATION_EXAMPLES = [
    # =================================================================
    # CONSCIOUS-BIZMMATH (10 examples)
    # Teaching: LTV/CAC/payback + Time Violence calculations
    # =================================================================
    
    {
        "messages": [
            {"role": "user", "content": "Calculate unit economics for a SaaS product: $50/month subscription, 18 month average retention, $200 customer acquisition cost. Also estimate time saved if product reduces user admin time by 2 hours per week."},
            {"role": "assistant", "content": """<|assumptions|>
1. Churn rate remains constant at ~5.5%/month
2. Users actually utilize the time-saving features
3. CAC stays consistent with current channels

<|python_start|>50*18<|python_end|><|output_start|>900<|output_end|>

LTV = $50/mo × 18mo = $900
CAC = $200
LTV:CAC ratio = 4.5:1 ✓ (healthy, target is >3:1)
Payback period = $200 / $50 = 4 months ✓

<|time_violence|>
ΔTVH = 2 hr/week × 52 weeks/yr × 1.5 yr avg retention = 156 hours saved per customer
v_t = $35/hr (shadow price of time)
Time value = 156 hr × $35/hr = $5,460

<|time_dividend|>
Users: 93.6 hr (60%)
Navigators: 31.2 hr (20%)
Company: 31.2 hr (20%)

<|metrics|>
C-ROI per customer = LTV + Time Value
= $900 + $5,460 = $6,360 total value created

Traditional view: $900 LTV
Conscious view: $6,360 (7.1x multiplier from time value)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Should we invest in reducing our app load time from 3.5 seconds to 1.2 seconds? Dev cost is $15K, affects 50K monthly active users."},
            {"role": "assistant", "content": """<|assumptions|>
1. Users open app avg 8 times/day
2. Load time reduction = 2.3 seconds saved
3. Dev effort = 2 weeks, maintenance minimal
4. User retention improves with faster load

<|tests|>
A/B test with 10% of users (5K) for 2 weeks
Success metrics:
- Session frequency ↑ ≥5% (p<0.05)
- Time-to-first-action ↓ ≥2sec
- App rating ↑ ≥0.1 stars

<|time_violence|>
Daily time saved per user = 2.3 sec × 8 opens = 18.4 sec/day
Monthly ΔTVH = 18.4 sec × 30 days × 50K users = 27,600,000 sec = 7,667 hours/month
v_t = $35/hr
Monthly time value = 7,667 hr × $35 = $268,345/month

<|time_dividend|>
Users: 4,600 hr/mo (60%)
Navigators: 1,533 hr/mo (20%)
Company: 1,533 hr/mo (20%)

<|metrics|>
Investment: $15,000 (one-time)
Time value: $268,345/month ongoing
Payback: 15,000 / 268,345 = 0.056 months = 1.7 days ✓

C-ROI first year = $268K × 12 - $15K = $3.2M
Traditional ROI might only capture increased conversions (~$50K/yr)
Conscious ROI is 64x larger due to cumulative time savings"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Evaluate: marketplace take rate of 15% vs 20%. Revenue model comparison."},
            {"role": "assistant", "content": """<|assumptions|>
1. 15% take rate: Higher transaction volume, lower revenue per transaction
2. 20% take rate: Lower volume, higher revenue per transaction
3. Suppliers more likely to leave at 20%
4. Platform value must justify the take rate

<|python_start|>1000000*0.15<|python_end|><|output_start|>150000<|output_end|>
<|python_start|>800000*0.20<|python_end|><|output_start|>160000<|output_end|>

Scenario A (15% take rate):
- Est. monthly GMV: $1M
- Platform revenue: $150K/mo
- Supplier retention: 85%

Scenario B (20% take rate):
- Est. monthly GMV: $800K (20% drop due to price sensitivity)
- Platform revenue: $160K/mo
- Supplier retention: 70%

<|time_violence|>
Higher take rate (20%) creates:
- Ops_Score: suppliers spend more time finding alternatives, negotiating
- Info_Score: pricing complexity, hidden fee confusion
- Estimated ΔTVH: +500 hr/month in supplier overhead

Lower take rate (15%) creates:
- Ops_Score: smoother transactions, less friction
- Info_Score: clearer pricing, better trust
- Estimated ΔTVH: -200 hr/month (reduced vs 20%)

<|trust_evidence|>
Survey data needed: supplier NPS at different rate tiers
Benchmark: similar marketplaces (Etsy 6.5%, Airbnb 15%, Uber 25%)
Our sweet spot likely 12-18% based on value provided

<|metrics|>
15% scenario: $150K/mo revenue - $7K/mo (time violence cost) = $143K net
20% scenario: $160K/mo revenue - $17.5K/mo (churn + TV cost) = $142.5K net

Recommendation: 15% take rate
- Slightly lower immediate revenue
- Much better long-term retention
- Lower Time Violence = higher Consciousness Index
- Suppliers stay longer, platform compounds"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Calculate CAC payback for freemium model: 2% convert to paid ($29/mo), avg CAC is $120 per signup (not per paid user)."},
            {"role": "assistant", "content": """<|assumptions|>
1. 2% freemium → paid conversion rate
2. CAC = $120 per signup (blended across free + paid)
3. Paid users stay avg 14 months
4. Free users provide data/network effects

<|python_start|>120/0.02<|python_end|><|output_start|>6000<|output_start|>

Effective CAC per paid user = $120 / 0.02 = $6,000
(You're paying to acquire 50 free users to get 1 paid user)

<|python_start|>29*14<|python_end|><|output_start|>406<|output_end|>
LTV = $29/mo × 14mo = $406

LTV:CAC = $406 / $6,000 = 0.068:1 ⚠️ WARNING
(Target is >3:1, you're at 0.07:1 - this is unsustainable)

Payback period = $6,000 / $29 = 207 months = 17.2 years ⚠️

<|risks|>
1. Burning capital at massive rate
2. Free users create support costs without revenue
3. Conversion rate (2%) may be overestimated
4. Paid retention (14mo) may decline

<|tests|>
Immediate tests needed:
1. Track cohort conversion: month 1, 3, 6, 12 (might be <2%)
2. Measure free user support burden (time cost)
3. Test higher-touch onboarding to boost conversion
4. Consider freemium → free trial model instead

<|metrics|>
Current model is value-destructive
Need to either:
- 10x conversion rate (2% → 20%) - unlikely
- Cut CAC by 90% ($120 → $12) - hard but possible
- Increase LTV 10x ($406 → $4,000) - longer retention or higher price

OR: pivot to different acquisition model entirely"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Estimate ROI of hiring a customer success manager. Salary $80K, they can handle 200 accounts, current churn is 8%/month."},
            {"role": "assistant", "content": """<|assumptions|>
1. CSM reduces churn from 8% → 5%/month (37.5% reduction)
2. CSM handles 200 accounts at steady state
3. Avg account value = $500/month
4. CSM fully productive month 2 onwards

<|python_start|>500*200*0.03*12<|python_end|><|output_start|>36000<|output_end|>

Churn reduction impact:
- Current churn: 8%/month × 200 accounts = 16 accounts/mo lost
- With CSM: 5%/month × 200 accounts = 10 accounts/mo lost  
- Accounts saved: 6/month × $500 = $3,000/mo = $36,000/yr

Annual revenue saved: $36,000
CSM cost: $80,000 (salary) + $20,000 (benefits/overhead) = $100,000

Traditional ROI = ($36K - $100K) / $100K = -64% ⚠️ (Looks bad)

<|time_violence|>
WITHOUT CSM:
- Ops_Score: Customers struggle with self-service, 200 tickets/mo
- Support team handles escalations: 80 hr/mo
- Customer time wasted: ~400 hr/mo (avg 2hr/lost customer × 200)

WITH CSM:
- Ops_Score: Proactive outreach prevents issues
- Support escalations: 30 hr/mo (62.5% reduction)
- Customer time saved: 250 hr/mo
- ΔTVH = 50 hr/mo (support team) + 250 hr/mo (customers) = 300 hr/mo

v_t = $35/hr (internal) + $50/hr (customer time, higher value)
Time value = (50 hr × $35) + (250 hr × $50) = $1,750 + $12,500 = $14,250/mo

<|time_dividend|>
Support team: 30 hr/mo (freed up for other work)
Customers: 150 hr/mo (60%)
CSM efficiency: 50 hr/mo (20%)
Company: 50 hr/mo (20%)

<|metrics|>
C-ROI per year:
Revenue saved: $36,000
Time value: $14,250/mo × 12 = $171,000
Total value: $207,000
Cost: $100,000
Net C-ROI: $107,000 (107% ROI) ✓

Traditional view: -64% ROI (looks like bad hire)
Conscious view: +107% ROI (excellent hire)
Multiplier: Time value is 4.75x the revenue impact"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Build vs buy for internal analytics dashboard. Build cost $40K, buy cost $2K/month. Which is better?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Build: 6 weeks dev time, $40K (contractors)
2. Build: ongoing maintenance 10 hr/month
3. Buy: $2K/month SaaS, 2 hours setup
4. Buy: limited customization, 80% feature fit
5. Team size: 12 people using analytics

<|python_start|>2000*12<|python_end|><|output_start|>24000<|output_end|>
<|python_start|>40000/24000<|python_end|><|output_start|>1.666<|output_end|>

Financial break-even:
- Buy: $24K/year
- Build: $40K upfront + ~$8K/year maintenance (10hr/mo × $67/hr dev rate)
- Break-even: 40,000 / (24,000 - 8,000) = 2.5 years

If retention >2.5 years → build is cheaper
If retention <2.5 years → buy is cheaper

<|time_violence|>
BUILD option:
- Ops_Score: 6 weeks of dev time = 240 hours
- Info_Score: Team waits 6 weeks for analytics (decision delays)
- Maintenance: 10 hr/month ongoing
- Custom fit: exactly what team needs (low friction)

BUY option:  
- Ops_Score: 2 hours setup, immediate value
- Info_Score: Learning curve for 12 people × 3 hr each = 36 hours
- Workarounds: missing features = 20% tasks still manual → 8 hr/month
- Vendor dependency: renewal negotiation, integration changes

Build ΔTVH: -240 hr upfront, -10 hr/month ongoing
Buy ΔTVH: -2 hr setup, -36 hr learning, -8 hr/month workarounds

<|time_dividend|>
Build scenario time investment:
Dev team: 240 hr (upfront) + 120 hr/year
User team: 0 hr learning (perfect fit)

Buy scenario time investment:
Setup: 2 hr
User team: 36 hr learning + 96 hr/year workarounds

<|trust_evidence|>
Need to answer:
1. How critical is perfect feature fit? (build wins)
2. Will requirements change? (buy is more flexible)
3. What's the cost of 6-week delay? (buy wins on speed)
4. Is this core competency? (probably not)

<|metrics|>
C-ROI analysis (3-year horizon):

BUILD:
- Cost: $40K + $24K (maintenance) = $64K
- Time violence: 240 + 360 = 600 hours
- Time cost: 600 × $67 = $40,200
- Total: $104,200

BUY:
- Cost: $72K (3 years)
- Time violence: 2 + 36 + 288 = 326 hours  
- Time cost: 326 × $50 = $16,300
- Total: $88,300

Recommendation: BUY
- 15% cheaper in total economic cost
- 45% less Time Violence
- Faster time-to-value (immediate vs 6 weeks)
- Less risk (can switch vendors)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Price increase: $49/mo to $79/mo. We have 1,200 customers. Estimate impact."},
            {"role": "assistant", "content": """<|assumptions|>
1. Current: 1,200 customers × $49/mo = $58,800/mo
2. Price sensitivity: expect 15-25% churn from increase
3. New customer acquisition at $79 continues normally
4. No grandfather clause (all customers see increase)

<|risks|>
1. Price increase may trigger churn wave (15-25%)
2. Brand damage if handled poorly
3. Competitor opportunity (they could poach during transition)
4. Support volume spike (complaints, questions)

<|tests|>
Staged rollout test:
Week 1: Survey 100 customers - "would you pay $79?"
Week 2: Pilot with 50 customers (4%), monitor churn
Week 3: If churn <20%, roll out to next 200 (total 21%)
Week 4: Full rollout if pilot successful

<|python_start|>1200*0.20*49<|python_end|><|output_start|>11760<|output_end|>
<|python_start|>1200*0.80*79<|python_end|><|output_start|>75840<|output_end|>

Scenario A (20% churn):
- Customers remaining: 960
- New MRR: 960 × $79 = $75,840
- Previous MRR: $58,800
- Net gain: $17,040/mo (+29%) ✓

Scenario B (30% churn - worst case):
- Customers remaining: 840
- New MRR: 840 × $79 = $66,360
- Net gain: $7,560/mo (+13%)

Scenario C (10% churn - best case):
- Customers remaining: 1,080  
- New MRR: 1,080 × $79 = $85,320
- Net gain: $26,520/mo (+45%)

<|time_violence|>
Price increase execution creates:
- Support load: 200 tickets, 80 hours handling complaints
- Customer time: 1,200 × 15min evaluating = 300 hours
- Decision paralysis: some customers delay/defer for weeks

ΔTVH = 80 hr (support) + 300 hr (customers) = 380 hours one-time
v_t = $50/hr (weighted avg)
Time cost = $19,000 one-time

<|compliance|>
Requirements:
- 30-day notice minimum
- Clear communication of value props
- Grandfather option for annual contracts (legal obligation)
- Refund policy for dissatisfied customers first month

<|metrics|>
Expected case (20% churn):
Revenue gain: $17,040/mo × 12 = $204,480/yr
Minus time violence cost: $19,000 (one-time)
Minus churn recovery CAC: 240 customers × $200 = $48,000
Net first-year gain: $137,480

C-ROI = 234% (on execution cost)

Recommendation: Proceed with price increase
- Stage the rollout (test with 4%, then 21%, then 100%)
- Over-communicate value justification
- Offer annual plans at slight discount to lock in
- Monitor churn daily during rollout, pause if >25%"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Should we offer a white-label version of our software? Enterprise clients asking for it. Development cost ~$120K."},
            {"role": "assistant", "content": """<|assumptions|>
1. White-label dev: $120K (6 months, 2 engineers)
2. Target: 3-5 enterprise deals in year 1
3. Deal size: $50K-$150K/year per enterprise
4. Ongoing: custom support, isolated instances

<|risks|>
1. Support complexity multiplies (each tenant is different)
2. Brand dilution (they market as their own)
3. Feature divergence (custom requests pull roadmap)
4. You become infrastructure, not product
5. Hard to sunset (contractual lock-in)

<|tests|>
Before building white-label:
1. Get 2 signed LOIs at $80K+ ARR minimum
2. Pilot with 1 design partner (co-build)
3. Test support load (shadow their instance for 1 month)
4. Validate they actually close enterprise deals (not just interest)

Success criteria:
- $160K ARR from 2 customers (break-even in 9 months)
- Support load <20 hr/month per tenant
- No feature divergence >10% from core product

<|time_violence|>
WHITE-LABEL model creates:
- Ops_Score: multi-tenant complexity, deployment overhead
- Support per tenant: 20 hr/month × 3 tenants = 60 hr/month
- Engineering tax: 30% of roadmap becomes custom work
- Info_Score: tribal knowledge, one-off fixes, documentation sprawl

Estimated ΔTVH: +60 hr/month support + 40 hr/month eng = 100 hr/month
v_t = $75/hr (eng time is expensive)
Time cost = $7,500/month = $90K/year

STANDARD SaaS model (counterfactual):
- Support: 5 hr/month per enterprise customer
- Engineering: shared roadmap, no divergence
- Estimated ΔTVH: +15 hr/month
- Time cost = $1,125/month = $13,500/year

DELTA = $90K - $13.5K = $76.5K/year in Time Violence

<|consciousness_index|>
White-label: Humans carry 80% of complexity (C(S) = 0.20)
Standard SaaS: Automation carries 60% (C(S) = 0.60)

Moving to white-label REDUCES consciousness (0.60 → 0.20)
This is moving backward on automation curve

<|metrics|>
Year 1 C-ROI:
Revenue: 3 tenants × $80K = $240K
Dev cost: -$120K
Time violence: -$90K (ongoing support/eng tax)
Net: $30K (12.5% ROI)

Year 2 C-ROI (if it works):
Revenue: 5 tenants × $80K = $400K
Time violence: -$150K (5 tenants × $30K)
Net: $250K (better, but still high TV)

Alternative: Standard enterprise plan (no white-label)
Revenue: 5 customers × $30K = $150K (less per customer)
Dev cost: $20K (minor enterprise features)
Time violence: -$13.5K
Net: $116.5K (78% ROI, less revenue but WAY better economics)

<|trust_evidence|>
Questions to answer:
1. Why do they want white-label? (control, brand, or just feature request in disguise?)
2. Will they actually close deals? (or are you building their POC for free?)
3. Can you charge 5-10x more to justify the complexity? ($80K → $400K+)

<|compliance|>
If you proceed:
- Minimum $150K/year per tenant (justify complexity)
- Limit custom development to <10% roadmap
- SLA with support hour caps (overage fees)
- Exit clause after year 1 (must be mutual)

Recommendation: DON'T build white-label yet
- Get 2 signed contracts at $150K+ first
- Test with manual white-labeling (CSS/logos only, not full multi-tenant)
- See if "enterprise features" satisfy them instead
- Time Violence cost is 2x-3x higher than standard SaaS
- Consciousness Index decreases (bad sign)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Referral program design: give $50 to referrer and referee for each successful referral. Avg LTV is $800. Good idea?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Referral incentive: $100 total per successful referral ($50 each side)
2. LTV = $800 per customer
3. Current CAC = $250 (baseline)
4. Referral close rate: 25-40% (better than cold leads)

<|python_start|>100/800<|python_end|><|output_start|>0.125<|output_end|>

Referral CAC = $100 per successful referral
As % of LTV: 12.5% (very good, baseline is $250 = 31% of LTV)

Payback: $100 / $50/mo = 2 months (excellent)

<|tests|>
Pilot program (month 1):
- Limit to 50 power users (most engaged)
- Track: referral rate, quality of referred customers, activation rate
- Success metrics:
  * >10% of users make ≥1 referral
  * Referred customers have ≥80% activation rate vs organic
  * Fraud/gaming <5%

<|time_violence|>
Referral program creates:
- Ops_Score: tracking, payouts, fraud detection
- Estimated support: 5 hr/month managing program
- Customer time to refer: 5 min per referral × est 200 referrals/mo = 17 hr/month

Without program:
- Customer time: 0 (but also 0 referrals)
- Organic WOM: some free referrals happen anyway

Net ΔTVH = +17 hr/month customer time + 5 hr/month ops = 22 hr/month
v_t = $35/hr  
Time cost = $770/month

BUT: referral time is WILLING time (they're helping friends), not violence
Reframe: this is low-friction sharing, not forced complexity

<|risks|>
1. Fraud/gaming (fake accounts, wash trading)
2. Quality dilution (referring bad-fit customers for $50)
3. Expectation creep (customers expect payment for WOM)
4. Referral cannibalization (would've signed up anyway)

<|compliance|>
Requirements:
- Clear terms: referee must be new customer, activate within 30 days
- Fraud detection: same payment method, same IP, same device = reject
- Payout timing: after referee pays for month 2 (prevents gaming)
- Tax implications: $50 is taxable income (must issue 1099 if >$600/year)

<|metrics|>
Expected monthly performance:
- Referrals sent: 200 (from 10% of 2,000 user base)
- Conversion rate: 30%
- Successful referrals: 60/month
- Cost: 60 × $100 = $6,000/month
- New revenue: 60 × $50 = $3,000/month (month 1)
- LTV of cohort: 60 × $800 = $48,000

Month 1 C-ROI: -$6,000 (payouts) + $3,000 (revenue) = -$3,000
Month 2-16: +$3,000/month (avg retention 16mo)
Total: -$3,000 + ($3,000 × 16) = $45,000 net from cohort

ROI on referral spend: $45,000 / $6,000 = 750% ✓

Conscious adjustment:
- Time value of 22 hr/month = $770/month cost
- But this is willing participation (low violence)
- Customer delight from helping friends (positive experience)

Recommendation: PROCEED with referral program
- Start with $50/$50 pilot
- Cap at 60 referrals/month initially (manage quality)
- Track referee quality closely (activation, retention, LTV)
- Consider tiered rewards ($75 for enterprise referrals)
- Much better CAC than paid acquisition ($100 vs $250)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Evaluate adding live chat support. Current: email-only (12hr response time). Live chat: immediate, but costs $4K/month for tool + 1 FTE at $50K/year."},
            {"role": "assistant", "content": """<|assumptions|>
1. Current: email support, 12-hour avg response time, 300 tickets/month
2. Live chat: <5 min response, handles 500 tickets/month (chat + email)
3. Tool cost: $4K/month ($48K/year)
4. FTE support rep: $50K salary + $15K benefits = $65K/year
5. Total cost: $48K + $65K = $113K/year

<|risks|>
1. Live chat = always-on expectation (nights/weekends?)
2. Support volume may increase 40-60% (easier to ask = more asks)
3. Quality vs speed tradeoff (fast but shallow answers)
4. Burnout: chat is more intense than email

<|tests|>
Month 1 pilot:
- Add live chat 9am-5pm ET only
- Limit to paid customers (not free tier)
- Track: response time, resolution rate, customer satisfaction, volume increase
- Success: CSAT ≥4.5/5, volume increase <50%, resolution rate >80%

<|time_violence|>
EMAIL-ONLY model:
- Customer waits 12 hours avg
- 300 tickets/month × 12 hr wait = 3,600 hours customer time blocked
- Back-and-forth: 2.5 exchanges avg × 12 hr = 30 hr per ticket resolution
- Total customer ΔTVH: ~9,000 hr/month waiting

LIVE CHAT model:
- Customer waits 5 min avg
- 500 tickets/month × 0.08 hr (5min) = 40 hours customer time blocked
- Resolution: 1.2 exchanges avg × 0.08 hr = instant fixes
- Total customer ΔTVH: ~60 hr/month waiting

REDUCTION: 9,000 - 60 = 8,940 hr/month saved
v_t = $50/hr (customer time is valuable)
Time value = 8,940 × $50 = $447,000/month = $5.36M/year ⚠️

(This seems high - let's sanity check)

Actually: customers aren't "blocked" 12 hours, they're async working
Real blocked time: ~30 min per ticket (context switching, checking email)
Email model: 300 × 0.5 hr = 150 hr/month
Live chat: 500 × 0.08 hr = 40 hr/month
Realistic ΔTVH: 110 hr/month saved

Realistic time value: 110 × $50 = $5,500/month = $66K/year

<|time_dividend|>
Time saved breakdown:
Customers: 66 hr/month (blocked time reduction)
Support team: -80 hr/month (chat is MORE intensive than email)
Net: -14 hr/month (slightly more Time Violence on team)

<|consciousness_index|>
Email: Async, batched, customer waits (low consciousness)
Live chat: Sync, immediate, but human-intensive (medium consciousness)
Self-service docs: Automated, instant, no human needed (high consciousness)

Live chat is MEDIUM consciousness (better than email, worse than self-service)

<|metrics|>
C-ROI analysis:
Cost: $113K/year
Customer time value saved: $66K/year
Revenue impact: hard to quantify (better experience → retention)

Traditional ROI: -$113K (pure cost center)
Conscious ROI: -$113K + $66K = -$47K (still negative, but 58% better)

Alternative: invest $40K in self-service docs + chatbot
- Higher consciousness (automates common questions)
- Scales better (handles unlimited volume)
- Lower Time Violence (instant answers, no human queue)

<|trust_evidence|>
Benchmarks needed:
- Competitors: do they offer live chat? (industry standard?)
- Churn analysis: does support quality drive retention?
- Conversion: does trial → paid improve with better support?

If support quality drives retention, C-ROI becomes positive via saved churn

<|compliance|>
If you proceed:
- Set clear hours (9am-9pm ET, 7 days? or business hours only?)
- SLA: response time <5min, resolution time <1 hour
- Escalation path: complex issues → email ticket (don't force sync for async-appropriate)
- Self-service first: chatbot + docs deflect 40-60% before human

Recommendation: HYBRID approach
Phase 1 (now): Invest in self-service docs + chatbot ($40K)
- Higher consciousness, lower Time Violence
- Deflects 50% of simple questions

Phase 2 (6 months): Add live chat IF:
- Support volume still high after docs
- Churn analysis shows support quality drives retention
- Can justify with revenue impact data

Don't jump straight to live chat - it's expensive and increases team Time Violence
Fix the root cause (better docs) before adding human bandaid"""}
        ]
    },
    
    # =================================================================
    # EXPERIMENT CARDS (5 examples)
    # Teaching: Hypothesis → Test → C-ROI workflow
    # =================================================================
    
    {
        "messages": [
            {"role": "user", "content": "Should we add a free tier to our SaaS product to drive growth?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Free tier attracts 10x more signups than paid-only
2. Conversion from free → paid is 2-5%
3. Free users create support load (avg 2 tickets/year)
4. Free tier drives network effects / virality

<|risks|>
1. Cannibalization: existing customers downgrade to free
2. Support burden: 1,000 free users × 2 tickets = 2,000 tickets/year
3. Server costs: hosting free users with no revenue
4. Brand dilution: free tier perceived as "cheap" version

<|tests|>
**One-week experiment:**
Launch limited free tier (max 500 users) with waitlist

Success metrics:
- Signup rate ↑ ≥5x vs current
- Free → paid conversion ≥2% by week 4
- Support tickets from free users <3 per user/year
- Paid user churn unchanged (<1% downgrade)

Pass/fail threshold:
- Pass: 10+ free users convert to paid in first month
- Fail: <5 conversions OR support tickets >4/user/year

<|time_violence|>
Free tier creates:
- Support load: 500 users × 0.5 ticket/month = 250 tickets/month = 100 hr/month
- Ops overhead: managing upgrades, limits, billing edge cases = 10 hr/month
- Total ΔTVH: +110 hr/month

Paid-only (current):
- Support: 200 users × 0.3 ticket/month = 60 tickets/month = 24 hr/month
- Ops overhead: 2 hr/month

Net Time Violence increase: 110 - 26 = 84 hr/month
v_t = $65/hr (support + ops time)
Time cost: 84 × $65 = $5,460/month

<|time_dividend|>
Who bears the Time Violence:
- Support team: 76 hr/month (handling free tier questions)
- Ops team: 8 hr/month (infrastructure, limits)
- Free users: 50 hr/month (learning curve, hitting limits)

<|metrics|>
Expected C-ROI (month 1):
Free users: 500
Conversions to paid: 10 (2% conversion rate)
New MRR: 10 × $49 = $490

Cost:
- Development: $8,000 (one-time, feature flagging + limits)
- Time violence: $5,460/month
- Server costs: $200/month

Month 1: -$8,000 - $5,460 - $200 + $490 = -$13,170
Break-even: Need 112 conversions to pay back development ($8K / ($49/mo × 1.4 LTV multiplier))

If conversion rate holds at 2%:
- Need 5,600 free users to get 112 conversions
- At 500/month growth rate: 11.2 months to break-even

<|trust_evidence|>
Insufficient evidence - need to test assumptions:
1. Is 2% conversion realistic? (industry avg 1-4%)
2. Will free users stay engaged? (might ghost immediately)
3. Does free tier help paid acquisition? (freemium vs free trial)

Proposed falsifier:
Run 1-week test with 50-100 free users, measure engagement daily

<|compliance|>
Free tier requirements:
- Clear limits (e.g., 100 items, 1 workspace, basic features only)
- Upgrade prompts (show value of paid, not nagware)
- Support policy: community forum for free, email for paid only
- No credit card required (reduces friction)

Recommendation: TEST first, don't commit
- Week 1: 50 users, measure engagement + support load
- Week 2: If promising, expand to 200 users
- Week 3: Measure conversion rate reality (vs assumption)
- Decision point: proceed only if conversion ≥2% AND support <3 tickets/user/year"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Test whether personalized onboarding emails increase activation rate."},
            {"role": "assistant", "content": """<|assumptions|>
1. Current: Generic welcome email, 35% activation rate (complete onboarding)
2. Personalized: Role-based emails (by signup info), expect 45-50% activation
3. Cost: 20 hours to write templates + set up automation
4. Send window: Day 0, 2, 5, 10 (4-email sequence)

<|tests|>
**A/B test design:**
- Duration: 2 weeks
- Cohort size: 400 signups (200 control, 200 treatment)
- Control: current generic emails
- Treatment: personalized by role (engineer, marketer, founder, ops)

Success metrics:
- Activation rate ↑ from 35% → ≥42% (20% relative improvement)
- Email open rate ≥40%
- Reply rate ≥2% (engagement signal)

Pass/fail:
- Pass: Activation ≥42% AND statistically significant (p<0.05)
- Fail: <38% OR not statistically significant

<|time_violence|>
Personalization setup:
- Write 4 role-based templates × 4 emails = 16 email variants
- Setup automation: segment by role, triggers, A/B logic
- Total: 20 hours one-time

Generic (current):
- 1 template × 4 emails = 4 emails
- Already done, 0 incremental time

Ongoing:
- Personalized: 2 hr/month tweaking based on data
- Generic: 0 hr/month

ΔTVH: +20 hr one-time, +2 hr/month ongoing

Time cost (year 1): (20 + 24) × $65/hr = $2,860

<|metrics|>
Impact calculation (assuming 2,000 signups/month):

Current activation:
- 2,000 × 0.35 = 700 activations/month

Personalized activation (if 45%):
- 2,000 × 0.45 = 900 activations/month
- Delta: +200 activations/month

LTV per activation: $800 (avg customer value)
Value gain: 200 × $800 = $160,000/month
Annual value: $1.92M

C-ROI:
Investment: $2,860 (time) + $0 (software, using existing tools)
Return: $1.92M/year
ROI: 67,000% ✓

Even if improvement is only 5% (35% → 37%):
- Delta: +40 activations/month
- Value: $384K/year
- ROI: 13,400% ✓

<|time_dividend|>
Time saved by activated users:
- Higher activation = users get value faster
- Estimated user time saved: 30 min per activated user (less frustration, faster time-to-value)
- 200 users × 0.5 hr = 100 hr/month user time saved
- v_t = $50/hr
- User time value: $5,000/month = $60K/year

Total C-ROI = $1.92M (revenue) + $60K (time value) = $1.98M

<|trust_evidence|>
Prior evidence:
- Case studies: personalization improves email performance 20-40% (open rates)
- Activation benchmark: industry avg 30-40% for SaaS
- Our baseline (35%) is average, room to improve

Test will provide:
- Direct measurement of our specific use case
- Role-level breakdown (which segments respond best)
- Email-level insights (which emails in sequence matter most)

<|compliance|>
Email requirements:
- Unsubscribe link in every email (CAN-SPAM)
- Don't send if user already activated (avoid spam perception)
- Respect email preferences (if they opt out of marketing, respect it)
- A/B test must be random assignment (no cherry-picking)

Recommendation: RUN THE TEST
- Extremely high potential ROI (13,000%+ even in pessimistic case)
- Low cost ($2,860)
- Low risk (worst case: no improvement, revert to generic)
- 2-week timeline to decision
- Can start this week with existing tools"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Should we redesign our pricing page? Current conversion is 2.3%, industry benchmark is 3-4%."},
            {"role": "assistant", "content": """<|assumptions|>
1. Current pricing page: 2.3% conversion (visitor → trial signup)
2. Industry benchmark: 3-4% conversion
3. Traffic: 5,000 visitors/month to pricing page
4. Redesign cost: $6,000 (designer + developer, 1 week)

<|risks|>
1. Redesign might DECREASE conversion (worse than current)
2. Designer may not understand messaging/positioning
3. A/B test duration needs sufficient sample size
4. Psychological: new page feels "different" (recency bias)

<|tests|>
**A/B test protocol:**
- Split: 50% current page, 50% new design
- Duration: 4 weeks (need ~5,000 visitors per variant)
- Primary metric: trial signup conversion rate
- Secondary: time on page, scroll depth, pricing tier clicks

Success criteria:
- New design achieves ≥2.8% conversion (20% improvement, p<0.05)
- If ≥3.2%, roll out to 100% immediately (40% improvement)
- If <2.5%, revert and iterate

Minimum detectable effect: 0.3% absolute (2.3% → 2.6%)
Confidence: 95%
Power: 80%

<|time_violence|>
Redesign process:
- Discovery: stakeholder interviews, competitor analysis = 8 hours
- Design: wireframes, mockups, iterations = 16 hours
- Development: implement, QA, A/B setup = 20 hours
- Total: 44 hours

Current page:
- 0 hours (already exists)

A/B test monitoring:
- Daily checks, data analysis, decision meetings = 10 hours over 4 weeks

Total ΔTVH: 44 + 10 = 54 hours
v_t = $80/hr (design + dev blended rate)
Time cost: $4,320

Additional: designer fee $6,000
Total cost: $10,320

<|metrics|>
Expected impact (if we hit 3% conversion):

Current:
- 5,000 visitors × 2.3% = 115 signups/month

Improved:
- 5,000 visitors × 3.0% = 150 signups/month
- Delta: +35 signups/month

Trial → paid conversion: 40%
New paid customers: 35 × 0.40 = 14/month

LTV per customer: $800
Monthly value gain: 14 × $800 = $11,200
Annual value: $134,400

C-ROI:
Investment: $10,320
Return (year 1): $134,400
ROI: 1,202% ✓

Payback: $10,320 / $11,200 = 0.92 months

Even at modest improvement (2.3% → 2.6%):
- Delta: +15 signups/month
- New customers: 6/month
- Value: $57,600/year
- ROI: 458% ✓

<|time_dividend|>
Improved pricing page reduces visitor Time Violence:
- Clearer value props = faster decision (2 min saved per visitor)
- Better pricing structure = less confusion
- Visitor time saved: 5,000 × 0.033 hr (2 min) = 165 hr/month
- v_t = $40/hr (visitor time)
- Time value: 165 × $40 = $6,600/month = $79,200/year

Total C-ROI = $134,400 (revenue) + $79,200 (time) = $213,600

<|trust_evidence|>
Evidence to gather during test:
- Heatmaps: where do visitors look? where do they drop off?
- Session recordings: watch 20-30 visitor sessions (qualitative)
- Exit surveys: "why didn't you sign up?" (0-5 responses expected)
- Competitor analysis: what do high-converting pages do differently?

Existing evidence:
- Current page hasn't been updated in 18 months
- User feedback: "pricing is confusing" (3 mentions in last quarter)
- Competitor pages are clearer, more visual

<|compliance|>
Test requirements:
- Random assignment (no geo/time biasing)
- Consistent experience (once assigned to variant, user sees same one)
- Track full funnel: page view → signup → activation → paid
- Privacy: anonymize visitor data, no PII in analytics

Design principles:
- Maintain price transparency (don't hide pricing)
- Clear CTA buttons (high contrast, obvious)
- Social proof if available (customer logos, testimonials)
- FAQ section (address common objections)

Recommendation: PROCEED with redesign + A/B test
- High ROI potential (458%-1,202%)
- Low cost ($10K)
- Low risk (A/B test = can revert if worse)
- 4-week timeline to results
- Even modest gains (0.3% improvement) justify the investment
- Visitor Time Violence reduction adds $79K/year in value"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Experiment: add video tutorials to reduce support volume. Cost to produce: $12K for 10 videos. Worth it?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Current support: 400 tickets/month, avg handle time 30 min = 200 hr/month
2. Videos deflect 30-40% of common questions
3. Production cost: $12K (10 videos, professional quality)
4. Video topics: top 10 support questions (cover 60% of volume)

<|tests|>
**Phased rollout test:**

Week 1-2: Produce 3 pilot videos (most common questions)
- Cost: $3,600
- Place in help center + email to active users
- Track: views, completion rate, support ticket reduction

Week 3-4: Measure impact
- Did tickets on those 3 topics decrease ≥30%?
- Are users watching videos? (completion rate ≥60%)
- User feedback: helpful? (survey 20-30 watchers)

Decision point:
- If ≥25% deflection + ≥50% completion → produce remaining 7 videos
- If <20% deflection → pivot to written docs instead (cheaper, scannablele)

Success metrics:
- Support tickets ↓ 120/month (30% of 400)
- Video completion rate ≥60%
- User satisfaction ≥4/5 ("videos were helpful")

<|time_violence|>
VIDEO production:
- Scripting: 10 videos × 2 hr = 20 hours
- Recording: 10 × 1 hr = 10 hours
- Editing: 10 × 3 hr = 30 hours
- Total: 60 hours internal time + $12K external (videographer)

Internal time cost: 60 × $65/hr = $3,900
Total: $12K + $3.9K = $15,900

WRITTEN DOCS (alternative):
- Writing: 10 guides × 3 hr = 30 hours
- Screenshots: 10 × 1 hr = 10 hours
- Total: 40 hours × $65/hr = $2,600

Video is 6x more expensive than written docs

<|metrics|>
Support deflection value:

Current:
- 400 tickets/month × 0.5 hr = 200 hr/month
- Support cost: 200 × $30/hr = $6,000/month

With videos (30% deflection):
- 280 tickets/month × 0.5 hr = 140 hr/month
- Support cost: 140 × $30/hr = $4,200/month
- Savings: $1,800/month = $21,600/year

ROI:
Investment: $15,900
Savings: $21,600/year
Payback: 8.8 months
Year 1 ROI: 36%

Customer time saved:
- 120 fewer tickets/month
- Avg customer time per ticket: 15 min (writing, waiting, reading response)
- Customer time saved: 120 × 0.25 hr = 30 hr/month
- v_t = $50/hr
- Customer time value: 30 × $50 = $1,500/month = $18,000/year

Total C-ROI = $21,600 (support savings) + $18,000 (customer time) = $39,600
ROI on $15,900: 149% ✓

<|consciousness_index|>
Support model evolution:
- Email support: C(S) = 0.1 (humans do everything)
- Written docs: C(S) = 0.6 (self-service, but requires reading)
- Video tutorials: C(S) = 0.7 (visual learning, easier than docs)
- Interactive tutorials: C(S) = 0.9 (in-app, contextual)

Videos improve consciousness vs email, but written docs are 6x cheaper

Alternative: Hybrid approach
- Written docs for 7 topics ($1,820)
- Videos for 3 most complex topics ($4,770)
- Total: $6,590 (58% cheaper than all-video)

<|time_dividend|>
Support time freed up: 60 hr/month
Reinvest in:
- Proactive help content (write more docs)
- Product improvements (reduce need for support)
- Customer success (higher-value interactions)

<|trust_evidence|>
Questions to answer in pilot:
1. Do users actually watch videos? (vs prefer written docs)
2. Do videos reduce tickets, or do users still email? (deflection reality)
3. Are 3 videos enough, or need all 10? (minimum effective dose)

Benchmarks:
- SaaS video completion rates: 40-70%
- Support deflection from content: 20-40%
- Our assumptions are industry-standard

<|compliance|>
Video requirements:
- Closed captions (accessibility)
- Hosting: YouTube (free) or Vimeo (paid, more professional)
- Keep videos short (<5 min each, ideally 2-3 min)
- Update plan: review every 6 months, remake if product changes

Recommendation: PILOT with 3 videos first
- Produce 3 videos on most common questions ($4,770 all-in)
- Measure deflection over 4 weeks
- If successful (≥25% deflection), produce remaining 7
- If not successful, pivot to written docs (cheaper, scannablele)
- Don't commit to full $15.9K until pilot validates assumptions
- Hybrid approach (docs + videos) might be optimal (58% cheaper)"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Test 7-day free trial vs 14-day. Which converts better?"},
            {"role": "assistant", "content": """<|assumptions|>
1. Current: 14-day free trial, 18% convert to paid
2. Hypothesis: 7-day trial creates urgency, might improve conversion
3. Counter-hypothesis: 14-day gives more time to realize value, higher quality conversions
4. Evaluation period: 4-6 weeks

<|risks|>
1. Shorter trial might reduce conversions (users need time to evaluate)
2. Longer trial might delay decisions (procrastination)
3. Trial length might matter less than activation (did they use it?)
4. Competitors offer 14-day trials (market expectation)

<|tests|>
**A/B test design:**
- Variant A: 7-day trial (treatment)
- Variant B: 14-day trial (control)
- Duration: 6 weeks (need 500+ trials per variant)
- Random assignment at signup

Metrics to track:
1. Trial → paid conversion rate (primary)
2. Time to first activation (secondary)
3. Feature usage during trial (engagement)
4. Trial → paid timing (when do they convert?)

Success criteria:
- If 7-day ≥20% conversion (vs 18% baseline), consider switching
- If 14-day maintains 18% and higher engagement, keep it
- Statistical significance: p<0.05

Decision framework:
- 7-day wins if: conversion ≥20% AND revenue/trial is equal or higher
- 14-day wins if: 7-day conversion <17% OR users need more time to activate

<|time_violence|>
Test setup:
- Engineering: add trial length parameter to signup flow = 4 hours
- Analytics: set up tracking, funnels, cohort analysis = 6 hours
- Monitoring: daily checks, weekly reviews = 12 hours over 6 weeks
- Total: 22 hours

Time cost: 22 × $75/hr = $1,650

User experience:
7-DAY trial creates urgency:
- Users compress evaluation into 1 week (time pressure)
- Potential stress: "need to decide fast"
- Estimated user time: 3 hours (setup + eval + decision) compressed into 7 days

14-DAY trial allows breathing room:
- Users spread evaluation over 2 weeks (less pressure)
- Potential procrastination: "I'll check it out later" → ghost
- Estimated user time: 3 hours spread over 14 days

Net user Time Violence: similar total time, but 7-day has higher intensity

<|metrics|>
Current performance (14-day trial):
- 1,000 trials/month × 18% = 180 conversions/month
- LTV per customer: $800
- Monthly value: 180 × $800 = $144,000

Scenario A: 7-day improves conversion to 20%
- 1,000 trials × 20% = 200 conversions/month
- Monthly value: $160,000
- Gain: $16,000/month = $192K/year

Scenario B: 7-day reduces conversion to 15%
- 1,000 trials × 15% = 150 conversions/month
- Monthly value: $120,000
- Loss: -$24,000/month = -$288K/year

Expected value:
- 40% chance: 7-day improves to 20% → +$192K/year
- 60% chance: 7-day reduces to 15% → -$288K/year
- EV = (0.4 × $192K) + (0.6 × -$288K) = -$96K

Risk: downside is larger than upside, but test will tell us which scenario is real

C-ROI of test:
Investment: $1,650
Information value: knowing optimal trial length is worth $192K-$288K/year
ROI: test is dirt cheap relative to decision value

<|trust_evidence|>
Existing research:
- SaaS trial benchmarks: 7-day (higher urgency), 14-day (higher value realization), 30-day (enterprise)
- Conversion rates: 7-day (15-25%), 14-day (10-20%), 30-day (5-15%)
- Our 18% is good for 14-day trial

What we don't know:
- Do OUR users need 7 or 14 days to see value?
- Is activation happening in first 3 days? (if so, 14 days is wasted)
- Does trial length correlate with retention? (longer trial = stickier customers?)

<|compliance|>
Test requirements:
- Clear messaging: "7-day trial" vs "14-day trial" (no ambiguity)
- Email reminders: day 1, day 3 (for 7-day), day 1, day 7 (for 14-day)
- No bait-and-switch: assigned trial length is final
- Extension policy: if user requests more time, what do we do? (decide before test)

Fair test conditions:
- Both groups get same onboarding emails
- Both groups get same feature access
- Only difference is trial duration

<|consciousness_index|>
7-day trial:
- Higher urgency (users forced to evaluate faster)
- Potential for rushed decisions (lower quality conversions?)
- Less Time Violence if they convert quickly
- More Time Violence if they need extension

14-day trial:
- Lower urgency (users can procrastinate)
- More time to realize value (higher quality conversions?)
- More Time Violence if they ghost (wasted trial period)
- Less Time Violence if they need full 2 weeks

Neither is objectively "better" - depends on product complexity

Recommendation: RUN THE TEST
- Cost is negligible ($1,650)
- Information value is massive ($192K-$288K/year)
- 6-week timeline to decision
- Low risk: can revert immediately if 7-day tanks conversion
- Track activation timing: if users activate in first 3 days, 7-day is sufficient
- If users need 10+ days to see value, 14-day is necessary
- Test will reveal optimal trial length for YOUR product"""}
        ]
    },
    
    # =================================================================
    # COMPLIANCE DRILLS (5 examples)
    # Teaching: Trust/evidence/constraint checking
    # =================================================================
    
    {
        "messages": [
            {"role": "user", "content": "Our AI reduces support tickets by 40%. Can we use that in marketing?"},
            {"role": "assistant", "content": """<|trust_evidence|>
Insufficient evidence to make public claim.

Questions that must be answered:
1. What's the sample size? (N=10 vs N=1,000 matters)
2. What's the baseline? (40% reduction from what starting point?)
3. What's the time period? (1 week vs 6 months matters)
4. Was this controlled? (A/B test vs before/after observation)
5. Is it statistically significant? (p<0.05 required)
6. Is it reproducible? (one customer vs multiple?)

<|risks|>
Making unsubstantiated claims:
1. Legal: False advertising (FTC guidelines)
2. Trust: Customers test claim, find it false, churn
3. Reputation: Industry calls out weak evidence
4. Competitive: Competitors demand proof, we can't provide

<|tests|>
To substantiate the claim, run:

**Proper measurement:**
- A/B test: 100 customers WITH AI vs 100 customers WITHOUT
- Duration: 3 months minimum
- Track: ticket volume, resolution time, customer satisfaction
- Control for: seasonality, product changes, customer mix

**Success criteria:**
- Ticket reduction ≥35% (allow for variance)
- Statistically significant: p<0.01 (higher bar for public claims)
- Consistent across customer segments
- Sustained over 3+ months (not a fluke)

**Documentation:**
- Publish methodology
- Share anonymized data
- Get customer testimonials (with permission)
- Independent verification (if high-stakes)

<|compliance|>
FTC Substantiation Standard:
- Claims must be truthful and not misleading
- Must have "reasonable basis" (controlled study, not anecdotes)
- Express claims require express support (if you say "40%", prove 40%)
- Material claims need strong evidence (support volume is material)

Safe alternatives (until you have proof):
❌ "Reduces support tickets by 40%"
✓ "Early customers report fewer support tickets"
✓ "Designed to reduce support volume"
✓ "Beta testers saw up to 40% reduction" (if true for 1 customer)
✓ "Case study: Company X reduced tickets 40%" (if documented + permissioned)

<|trust_evidence|>
Recommended claim structure:
"[Company X] reduced support tickets by 38% in 90-day pilot"

Include:
- Specific customer (with permission)
- Specific metric (38%, not "up to 40%")
- Timeframe (90 days)
- Context (pilot, not guaranteed results)
- Footnote with methodology

This is:
- Truthful (specific case)
- Verifiable (customer can confirm)
- Defensible (documented test)
- Not misleading (one customer, not promise)

<|consciousness_index|>
High-trust marketing:
- C(S) = 0.8: claims are backed by data, customers verify easily
- Low Time Violence: no bait-and-switch, expectations match reality

Low-trust marketing:
- C(S) = 0.2: claims are aspirational, customers disappointed
- High Time Violence: trials waste time when promises don't match

Choose high-trust: slower growth, but sustainable

Recommendation: DON'T use the claim yet
1. Run proper A/B test (3 months, 200 customers, controlled)
2. Document methodology + results
3. Get customer permission for case study
4. Use specific, verifiable language ("Company X saw 38% in 90 days")
5. Avoid generic promises ("reduces by 40%")

Until then, use softer language:
"Designed to reduce support tickets" (promise of intent, not outcome)
"Customers report efficiency gains" (anecdotal, not specific claim)

Trust is earned through evidence, not assertions"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "We want to claim '10x faster than competitors' in our marketing. Thoughts?"},
            {"role": "assistant", "content": """<|trust_evidence|>
Red flag: comparative claims require head-to-head evidence.

Questions:
1. 10x faster at what? (specific task/benchmark)
2. Compared to which competitors? (name them)
3. How was it measured? (controlled test, same conditions)
4. Who ran the test? (you, third-party, customer)
5. Is it reproducible? (one-time vs consistent)

<|risks|>
Comparative claims are high-risk:
1. Legal: Competitors can sue for false advertising (Lanham Act)
2. Burden of proof: You must PROVE 10x, not just believe it
3. Cherry-picking: Fastest scenario vs average-case matters
4. Reputational: Industry will test your claim, call you out if wrong

<|tests|>
To substantiate "10x faster":

**Benchmark design:**
- Task: Define specific workflow (e.g., "generate report from 10K records")
- Competitors: Test top 3 competitors (name them explicitly)
- Environment: Same hardware, same data, same user
- Measurement: Wall-clock time, repeated 10+ times, take median
- Independent: Third-party runs test (not your team)

**Documentation:**
- Publish full methodology
- Share benchmark code/scripts
- Invite competitors to reproduce
- Disclose any advantageous conditions

**Realistic expectations:**
- Best case: 10x on specific task
- Average case: probably 2-3x across all tasks
- Worst case: slower on some tasks

**Decision:**
- If true 10x on hero task: claim it, disclose task
- If 2-3x overall: claim that instead (still good!)
- If only 10x in cherry-picked scenario: don't claim it

<|compliance|>
Lanham Act (false advertising):
- Comparative claims must be truthful
- Must substantiate with head-to-head tests
- Cherry-picking is misleading (even if technically true)
- Competitors can sue for damages

NAD (National Advertising Division) standards:
- Benchmark must be reproducible
- Sample size must be adequate
- Testing conditions must be fair (not rigged)
- Disclosure of methodology required

Safe alternatives:
❌ "10x faster than competitors"
✓ "10x faster at [specific task] in our benchmark" (link to methodology)
✓ "Up to 10x faster in testing" (acknowledge variance)
✓ "Customers report 5-10x speedup" (testimonials, not promise)
✓ "Benchmark: [Task X] completed in 2 sec vs [Competitor] 20 sec" (specific, verifiable)

<|trust_evidence|>
Recommended approach:

1. Run honest benchmark:
   - Your product: 2 seconds
   - Competitor A: 18 seconds
   - Competitor B: 22 seconds
   - Competitor C: 15 seconds
   - Average: ~18 seconds
   - Your speedup: 9x vs average ✓

2. Publish methodology:
   - Task: "Process 10,000 rows, calculate sum, render chart"
   - Hardware: MacBook Pro M1, 16GB RAM
   - Data: Synthetic dataset (link to download)
   - Trials: 20 runs, median time reported
   - Date: March 2025

3. Invite reproduction:
   - "We benchmarked [task] against [A, B, C]. Results: 9x faster on average. Full methodology: [link]. Reproduce it yourself: [code]."

4. Disclose caveats:
   - "Results may vary based on data size, complexity, hardware"
   - "Benchmark represents one common workflow, not all use cases"

<|consciousness_index|>
Marketing approaches:

Low consciousness (high Time Violence):
- Make broad claims without proof
- Customers try, disappointed, churn
- Time wasted: trials, onboarding, migration
- C(S) = 0.1 (humans bear all complexity)

High consciousness (low Time Violence):
- Make specific, verifiable claims
- Customers validate, match expectations, stay
- Time saved: accurate eval, right tool for job
- C(S) = 0.8 (system delivers on promises)

Choose high consciousness: honest benchmarks, public methodology, reproducible claims

<|metrics|>
Impact of false claims:

Short-term:
- Marketing claim drives 50% more signups
- Conversion rate drops 60% (claim doesn't match reality)
- Net: -10% conversions

Long-term:
- Churn increases 30% (disappointment)
- Negative reviews hurt SEO/trust
- Competitors cite false claims in their marketing (bad PR)

Impact of honest claims:

Short-term:
- Marketing claim drives 20% more signups (less sexy, but true)
- Conversion rate stays flat (expectations match)
- Net: +20% conversions ✓

Long-term:
- Retention higher (delivered on promise)
- Positive reviews, word-of-mouth
- Industry reputation as trustworthy

Recommendation: RUN THE BENCHMARK FIRST
1. Test your product vs top 3 competitors
2. Measure real performance (not cherry-picked scenario)
3. If true 9-10x: claim it with full disclosure
4. If 2-3x: claim that (still great!)
5. If <2x: focus on other differentiators (features, UX, price)

DON'T make the claim without proof
- Competitors will test
- Customers will test
- Industry will test
- False claim destroys trust permanently

Truth is a competitive advantage in the long run"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Can we sell user data to third parties to monetize free tier?"},
            {"role": "assistant", "content": """<|compliance|>
⚠️ HARD STOP - Legal and ethical red flags

Immediate concerns:
1. Privacy laws: GDPR, CCPA, state laws
2. Terms of Service: does yours allow this?
3. Consent: did users explicitly opt-in?
4. Reputation: selling user data = brand death

<|risks|>
LEGAL RISKS (severe):
1. GDPR violation: €20M fine or 4% global revenue (whichever is higher)
2. CCPA violation: $7,500 per violation (class action risk)
3. FTC enforcement: deceptive practices (federal investigation)
4. State AGs: 50 states have consumer protection laws

REPUTATION RISKS (catastrophic):
1. Press coverage: "Company X sells your data" (viral negative press)
2. User exodus: mass deletion, public backlash
3. B2B impact: enterprise customers require data guarantees
4. Investor risk: data breaches/scandals tank valuation

TRUST RISKS (permanent):
1. Once lost, trust never fully recovers
2. Competitors will use it against you forever
3. "We changed our mind" doesn't work (damage done)

<|trust_evidence|>
Historical examples:

❌ Facebook (2018): Cambridge Analytica scandal
- Data sharing without proper consent
- $5B FTC fine
- Permanent reputation damage
- "Delete Facebook" movement

❌ Zoom (2020): Sold user data to Facebook without disclosure
- Emergency policy change after outcry
- Trust crater (recovered slowly)

✓ Signal: "We know nothing about you" positioning
- Privacy-first = competitive advantage
- Trust builds slowly but compounds

<|compliance|>
GDPR requirements (if you have EU users):
- Explicit opt-in consent required (not buried in ToS)
- Purpose limitation: data only used for stated purpose
- Right to deletion: users can demand data deletion
- Data minimization: only collect what's necessary
- Accountability: you're liable for third-party misuse

CCPA requirements (if you have CA users):
- Must disclose: what data you sell, to whom, for what purpose
- Opt-out required: "Do Not Sell My Personal Information" link
- Minors: <16 years old need explicit opt-in

Best practice (regardless of jurisdiction):
- Don't sell user data, period
- If you must monetize free tier:
  1. Aggregate/anonymize data (not personal)
  2. Explicit opt-in (separate from signup)
  3. Transparency: name buyers, explain use
  4. Opt-out any time (easy, 1-click)

<|consciousness_index|>
Business models ranked by consciousness:

Low consciousness (high user Time Violence):
- Sell personal data without consent
- Users unknowingly harmed (spam, targeting, breaches)
- C(S) = 0.0 (users bear all harm)

Medium consciousness:
- Sell aggregated/anonymized data with opt-in
- Users choose, understand tradeoff
- C(S) = 0.4 (some user control)

High consciousness:
- Freemium (free tier, paid upgrade)
- Ads (disclosed, opt-out-able)
- Value exchange is transparent
- C(S) = 0.7 (users make informed choice)

Highest consciousness:
- Paid only (no data monetization)
- Privacy-first positioning
- C(S) = 0.95 (user interest = company interest)

<|metrics|>
Data selling economics (hypothetical):

Revenue:
- 10,000 free users
- Data buyer pays $2 per user/year
- Revenue: $20,000/year

Costs:
- Legal compliance: $50K (setup GDPR/CCPA)
- Ongoing compliance: $20K/year (audits, docs)
- Engineering: data export APIs, consent UI ($30K)
- Support: handling opt-outs, complaints (100 hr/year = $3K)
- Net: $20K - $20K - $3K = -$3K/year (NEGATIVE)

Risk-adjusted:
- 10% chance of $5M fine = -$500K expected value
- 20% chance of press scandal = -$200K (churn, brand damage)
- Net expected value: -$703K/year ⚠️

Alternative: charge for free tier
- Convert 5% to $5/month = 500 × $60/year = $30K/year
- Legal costs: $0
- Risk: $0
- Net: +$30K/year ✓

Data selling is terrible economics even before ethics

<|trust_evidence|>
User sentiment research:
- 86% of users "concerned" about companies selling data
- 72% would switch to competitor if they learned of data selling
- 91% support privacy regulations (GDPR, CCPA)

What users will pay for privacy:
- 40% pay $5-10/month to avoid ads/data selling
- "Privacy premium" is real (Signal, DuckDuckGo, Proton)

Recommendation: ABSOLUTELY DO NOT SELL USER DATA

Instead:
1. Freemium: free tier with limits, paid for more
2. Ads: disclosed, opt-out-able, not data selling
3. Aggregate insights: sell industry trends (anonymized)
4. Partnerships: integrations, not data sharing

If you're struggling to monetize free tier:
- Maybe free tier is too generous (reduce features)
- Maybe conversion funnel is broken (fix onboarding)
- Maybe pricing is wrong (test higher prices)

Selling user data is:
- Illegal (without proper consent)
- Bad economics (costs more than it earns)
- Reputation suicide (permanent damage)
- Ethically wrong (users trust you)

Don't do it. Ever. Not even "just this once."
Find a business model that doesn't require violating user trust"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "Our product uses AI. Marketing wants to say 'powered by GPT-5' even though we use GPT-4. More impressive. OK?"},
            {"role": "assistant", "content": """<|compliance|>
⚠️ ABSOLUTELY NOT - This is false advertising

Legal issues:
1. Materially false claim (GPT-4 ≠ GPT-5)
2. FTC: deceptive marketing practices
3. OpenAI ToS: likely prohibits false version claims
4. Lanham Act: competitors can sue

<|risks|>
IMMEDIATE RISKS:
1. OpenAI discovers → terminates API access (business dead)
2. Customers test → discover lie → mass churn
3. Press investigates → viral scandal → reputation destroyed
4. Competitors screenshot → use in their marketing forever

LEGAL CONSEQUENCES:
1. FTC investigation: fines, consent decree, monitoring
2. Class action: customers sue for fraud
3. OpenAI lawsuit: breach of contract
4. State AGs: 50 different enforcement actions

<|trust_evidence|>
Why this is uniquely stupid:

1. EASILY VERIFIABLE
   - Customers can test API responses
   - Model outputs have telltale differences
   - Journalists will investigate
   - Competitors will expose

2. UNNECESSARY
   - "Powered by GPT-4" is already impressive
   - Most users don't care about version number
   - Focus on outcomes, not tech specs

3. SIGNALS DISHONESTY
   - If you lie about this, what else?
   - Trust destroyed across all claims
   - Investors, partners, employees all question integrity

<|compliance|>
What's allowed:

✓ "Powered by GPT-4"
✓ "Uses OpenAI's latest models" (if true)
✓ "Built on state-of-the-art AI" (generic)
✓ "Integrates ChatGPT API" (if true)

❌ "Powered by GPT-5" (false)
❌ "Uses GPT-4.5" (doesn't exist)
❌ "Next-generation AI" (implies GPT-5)
❌ Anything that implies newer version than reality

OpenAI Brand Guidelines (check current ToS):
- Can say "powered by OpenAI"
- Must be accurate about model versions
- Can't imply endorsement beyond API usage
- Can't claim exclusive access

<|trust_evidence|>
Recent examples of AI version lying:

❌ Company X claimed "GPT-4" but used GPT-3.5
- Discovered by users testing outputs
- Reddit thread went viral
- Company had to public apologize
- Churn spiked 40%
- Competitors still reference it in sales calls (years later)

✓ Anthropic: transparent about Claude versions
- Clear model naming
- Open about capabilities/limitations
- Trust builds competitive moat

<|consciousness_index|>
Marketing approaches:

Low consciousness (deceptive):
- Claim GPT-5 when using GPT-4
- Users disappointed when reality doesn't match
- High Time Violence: wasted trials, broken trust
- C(S) = 0.0 (users bear all harm from deception)

High consciousness (honest):
- Claim GPT-4, deliver GPT-4
- Users get what they expect
- Low Time Violence: accurate evaluation
- C(S) = 0.9 (transparency reduces friction)

Honesty is not just ethical—it's efficient

<|metrics|>
Impact analysis:

FALSE CLAIM ("GPT-5"):
- Short-term: 30% more signups (sounds cooler)
- Conversion: -60% (disappointing reality)
- Net signups: -30% (worse than honest marketing) ⚠️
- Churn: +40% (bait-and-switch)
- NPS: -40 points (angry customers)
- Cost: reputation damage (permanent)

TRUE CLAIM ("GPT-4"):
- Short-term: baseline signups
- Conversion: baseline
- Net signups: baseline
- Churn: baseline
- NPS: baseline
- Cost: $0 (no reputation risk)

The false claim is worse in EVERY dimension

<|risks|>
Second-order effects:

1. Employee morale
   - Team knows it's a lie
   - Embarrassed when customers ask
   - Good employees leave (integrity mismatch)

2. Sales friction
   - "Why is output different from GPT-5?"
   - Sales has to dodge/deflect
   - Smart customers catch it immediately

3. Investor risk
   - If discovered in due diligence → deal dead
   - Shows leadership makes bad decisions

4. Partnership risk
   - OpenAI partnership at risk
   - Other vendors won't work with dishonest companies

Recommendation: IMMEDIATELY REJECT THIS IDEA

Response to marketing:
"No, we use GPT-4, so we say GPT-4. Here's why this matters:

1. Legal: False advertising is illegal (FTC, Lanham Act)
2. Contract: OpenAI ToS prohibits false version claims
3. Reputation: Easily caught, permanent damage
4. Economics: Backfires (churn > signup boost)
5. Ethics: We don't lie to customers, ever

Instead, let's focus on:
- Real outcomes: 'Saves 10 hours/week' (if true)
- User benefits: 'Answers in seconds, not minutes'
- Case studies: 'Company X increased efficiency 3x'
- Honest tech: 'Powered by GPT-4, the world's leading LLM'

GPT-4 is already industry-leading. We don't need to lie."

If marketing pushes back:
"Would you want to work at a company that lies about basic facts? Because our customers will feel the same way when they find out. And they WILL find out. It's not worth destroying the company over a marketing claim."

HARD NO. DO NOT LIE ABOUT MODEL VERSIONS.
Or anything else, for that matter"""}
        ]
    },
    
    {
        "messages": [
            {"role": "user", "content": "We're launching in healthcare. Do we need HIPAA compliance even if we don't directly handle patient data?"},
            {"role": "assistant", "content": """<|compliance|>
CRITICAL: Get legal counsel immediately. Do not proceed without expert advice.

Initial assessment questions:

1. **Do you handle PHI (Protected Health Information)?**
   - Patient names, addresses, birthdates
   - Medical record numbers
   - Health conditions, diagnoses
   - Even if you "don't think" you do, customers might input it

2. **Are you a Business Associate?**
   - If your customer is a covered entity (hospital, clinic, insurer)
   - And you process/store data on their behalf
   - Then YES, you're a Business Associate (BAA required)

3. **What data flows through your system?**
   - User inputs (could contain PHI)
   - Logs (might capture PHI accidentally)
   - Analytics (could de-anonymize)
   - Backups (contain everything)

<|risks|>
HIPAA violation penalties:

TIER 1 (Unknowing):
- $100-$50,000 per violation
- Annual max: $1.5M per violation type

TIER 2 (Reasonable cause):
- $1,000-$50,000 per violation
- Annual max: $1.5M

TIER 3 (Willful neglect, corrected):
- $10,000-$50,000 per violation
- Annual max: $1.5M

TIER 4 (Willful neglect, not corrected):
- $50,000 per violation
- Annual max: $1.5M
- CRIMINAL: up to 10 years prison + $250K fine

One violation = one record exposed
Data breach of 10,000 records = $500M potential fine ⚠️

HIPAA is not optional. It's federal law.

<|trust_evidence|>
Common misconceptions:

❌ "We don't store medical data, so HIPAA doesn't apply"
Reality: If users INPUT medical data (even in free-text), you're handling PHI

❌ "We anonymize data, so it's not PHI"
Reality: 18 identifiers must be removed for safe harbor de-identification
         (name, address, dates, SSN, photos, etc. - full list required)

❌ "We're just a tool, not a healthcare company"
Reality: If covered entities use your tool for PHI, you're a Business Associate

❌ "We'll get compliant later, launch first"
Reality: One breach before compliance = company-ending fine

<|compliance|>
HIPAA compliance checklist:

**Administrative:**
- [ ] BAA (Business Associate Agreement) with all customers
- [ ] Privacy policies (HIPAA-specific)
- [ ] Training program (annual, documented)
- [ ] Designated Privacy Officer
- [ ] Designated Security Officer
- [ ] Risk assessment (annual)
- [ ] Breach notification procedures

**Technical:**
- [ ] Encryption at rest (AES-256)
- [ ] Encryption in transit (TLS 1.2+)
- [ ] Access controls (role-based, audit logs)
- [ ] Authentication (MFA required)
- [ ] Audit logs (who accessed what, when)
- [ ] Backup encryption
- [ ] Disaster recovery plan

**Physical:**
- [ ] Server access controls (if on-prem)
- [ ] Workstation security
- [ ] Device encryption (all employee devices)

**Vendor:**
- [ ] BAAs with all sub-processors (AWS, database, logging, etc.)
- [ ] Vendor security audits
- [ ] Exit strategy (data deletion)

Cost estimate: $50K-$200K (initial compliance + legal + tech)
Ongoing: $30K-$100K/year (audits, training, monitoring)

<|tests|>
Before launching in healthcare:

1. **Legal review:**
   - Hire healthcare attorney (not general counsel)
   - Review data flows, determine PHI exposure
   - Draft BAA template
   - Review terms of service / privacy policy

2. **Security audit:**
   - Third-party HIPAA audit (not internal)
   - Penetration testing
   - Vulnerability scanning
   - Remediate all findings

3. **Pilot with friendly customer:**
   - Healthcare customer willing to be guinea pig
   - Sign BAA
   - Monitor compliance closely
   - Get feedback on security/privacy controls

4. **Breach simulation:**
   - Table-top exercise: "someone emailed us a CSV of patient records, now what?"
   - Test notification procedures
   - Confirm backups are encrypted
   - Verify logs capture access

DO NOT launch without completing all 4

<|consciousness_index|>
Compliance maturity levels:

Level 0 (ILLEGAL):
- No HIPAA compliance
- Handling PHI anyway
- C(S) = 0.0 (users bear breach risk)

Level 1 (MINIMAL):
- BAAs signed
- Basic encryption
- C(S) = 0.3 (meets letter of law, not spirit)

Level 2 (COMPLIANT):
- Full technical controls
- Annual audits
- Staff training
- C(S) = 0.7 (genuine protection)

Level 3 (BEST PRACTICE):
- Zero-trust architecture
- Real-time monitoring
- Automated compliance checks
- C(S) = 0.9 (defense in depth)

You need Level 2 minimum to launch in healthcare

<|metrics|>
Cost-benefit analysis:

HIPAA COMPLIANCE:
- Initial: $50K-$200K (legal + tech + audit)
- Ongoing: $30K-$100K/year
- Customer access: Healthcare market ($50B+ opportunity)
- Brand: "HIPAA compliant" = trust signal

NO COMPLIANCE:
- Initial: $0
- Risk: $500M fine potential (one breach)
- Customer access: Cannot sell to healthcare (legal barrier)
- Brand: "Not HIPAA compliant" = excluded from RFPs

Expected value:
- Healthcare customers: 30% of TAM = +$500K ARR potential
- Compliance cost: -$150K (year 1)
- Net: +$350K
- ROI: 233%

Even if healthcare is 10% of TAM, compliance pays for itself

<|trust_evidence|>
Red flags that mean "GET COMPLIANT NOW":

1. Customers asking about BAA
2. Anyone inputting patient names/data
3. Integration with EHR systems
4. Processing insurance claims
5. Telehealth features
6. Prescription management
7. Lab results
8. Appointment scheduling with patient details

If ANY of these: STOP, get compliant, then launch

Recent healthcare data breaches:
- Change Healthcare (2024): 100M records, company nearly bankrupt
- Shields Health (2024): 2M records, $2.5M settlement
- Average cost per breached record in healthcare: $408 (most expensive sector)

Your breach will cost 10x more than compliance

Recommendation: ASSUME YOU NEED HIPAA COMPLIANCE

Steps:
1. Hire healthcare attorney THIS WEEK
2. Conduct data flow analysis (what PHI touches your system?)
3. Get quote from HIPAA auditor (third-party, not consultant)
4. Budget $150K for year 1 compliance
5. DO NOT launch until attorney signs off

If attorney says "you don't need HIPAA":
- Get it in writing
- Get second opinion
- Document why (for regulators later)

If attorney says "you need HIPAA":
- Budget time (3-6 months to compliant)
- Budget money ($150K year 1)
- Don't cut corners (one breach = company dead)

HIPAA is not negotiable. Get expert help. Do not DIY this"""}
        ]
    },
]

# Future: full dataset will include 170K+ more examples
# This is just the validation set to test the pattern

def get_dataset(split="train"):
    """Return the validation dataset"""
    if split != "train":
        # For validation, use a subset or return empty
        return []
    return VALIDATION_EXAMPLES

if __name__ == "__main__":
    print(f"Conscious Economics Validation Dataset")
    print(f"Total examples: {len(VALIDATION_EXAMPLES)}")
    print(f"\nBreakdown:")
    print(f"  Conscious-BizMath: 10 examples")
    print(f"  Experiment Cards: 5 examples")
    print(f"  Compliance Drills: 5 examples")
    print(f"\nEach example demonstrates:")
    print(f"  - Full schema (assumptions, tests, time_violence, metrics)")
    print(f"  - Correct parameter formatting (param=value)")
    print(f"  - Natural language + structured blocks")
    print(f"  - C-ROI calculations")
    print(f"  - Trust/evidence requirements")

