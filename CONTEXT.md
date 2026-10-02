# GT CRM — sales language

The terms of GT's sales CRM, named **GT CRM** in the product (Tom 2026-10-02, D-046; earlier "GT Pulse", which stays the name of past build units and of the D1 visual system), as Tom has decided them. A glossary only: no implementation, no status. Business rules live in `doctrine/`, designs in `docs/superpowers/specs/`.

## Language

**Lead**:
One enquiry or opportunity from a business. Status is `new`, `working`, `won` or `lost`. `won` needs evidence of an order.
_Avoid_: prospect, deal

**Org**:
The business that buys from GT, one Shopify customer, which is one branch. A business with several branches is several orgs under one chain.
_Avoid_: account, company, client

**Branch**:
One buying location of a business, recorded as one Shopify customer.
_Avoid_: site, store

**Chain**:
Branches that buy from GT under one brand, as listed in Tom's chain map. A distributor is a chain whose branches are not GT's accounts.
_Avoid_: group, franchise

**Clean order**:
A Shopify order that is not a test, not cancelled and not a draft. A refunded order is still clean.
_Avoid_: valid order, real order

**Draft**:
An open or invoice-sent Shopify draft order. A completed draft is an order.
_Avoid_: pending order

**Order class**:
One of `completed`, `draft`, `cancelled`, `test`, `refunded`, decided in that order of precedence: draft, test, cancelled, refunded, completed.

**Verified customer**:
A Shopify customer with at least one clean order and a `client_key`, the link to its Green Invoice client.
_Avoid_: B2B customer, existing customer

**Active customer**:
A verified customer with a clean order in the last 12 months. A label, not a condition.
**Dormant customer**:
A verified customer who is not active.

**Link status**:
How far GT trusts the connection between an org and a Shopify customer: `verified`, `review`, `disputed` or `retired`. Nothing derived from Shopify is shown for an org unless its link is `verified`.

**Review queue**:
The managers' list of orgs whose link is `review` or `disputed`. Identity tasks live here, never in Today.

**Contact**:
A named person with a way to reach them at the buying business. A café's own customers are never contacts.
_Avoid_: customer, lead contact

**Verified contact**:
A contact a person confirmed, or whose phone placed an approved order for the org.
**Unverified contact**:
A contact with provenance that nobody has confirmed. Shown in a separate review area.

**Owner**:
The person responsible for a lead or an org. A lead's owner is its assignee; an org without a lead has no owner until Tom assigns one.

**Manager**:
A user with role `planner` or `admin`. **Rep**: a user with role `sales_rep`, who sees only own work.

**Mirror**:
GT's stored copy of Shopify orders. Shopify stays the source; the mirror can be rebuilt from it.

**Reconciliation**:
The automated comparison of the mirror with Shopify. History and money are shown only while it passes.

**Coverage**:
Verified active customers divided by active customers in the Shopify census.

**Source and time**:
Every number, node and line on screen opens where it came from and when it was read.
