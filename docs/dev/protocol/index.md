---
description: "How the protocol guides relate to the normative whitepaper, how to read its rules, algorithms and test vectors, and which page answers which question."
---

# Protocol guides

These guides cover the parts of the Decred protocol that wallet, service and integration builders touch. Start with a guide; go to the [Decred technical whitepaper](../../whitepaper/index.md) when you need the exact rule.

## In this section

<div class="grid cards" markdown>

-   **[Transactions for builders](transactions.md)**

    ---

    Transaction types, IDs, fees, expiry, maturity and standardness.

-   **[Scripts for builders](scripts.md)**

    ---

    Standard scripts, stake tags, signature types, multisig, time locks and swaps.

-   **[Blocks, confirmations and reorganizations](blocks-and-confirmations.md)**

    ---

    What a confirmation means when voters can disapprove a block.

-   **[Keys, addresses and seeds](keys-and-addresses.md)**

    ---

    Seeds, hierarchical deterministic (HD) derivation, addresses and signed messages.

-   **[Staking and the treasury for builders](staking-and-treasury.md)**

    ---

    Tickets, votes and revocations, stake difficulty, and treasury spends.

-   **[Mixing for builders](mixing.md)**

    ---

    StakeShuffle through dcrd's `mixing` module and mix-message remote procedure calls (RPCs).

</div>

## Guides versus the specification

**The whitepaper is normative.** It states what makes a block valid and how nodes communicate, precisely enough to implement from. Decred has no specification separate from `dcrd` and the [Decred Change Proposals (DCPs)](https://github.com/decred/dcps), so where the whitepaper and `dcrd` disagree, `dcrd` is correct ([the reference implementation](../../whitepaper/02-conventions.md#conv:reference)). Version 1.0 describes `dcrd` master at commit `46e9df48109a`, which deploys the same consensus agendas as release 2.1.7.

**The guides are practical.** They say what your software must handle, which RPC or Go package helps, and which mistakes cost money. They also cover what the whitepaper [leaves out by design](../../whitepaper/01-intro.md#sec:intro-scope): how `dcrd` is organized and stores the chain, its RPC interface, and `dcrwallet`, whose behavior and defaults the whitepaper does not describe. If a guide contradicts the whitepaper, follow the whitepaper and [report the page](../contributing/docs.md).

Requirements fall into four kinds; the guides name the kind where it matters:

| Kind | Example | If your software differs |
| --- | --- | --- |
| Consensus rule | Coinbase outputs mature after 256 blocks | Its blocks or transactions are rejected |
| Interoperability | Mainnet pay-to-pubkey-hash (P2PKH) addresses start with `Ds` | Payments, peer connections or mixes fail |
| Relay or mining policy | `dcrd`'s default minimum relay fee, 0.0001 DCR/kB | Transactions may not be relayed or mined |
| Wallet default | `dcrwallet`'s address gap limit of 20 | A seed restore may miss payments |

## How the whitepaper is written

The whitepaper uses five devices; read its [conventions chapter](../../whitepaper/02-conventions.md#ch:conventions) first.

Rule boxes
:   Titled like **Rule 8.3 · Null data script**, each states one consensus requirement with MUST or MUST NOT and names the `dcrd` function that enforces it. Chapters whose requirements are only interoperability, such as mixing, have none.

Rule index
:   The [index of consensus rules](../../whitepaper/B-rule-index.md#ch:rule-index) lists all 260 boxes. A block is valid if and only if no rule rejects it, so this is a validator's checklist.

Algorithms
:   Titled like **Algorithm 8.1 · Ticket predicate**: pseudocode to read, not run. Integers are unbounded unless typed, `tdiv` divides truncating toward zero and `tmod` is its remainder, and `reject(reason)` means invalid.

Asides
:   **Note** and **Rationale** are informative. **History** is binding: older blocks still validate under older rules. **Implementation pitfall** marks behavior easy to implement almost correctly.

Test vectors
:   111 collapsed **Test vector:** boxes, produced by running `dcrd` ([test vectors](../../whitepaper/02-conventions.md#conv:vectors)). `dcrd` also ships [script tests](https://github.com/decred/dcrd/tree/release-v2.1.7/txscript/testdata) and [`fullblocktests`](https://github.com/decred/dcrd/tree/release-v2.1.7/blockchain/fullblocktests).

!!! warning "Three conventions that trip up implementations"
    - **No floating point, and division truncates toward zero**: −7 ÷ 2 is −3, where Python's `//` gives −4.
    - **Hashes display byte-reversed.** The mainnet genesis hash displays as `298e5cc3…21d980`; its bytes on the wire begin `80d9212b`.
    - **Agenda activation comes from the chain**, never from a table of heights.

## Which page answers which question

| Topic | Guide | Whitepaper |
| --- | --- | --- |
| Transaction types, IDs, fees and relay | [Transactions](transactions.md) | [Data encoding](../../whitepaper/04-encoding.md#ch:encoding), [Transactions](../../whitepaper/07-transactions.md#ch:transactions), [Relay policy](../../whitepaper/17-policy.md#ch:policy) |
| Multisig, time locks and swaps | [Scripts](scripts.md) | [Script system](../../whitepaper/06-script.md#ch:script), [Opcodes](../../whitepaper/A-opcodes.md#ch:opcodes) |
| When a payment is final | [Blocks and confirmations](blocks-and-confirmations.md) | [Stakeholder approval](../../whitepaper/10-blocks.md#sec:blocks-approval), [Chain selection](../../whitepaper/10-blocks.md#sec:blocks-selection) |
| Keys, addresses and signed messages | [Keys and addresses](keys-and-addresses.md) | [Keys and addresses](../../whitepaper/05-addresses.md#ch:addresses) |
| Tickets, votes and treasury spends | [Staking and the treasury](staking-and-treasury.md) | [Stake system](../../whitepaper/08-staking.md#ch:staking), [Stake difficulty](../../whitepaper/09-difficulty.md#sec:difficulty-stake), [Treasury](../../whitepaper/12-treasury.md#ch:treasury) |
| Joining StakeShuffle mixes | [Mixing](mixing.md) | [StakeShuffle mixing](../../whitepaper/18-mixing.md#ch:mixing) |
| The block subsidy split | [DCR supply and issuance](../../user/start/supply-and-issuance.md) | [Issuance and block subsidy](../../whitepaper/11-subsidy.md#ch:subsidy) |
| Light client filters | [Add Decred to a wallet](../integrate/wallet-support.md) | [Compact filters](../../whitepaper/16-filters.md#ch:filters) |
| Testnet, simnet and regnet | [Networks](../environment/index.md) | [Network parameters](../../whitepaper/14-parameters.md#ch:parameters) |
| Voting in rule changes | [Consensus changes](../contributing/consensus-changes.md) | [Consensus rule changes](../../whitepaper/13-voting.md#ch:voting) |
| Differences from Bitcoin | [Decred for Bitcoin developers](../start/decred-for-bitcoin-developers.md) | [Differences from Bitcoin](../../whitepaper/C-bitcoin-differences.md#ch:bitcoin-differences) |
| The peer-to-peer protocol | None: use the whitepaper | [Peer-to-peer protocol](../../whitepaper/15-p2p.md#ch:p2p) |

## Next steps

- [Transactions for builders](transactions.md): start here to accept or send DCR.
- [Set up a private simnet](../environment/simnet.md): try these rules locally.
- [A tour of the dcrd and dcrwallet code](../contributing/codebase-tour.md): find the functions rule boxes name.

*[RPC]: remote procedure call
*[RPCs]: remote procedure calls
*[HD]: hierarchical deterministic
*[P2PKH]: pay-to-pubkey-hash
*[DCP]: Decred Change Proposal
*[DCPs]: Decred Change Proposals
