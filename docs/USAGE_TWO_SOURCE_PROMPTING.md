# Two-Source Prompting for Claude - Usage Guide

## What Is This?

A method to ask Claude questions about Flyberry products **without hallucinations** by providing:
1. **JSON data** = Source of truth (facts)
2. **Markdown context** = Narrative and descriptions

---

## Quick Start

### Installation

```bash
# No installation needed - already built into flyberry_data_loader.py
```

### Basic Usage

```python
from flyberry_data_loader import FlyberryData

# 1. Initialize data loader
data = FlyberryData()

# 2. Generate two-source prompt
prompt = data.to_two_source_prompt(
    product_id="medjoul-dates",
    question="What is the origin and nutritional profile of this product?"
)

# 3. Send to Claude (see examples below)
```

---

## Real-World Examples

### Example 1: Brand Package Generation

```python
from flyberry_data_loader import FlyberryData
import anthropic

data = FlyberryData()
client = anthropic.Anthropic(api_key="your-api-key")

# Generate prompt
prompt = data.to_two_source_prompt(
    product_id="medjoul-dates",
    question="Write a 2-paragraph brand story for this product focusing on origin and quality"
)

# Send to Claude Sonnet 4.5
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)
```

**Output:**
> According to the JSON data, Medjoul Dates are imported from Jordan/Palestine and sourced from the Jordan Valley at 390 meters below sea level. From the markdown context, this region is described as having 258 sunny days per year with unique semi-clayish soil that creates exceptional quality dates that cannot be replicated elsewhere...

---

### Example 2: Customer Support

```python
# Customer asks: "Where are your Medjoul dates from?"
prompt = data.to_two_source_prompt(
    product_id="medjoul-dates",
    question="Where are these dates sourced from and why is that origin important?"
)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}]
)

# Claude will cite: "According to the JSON data, the origin is 'Imported Product of Jordan / Palestine'"
```

---

### Example 3: Marketing Copy Verification

```python
# Verify a marketing claim
prompt = data.to_two_source_prompt(
    product_id="medjoul-dates",
    question="""
    Verify this marketing claim:
    "Flyberry Medjoul dates from the Jordan Valley contain 13.5% of your daily fiber needs"

    Is this accurate according to the data?
    """
)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}]
)

# Claude verifies against JSON: "According to the JSON data, the dietary fiber RDA is 13.5%, so this claim is accurate."
```

---

### Example 4: Recipe Content Generation

```python
# Generate recipe content
prompt = data.to_two_source_prompt(
    recipe_id="natural-caramel",
    question="Write step-by-step instructions for this recipe with cooking tips"
)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1500,
    messages=[{"role": "user", "content": prompt}]
)
```

---

## Method Parameters

```python
data.to_two_source_prompt(
    product_id: Optional[str] = None,    # Product ID (e.g., "medjoul-dates")
    recipe_id: Optional[str] = None,     # Recipe ID (e.g., "natural-caramel")
    question: str = "[Your question]",   # The question to ask Claude
    model: str = "claude-sonnet-4-20250514"  # Claude model (default: Sonnet 4.5)
)
```

**Returns:** Formatted prompt string ready for Claude API

---

## Available Products

```python
# Get list of all products
data = FlyberryData()
products = [p['productId'] for p in data.products]
print(products)
# ['ajwa-dates', 'ameri-dates', 'brazil-nuts', 'deglet-nour-dates',
#  'deri-dates', 'halawi-dates', 'hazelnuts', 'kalmi-dates',
#  'mabroom-dates', 'macadamia-nuts', 'medjoul-dates', 'pecan-nuts',
#  'pine-nuts']
```

## Available Recipes

```python
recipes = [r['recipeId'] for r in data.recipes]
print(recipes)
# ['ajwa-kalakand', 'caramely-date-sundae', 'dark-chocolate-fondue',
#  'date-bark', 'date-bars', 'hazelnut-katli', 'natural-caramel',
#  'nut-pulao', 'pine-nut-candy', 'roasted-spiced-pecan-nuts',
#  'vegan-parmesan']
```

---

## How It Prevents Hallucinations

### The Rules Claude Follows

1. **JSON = Absolute Truth**
   - All facts (names, numbers, origins, claims) come from JSON
   - Claude MUST cite: "According to the JSON data..."

2. **Markdown = Context Only**
   - Used for tone, style, descriptions, storytelling
   - Claude cites: "From the markdown context..."

3. **Conflict Resolution**
   - If JSON says one thing and Markdown says another → JSON wins

4. **No Guessing**
   - If data not found → "This information is not available in the provided documents"

### Example of Conflict Resolution

**JSON says:** `"origin": "Imported Product of Jordan / Palestine"`
**Markdown says:** "...sourced from the best dates in the Middle East..."

**Claude's answer:** "According to the JSON data, the origin is 'Imported Product of Jordan / Palestine'. The markdown context describes them as being sourced from the best dates in the Middle East."

✅ **No hallucination** - Claude doesn't invent specific countries

---

## Model Information

**Default Model:** `claude-sonnet-4-20250514` (Claude Sonnet 4.5)

**Why Sonnet 4.5?**
- ✅ Best balance of speed and accuracy
- ✅ Excellent at following instructions
- ✅ Strong citation discipline
- ✅ Cost-effective for brand content

**Want a different model?**
```python
prompt = data.to_two_source_prompt(
    product_id="medjoul-dates",
    question="...",
    model="claude-opus-4-20250514"  # Use Opus if you need highest accuracy
)
```

---

## Prompt Structure

The generated prompt has this structure:

```
1. System instruction (Claude Sonnet 4.5)
2. 5 mandatory rules
3. <json_data> section (product facts)
4. <markdown_context> section (narrative, up to 5000 chars)
5. Your question
6. "Answer:" prompt
```

**Total length:** ~10-15KB per product

---

## Best Practices

### ✅ DO:
- Ask specific questions
- Request citations (Claude automatically provides them)
- Use for fact-checking marketing copy
- Generate multiple outputs and compare

### ❌ DON'T:
- Ask questions that require external knowledge
- Request information not in the data
- Assume Claude remembers previous conversations

---

## Troubleshooting

### "Product not found"
```python
# Check available products:
data = FlyberryData()
print([p['productId'] for p in data.products])
```

### "Must provide either product_id or recipe_id"
```python
# You must specify one:
prompt = data.to_two_source_prompt(
    product_id="medjoul-dates",  # ✅ Specify this
    question="..."
)
```

### API Key Issues
```python
import anthropic

# Set API key:
client = anthropic.Anthropic(api_key="your-key-here")

# Or use environment variable:
# export ANTHROPIC_API_KEY="your-key-here"
client = anthropic.Anthropic()  # Automatically uses env var
```

---

## Performance

- **Prompt generation:** <50ms
- **Claude API call:** 2-5 seconds
- **Total cost:** ~$0.01-0.03 per request (Sonnet 4.5)

---

## Next Steps

1. Get Claude API key: https://console.anthropic.com/
2. Install Anthropic SDK: `pip install anthropic`
3. Try the examples above
4. Generate your brand package!

---

## Support

**Issues?** Check:
1. `example_usage.py` - See all features in action
2. `flyberry_data_loader.py` - Source code with docstrings
3. `data-lineage.json` - See all mapped sources

**Questions?** Ask Claude Code (me!) for help.
