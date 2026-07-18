# Recipe — Chain White-Space Map

> Which products each branch has NOT yet bought (land-and-expand fuel).
> Status: v1 sketch — requires the chain map (Interview #2) and a sellable-product
> list. **Never reads factory-os core tables; catalog via curated view / Shopify
> products only.**

## Method
1. Product axis: sellable SKUs relevant to the segment (from Shopify products; segment
   relevance per ICP doctrine once confirmed).
2. Account axis: chain branches (chain map).
3. Cell = has the branch bought SKU s in trailing 12mo? (from order line items).
4. Output per chain: matrix + top-N gap opportunities ranked by
   `sister-branch adoption × branch volume`.

## Caveats
- A gap is an *opportunity hypothesis*, not a need — menus differ by branch.
- Requires decoded pricing doctrine before quoting anything (U-003).

## Verification
Spot-check 5 cells per chain against raw orders (N/N reported).
