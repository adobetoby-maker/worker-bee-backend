---
name: skill-stripe
description: Stripe MCP integration (REQUESTED) - payment processing, customer management, subscription handling. Manual REST API access until MCP available.
---

# skill-stripe — Stripe Payment Integration

**MCP Status:** ❌ **REQUESTED - Not Yet Available**
**Alternative:** Stripe REST API via HTTP calls
**Escalation:** Use skill-builder.md to create Stripe API integration

---

## What Stripe MCP Would Do (When Available)

**Payment Operations:**
- Create payment intents
- Process charges
- Refund transactions
- List payment history
- Get payment status

**Customer Management:**
- Create/update customers
- List customers
- Get customer payment methods
- Manage customer subscriptions

**Subscription Handling:**
- Create subscriptions
- Update subscription plans
- Cancel subscriptions
- List active subscriptions
- Handle billing cycles

**Reporting:**
- Get revenue reports
- List transactions by date range
- Export financial data
- Check account balance

---

## Current Workaround (Until MCP Available)

**Use Stripe REST API directly:**

```python
import stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Example: List recent charges
charges = stripe.Charge.list(limit=10)

# Example: Get customer
customer = stripe.Customer.retrieve("cus_xxxxx")
```

**Integration approach:**
1. Add stripe package: `pip install stripe`
2. Store API key in .env: `STRIPE_SECRET_KEY=sk_...`
3. Create helper functions in agent/tools/stripe_tool.py
4. Call from runner.py when needed

---

## When To Use Stripe vs Manual

**Use Stripe integration when:**
- Automated payment processing needed
- Subscription management at scale
- Financial reporting automation
- Customer payment tracking
- Webhook handling for payment events

**Do it manually when:**
- Initial Stripe account setup
- Tax configuration
- Payout settings
- Dispute resolution
- Fraud review

**Rule of thumb:** If it's payment automation → use API/MCP. If it's account configuration → use Stripe dashboard.

---

## How To Escalate (Current Pattern)

**Until MCP available:**

```python
# When user asks about Stripe:
if "stripe" in user_content.lower() or "payment" in user_content.lower():
    # Use skill-builder.md to create Stripe API integration
    await self.run_plan({
        "task": "Create Stripe API helper for: " + user_content,
        "approach": "Use Stripe Python SDK"
    })
```

---

## Common Use Cases (Future MCP)

### 1. Check Payment Status

**User Request:** "Did the client's payment go through?"

**Future Action:**
1. Search payments by customer email
2. Get payment intent status
3. Return: succeeded/pending/failed

---

### 2. Create Subscription

**User Request:** "Set up monthly subscription for new client"

**Future Action:**
1. Create customer if not exists
2. Attach payment method
3. Create subscription with plan
4. Return subscription ID

---

### 3. Financial Report

**User Request:** "Total revenue this month?"

**Future Action:**
1. List charges for date range
2. Sum successful payments
3. Subtract refunds
4. Return net revenue

---

## Integration with Worker Bee (Future)

**Payment Pipeline:**
```
User signs up
  ↓
skill-stripe creates customer
  ↓
Collects payment method
  ↓
Creates subscription
  ↓
Stores customer ID in Supabase
  ↓
Webhook notifies on payment success
```

---

## Security & Approval Gates

**Critical Rules:**

1. **Never Log Full API Keys** - Use environment variables only
2. **Test Mode First** - Always test with test API keys
3. **Confirm Before Charge** - Show amount and ask approval
4. **No Automatic Refunds** - Always confirm refund requests
5. **Webhook Verification** - Verify webhook signatures

**Approval Pattern:**

```
Worker Bee: "Ready to charge customer:

Amount: $49.00
Customer: john@example.com
Description: Monthly subscription

This will charge their saved payment method.
Approve? (yes/no)"
```

---

## Pairs With

- **skill-supabase.md** - Store customer/payment data
- **skill-gmail.md** - Send payment confirmations
- **skill-google-calendar.md** - Schedule subscription renewals

---

## The Bottom Line

Stripe MCP is **requested but not yet available**.

Until MCP exists, use Stripe Python SDK directly.
When MCP becomes available, it will enable automated payment processing.

For now: Build Stripe API integration with skill-builder.md when needed.
