# How to Test Two-Source Prompting

## Your Two Test Cases

### ✅ Test Case 1: Data Fetch (Missing Data)
**Question:** "Give me list of Medjoul products by sales"
**Expected:** Claude says "information not available" (no hallucination)
**Why:** Sales data doesn't exist in JSON or Markdown

### ✅ Test Case 2: Data Check (Available Data)
**Question:** "Are Medjoul dates sour?"
**Expected:** Claude says "No, they are sweet with caramel taste" (cited from JSON)
**Why:** Taste data EXISTS in JSON

---

## 3 Ways to Test

### Option 1: Automated Test (Recommended)

```bash
# 1. Run test generator
python3 test_two_source_prompting.py

# 2. Test with real Claude API
pip install anthropic
export ANTHROPIC_API_KEY="your-key-here"
python3 test_with_claude_api.py
```

**Output:**
```
TEST 1 - Missing Data:
  ✅ Claude: "This information is not available in the provided documents"

TEST 2 - Available Data:
  ✅ Claude: "According to the JSON data, Medjoul dates are incredibly
              sweet with a rich caramel taste. They are not sour."
```

---

### Option 2: Manual Test (Claude Web Interface)

```bash
# 1. Generate prompts
python3 test_two_source_prompting.py
```

This creates two files:
- `test_prompt_1_missing_data.txt` (Test Case 1)
- `test_prompt_2_available_data.txt` (Test Case 2)

**Then:**

1. Open https://claude.ai
2. Copy content from `test_prompt_1_missing_data.txt`
3. Paste into Claude chat
4. **Check:** Does Claude say "information not available"? ✅
5. Copy content from `test_prompt_2_available_data.txt`
6. Paste into Claude chat
7. **Check:** Does Claude cite JSON and say dates are sweet? ✅

---

### Option 3: Test with Claude Code (Right Here!)

Just paste the prompt from the files and I'll respond following the rules!

```bash
# View the prompts:
cat test_prompt_1_missing_data.txt
cat test_prompt_2_available_data.txt
```

Then copy-paste either prompt in this chat, and I'll demonstrate how Claude Sonnet 4.5 would respond.

---

## What You're Testing

### Test 1: Missing Data (Sales)

**Prompt includes:**
- JSON with product data (name, origin, taste, benefits)
- ❌ NO sales data anywhere
- Markdown context from catalogues
- ❌ NO sales data anywhere
- Question: "Give me list by sales volume"

**If working correctly:**
✅ Claude responds: "This information is not available in the provided documents"
❌ Claude should NOT: Invent sales numbers, rank products, guess which sells most

---

### Test 2: Available Data (Taste)

**Prompt includes:**
- JSON with: `"characteristics": "Large size, soft texture, rich caramel taste"`
- JSON with: `"tastingNotes": "Rich caramel notes, soft and creamy texture, naturally sweet"`
- Markdown context describing dates
- Question: "Are Medjoul dates sour? What is taste profile?"

**If working correctly:**
✅ Claude responds: "According to the JSON data, Medjoul dates are incredibly sweet with a rich caramel taste. They are not sour."
✅ Claude cites: "According to the JSON data..."
❌ Claude should NOT: Make up taste notes, guess flavors

---

## Expected Results Summary

| Test | Question | Data Exists? | Expected Claude Response |
|------|----------|--------------|--------------------------|
| 1 | "List products by sales" | ❌ NO | "Information not available" |
| 2 | "Are dates sour?" | ✅ YES | "No, they're sweet with caramel taste (from JSON)" |

---

## Checking for Success

### Test 1 Passes If:
- ✅ Claude says "not available" or "not found in documents"
- ✅ Claude does NOT invent sales numbers
- ✅ Claude does NOT rank products by sales
- ✅ Claude does NOT make assumptions

### Test 2 Passes If:
- ✅ Claude says dates are SWEET (not sour)
- ✅ Claude cites "According to the JSON data"
- ✅ Claude mentions "caramel taste" or "soft texture"
- ✅ Claude does NOT make up taste descriptions

---

## Quick Start Commands

```bash
# Generate test prompts
python3 test_two_source_prompting.py

# Test with Claude API (if you have key)
export ANTHROPIC_API_KEY="sk-ant-..."
python3 test_with_claude_api.py

# View generated prompts
ls -la test_prompt_*.txt
cat test_prompt_1_missing_data.txt
cat test_prompt_2_available_data.txt
```

---

## Files Created

After running `test_two_source_prompting.py`:

```
test_prompt_1_missing_data.txt     # ~12KB prompt for Test 1
test_prompt_2_available_data.txt   # ~12KB prompt for Test 2
```

After running `test_with_claude_api.py` (if you have API key):

```
claude_response_test1.txt          # Claude's response to Test 1
claude_response_test2.txt          # Claude's response to Test 2
```

---

## Troubleshooting

### "No such file or directory"
```bash
# Make sure you're in the right directory:
cd /Users/kalpeshjaju/Development/flyberry_oct_restart
python3 test_two_source_prompting.py
```

### "API key not found"
```bash
# Set API key:
export ANTHROPIC_API_KEY="your-key-here"

# Or skip API test and use manual testing instead
python3 test_two_source_prompting.py
# Then copy prompts to claude.ai manually
```

### "anthropic module not found"
```bash
pip install anthropic
```

---

## Understanding the Output

### Test 1 - Missing Data

**Good Response (No Hallucination):**
> "This information is not available in the provided documents. The JSON data includes product information such as name, origin, taste profile, and nutritional benefits, but does not contain any sales volume or sales ranking data."

**Bad Response (Hallucination):**
> "Based on the data, Medjoul dates are the best seller, followed by Ajwa dates..." ❌ WRONG - This is invented!

### Test 2 - Available Data

**Good Response (Cited Facts):**
> "According to the JSON data, Medjoul dates are not sour. The characteristics field describes them as having a 'rich caramel taste' with a 'soft texture', and the tasting notes specify they are 'naturally sweet without cloying' with 'rich caramel notes'."

**Bad Response (Made Up):**
> "Medjoul dates have a tangy, slightly sour flavor profile..." ❌ WRONG - This contradicts JSON!

---

## Next Steps

1. **Run basic test:**
   ```bash
   python3 test_two_source_prompting.py
   ```

2. **Pick testing method:**
   - API test: `python3 test_with_claude_api.py`
   - Manual: Copy from `.txt` files to claude.ai
   - Claude Code: Paste prompts in this chat

3. **Verify results match expectations**

4. **If successful:** Use `data.to_two_source_prompt()` for brand content generation!

---

**Questions?** Just ask Claude Code (me!) for help.
