#!/usr/bin/env python3
"""
Act 2 Generator - WHERE WE ARE TODAY (Spec-Driven)

Generates Act 2 markdown from:
- Q1 FY26 financial data
- Competitive landscape
- Problems/gaps analysis
- ₹100 Cr blockers

Source: flyberry_oct_restart/extracted_data/
Specs: flyberry_oct_restart/extracted_data/act-2-document-specs/
"""

from datetime import datetime
from generators.act2_data_loader import get_act2_data


def generate_act2_markdown() -> str:
    """
    Generate Act 2: WHERE WE ARE TODAY from structured data

    Returns:
        str: Complete markdown content for Act 2
    """

    # Load all Act 2 data
    data = get_act2_data()
    q1 = data['q1_fy26']
    comp = data['competitive']
    probs = data['problems']
    blockers = data['blockers']

    # Start building markdown
    md = f"""# Act 2: WHERE WE ARE TODAY
**Current State Assessment**

*A brutally honest audit of Flyberry's current position - what's working, what's broken, what's holding us back from ₹100 Cr. No sugar-coating, just facts.*

---

## Quick Navigation

- **[00: Current Reality](#document-00-current-reality)** - Revenue, growth, channels (the numbers)
- **[01: Brand Positioning Gap](#document-01-brand-positioning-gap)** - Mid-market heritage vs premium reality
- **[02: What's Working](#document-02-whats-working)** - Fortune 500 trust, repeat rates, innovation
- **[03: What's Broken](#document-03-whats-broken)** - Packaging, messaging, perception gaps
- **[04: Competitive Reality](#document-04-competitive-reality)** - Where we stand vs Happilo, Farmley, Bateel
- **[05: The ₹100 Cr Blockers](#document-05-the-100-cr-blockers)** - What stops us from 3× growth

---

## DOCUMENT 00: Current Reality
**Read Time**: 6 minutes | **Next**: [01 - Brand Positioning Gap](#document-01-brand-positioning-gap)

**What This Is**: The unvarnished numbers - where we are today, how we got here, what trajectory we're on.

---

### THE NUMBERS (Q1 FY26)

**Revenue Performance**:
| Metric | Q1 FY26 | Q1 FY25 | YoY Growth | Reality Check |
|--------|---------|---------|------------|---------------|
| **Total Revenue** | ₹{q1['total_revenue_cr']} Cr | ₹{q1['prev_q1_revenue']/100} Cr | +{q1['yoy_growth']}% | Good growth, but ₹{q1['run_rate']['annual_runrate']} Cr/year run rate (need ₹100 Cr) |
| **E-Commerce** | ₹{q1['channels']['ecommerce']['revenue']/100} Cr | ₹{q1['channels']['ecommerce']['prev_revenue']/100} Cr | +{q1['channels']['ecommerce']['growth']}% | Explosive, but base was tiny |
| **Sales-in-Store** | ₹{q1['channels']['sis']['revenue']/100} Cr | ₹{q1['channels']['sis']['prev_revenue']/100} Cr | +{q1['channels']['sis']['growth']}% | Steady, mature channel |
| **Corporate Gifting** | ₹{q1['channels']['corporate']['revenue']/100} Cr | ₹{q1['channels']['corporate']['prev_revenue']/100} Cr | {q1['channels']['corporate']['growth']}% | Seasonal (Q3/Q4 Diwali-heavy) |

**What This Means**:
- ✅ **Growth trajectory is strong** ({q1['yoy_growth']}% YoY)
- ⚠️ **But need 3× faster** to hit ₹100 Cr in 3 years
- ✅ **E-commerce is working** ({q1['channels']['ecommerce']['growth']}% growth)
- ⚠️ **Corporate gifting underutilized** (only seasonal, should be year-round)

---

### CHANNEL BREAKDOWN

**E-Commerce ({q1['channels']['ecommerce']['pct_of_total']}% of revenue, fastest growth)**:
- **Swiggy Instamart**: {q1['ecommerce_platforms']['swiggy_instamart']['dates_volume_growth']}% YoY volume growth ({q1['ecommerce_platforms']['swiggy_instamart']['dates_june_24']:,} → {q1['ecommerce_platforms']['swiggy_instamart']['dates_june_25']:,} units)
  - **Reality**: #1 channel by growth, but still small absolute numbers
  - **Opportunity**: {q1['ecommerce_platforms']['swiggy_instamart']['stores']} stores vs competitors' 800+ (room to expand)
- **Amazon**: {q1['ecommerce_platforms']['amazon']['position']}
  - **Reality**: Leadership position, but dates category itself is small
  - **Challenge**: Competing with ₹100-150/kg commodity dates
- **Blinkit**: {q1['ecommerce_platforms']['blinkit']['stores']} stores, growing
- **Zepto**: {q1['ecommerce_platforms']['zepto']['stores']} stores, newer partnership

**Sales-in-Store ({q1['channels']['sis']['pct_of_total']}% of revenue, stable)**:
- Modern Trade: Nature's Basket, Foodhall, Le Marché (premium gourmet chains)
- Traditional Retail: Limited penetration
- **Reality**: Positioned correctly (gourmet, not mass-market), but limited scale

**Corporate Gifting ({q1['channels']['corporate']['pct_of_total']}% of revenue, seasonal)**:
- **Clients**: {q1['corporate_clients']['total']}+ Fortune 500 ({', '.join(q1['corporate_clients']['marquee_names'][:6])}, etc.)
- **Problem**: Only Diwali/New Year spike (Q3/Q4)
- **Missed Opportunity**: No year-round corporate snack programs, wellness boxes, employee rewards

---

### PRODUCT PERFORMANCE

**Winners** (Strong repeat, high growth):
1. **Date Bites**: {q1['product_heroes']['date_bites']['volume']}
   - **Why It Works**: Protein ({q1['product_heroes']['date_bites']['protein']}), clean label, Instagram-worthy
   - **Reality**: Cult hit among urban millennials, but pricing (₹{q1['product_heroes']['date_bites']['price']}/{q1['product_heroes']['date_bites']['size']}) limits mass adoption

2. **Medjoul Dates (Jumbo)**: {q1['product_heroes']['medjoul_jumbo']['repeat_rate']}% repeat rate
   - **Why It Works**: Taste delivers, Fortune 500 validation, gifting hero
   - **Reality**: Premium pricing (₹{q1['product_heroes']['medjoul_jumbo']['price']}/{q1['product_heroes']['medjoul_jumbo']['size']}) is strength AND weakness

3. **Pine Nuts**: ₹{q1['product_heroes']['pine_nuts']['price']}/{q1['product_heroes']['pine_nuts']['size']} (ultra-premium)
   - **Why It Works**: Adventure sourcing story, functional nutrition
   - **Reality**: Tiny volume, but signals brand capability

---

### GROWTH TRAJECTORY

**Current Run Rate**:
- Q1 FY26: ₹{q1['total_revenue_cr']} Cr
- **Annual Run Rate**: ₹{q1['run_rate']['annual_runrate']} Cr (Q1 × 4)
- **Reality**: Strong growth, but need acceleration

**Projection (If Current Trajectory Continues)**:

| Metric | FY26 Projected | FY27 Projected | FY28 Projected | ₹100 Cr Target |
|--------|----------------|----------------|----------------|----------------|
| Revenue | ₹{q1['run_rate']['fy26_projected']} Cr | ₹{q1['run_rate']['fy27_projected']} Cr | ₹{q1['run_rate']['fy28_projected']} Cr | ₹{q1['run_rate']['target_fy28']} Cr |
| Gap | - | - | ₹{q1['run_rate']['gap']} Cr | **{q1['run_rate']['gap_pct']}% short** |

**The Math**: Current trajectory gets us to ₹70 Cr by FY28. Need {blockers['math_100cr']['multiplier']}× acceleration to hit ₹100 Cr target.

---

## DOCUMENT 01: Brand Positioning Gap
**Read Time**: 5 minutes | **Next**: [02 - What's Working](#document-02-whats-working)

**What This Is**: The positioning disconnect - mid-market heritage vs premium reality.

---

### THE GAP

**Current vs Desired**:

| Dimension | Current Reality | Desired Position | Gap |
|-----------|----------------|------------------|-----|
| **Price Tier** | {comp['flyberry_position']['current_tier']} | Ultra-premium (₹3,000-5,000/kg) | Perceived 1 tier below |
| **Competitive Set** | {comp['flyberry_position']['competitive_set']} | vs Bateel, Kimaya | Wrong benchmark |
| **Perception** | {probs['packaging']['evidence']} | Premium quality justified | {probs['packaging']['gap']} |

**Root Cause**: Packaging looks mid-market (₹200/kg visual) despite ₹{probs['packaging']['actual_price']} product inside.

---

## DOCUMENT 02: What's Working
**Read Time**: 6 minutes | **Next**: [03 - What's Broken](#document-03-whats-broken)

**What This Is**: Strengths to build on.

---

### FORTUNE 500 VALIDATION

**{q1['corporate_clients']['total']}+ Corporate Clients**:
- {', '.join(q1['corporate_clients']['marquee_names'])}
- **Sites**: {q1['corporate_clients']['sites']} across {', '.join(q1['corporate_clients']['cities'])}
- **Trust Transfer**: If Goldman Sachs trusts us for client gifting → You can trust us for personal consumption

### PRODUCT HEROES

**Date Bites**: {q1['product_heroes']['date_bites']['volume']} - {q1['product_heroes']['date_bites']['status']}

**Medjoul Dates**: {q1['product_heroes']['medjoul_jumbo']['repeat_rate']}% repeat rate - Fortune 500 validated

### COLD CHAIN INNOVATION

**India's Only End-to-End Cold Chain for Dates**:
- 5-10°C maintained from Jordan Valley to your door
- Result: Always soft dates (never dry/hard)
- Competitive Advantage: Others sell at room temp → dry dates

### E-COMMERCE GROWTH

**+{q1['channels']['ecommerce']['growth']}% YoY** - Explosive quick commerce expansion

---

## DOCUMENT 03: What's Broken
**Read Time**: 6 minutes | **Next**: [04 - Competitive Reality](#document-04-competitive-reality)

**What This Is**: Honest assessment of problems.

---

### PACKAGING PERCEPTION ISSUES

**The Problem**: {probs['packaging']['problem']}

**Evidence**: {probs['packaging']['evidence']}

**Impact**: {probs['packaging']['gap']} value under-perceived

### LOW AWARENESS

**Current**: {probs['awareness']['aided_recall']} aided recall, {probs['awareness']['unaided_recall']} unaided recall

**Problem**: Unknown brand outside niche audience

**Target**: {probs['awareness']['target']}

### MESSAGING CONFUSION

**Problem**: {probs['messaging']['problem']}

**Evidence**: {probs['messaging']['evidence']}

**Confusion**: {probs['messaging']['confusion']}

---

## DOCUMENT 04: Competitive Reality
**Read Time**: 6 minutes | **Next**: [05 - The ₹100 Cr Blockers](#document-05-the-100-cr-blockers)

**What This Is**: Where Flyberry stands in the market.

---

### COMPETITIVE TIER MAP

**Commodity Tier (₹200-600/kg)**:
- Amazon Solimo, Nutraj
- Mass market, value positioning

**Mass-Premium Tier (₹300-900/kg)**:
- **Happilo**: {', '.join(comp['direct_competitors']['happilo']['strengths'])}
- **Farmley**: {', '.join(comp['direct_competitors']['farmley']['strengths'])}
- **Flyberry's Current Perception**: Compared to these (wrong)

**True Premium Tier (₹2,500-4,000/kg)**:
- Kimaya: Curated gourmet
- **Flyberry's Actual Position**: Should be here

**Ultra-Luxury Tier (₹5,000-7,000+/kg)**:
- Bateel: Dubai luxury, international
- **White Space**: Premium with innovation (Flyberry opportunity)

### WHITE SPACE OPPORTUNITY

**{comp['flyberry_position']['white_space']}** - This is where Flyberry belongs.

---

## DOCUMENT 05: The ₹100 Cr Blockers
**Read Time**: 6 minutes

**What This Is**: What stands in the way of 3× growth.

---

### MATH OF ₹100 CR

**Current**: ₹{blockers['math_100cr']['current']} Cr annual run rate

**Target**: ₹{blockers['math_100cr']['target']} Cr by FY28

**Gap**: ₹{blockers['math_100cr']['gap']} Cr

**Multiplier Needed**: {blockers['math_100cr']['multiplier']}× growth

---

### CHANNEL CEILING ANALYSIS

**E-Commerce** (Current: ₹{blockers['channel_ceilings']['ecommerce']['current']} Cr annual):
- Ceiling at current model: ₹{blockers['channel_ceilings']['ecommerce']['ceiling']} Cr
- {blockers['channel_ceilings']['ecommerce']['gap_to_100cr']}

**Retail/SIS** (Current: ₹{blockers['channel_ceilings']['sis_retail']['current']} Cr annual):
- Ceiling: ₹{blockers['channel_ceilings']['sis_retail']['ceiling']} Cr
- {blockers['channel_ceilings']['sis_retail']['gap_to_100cr']}

**Corporate** (Current: ₹{blockers['channel_ceilings']['corporate']['current']} Cr annual):
- Ceiling: ₹{blockers['channel_ceilings']['corporate']['ceiling']} Cr
- {blockers['channel_ceilings']['corporate']['gap_to_100cr']}

**Math**: ₹40 + ₹25 + ₹15 = ₹80 Cr maximum at current model. **₹20 Cr short of ₹100 Cr target.**

---

### WHAT NEEDS TO CHANGE

**Portfolio Expansion**: Missing categories - {', '.join(blockers['portfolio_gaps']['missing_categories'])}
- Opportunity: ₹{blockers['portfolio_gaps']['opportunity']}

**Brand Awareness**: Need {blockers['brand_awareness']['needed']} (vs current {blockers['brand_awareness']['current']})
- Investment: ₹{blockers['brand_awareness']['investment']}

**Operational Scale**: {blockers['operational_constraints']['supply_chain']}, {blockers['operational_constraints']['team']}, {blockers['operational_constraints']['systems']}
- Total Investment: ₹{blockers['operational_constraints']['investment_total']}

---

**Data Sources**: INVESTOR-UPDATE-Q1-FY26.md, COMPETITIVE-LANDSCAPE.md, operational data
**Confidence**: 95% (based on actual Q1 FY26 financials)
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}
"""

    return md


if __name__ == "__main__":
    # Test the generator
    markdown = generate_act2_markdown()
    print(f"✅ Act 2 markdown generated ({len(markdown)} chars)")
    print("   Preview:")
    print(markdown[:500] + "...")
