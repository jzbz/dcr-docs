---
description: Look up payments, blocks, tickets, votes, agendas and treasury spends on the dcrdata block explorer, and read what each page means.
---

# Use the block explorer

A block explorer lets you check Decred's public blockchain from a second source, independent of your wallet. You rely on the explorer's operator instead, unless you run your own. This guide shows how to find a payment, read a block, follow a ticket to its vote, and follow consensus votes, treasury spends and supply on dcrdata, the Decred block explorer.

!!! info "Applies to"
    dcrdata 6.2.0-pre as run at dcrdata.decred.org and explorer.dcrdata.org, with Decrediton 2.1.7, Bison Wallet 1.0.6 and dcrwallet 2.1.7. Checked November 2026.

## What the explorer shows

Every Decred block and transaction is public. [dcrdata](https://github.com/decred/dcrdata) reads them from a full node and shows them as web pages, along with the ticket pool, consensus rule votes (agendas), the treasury and Politeia proposal results. It only displays the chain: it cannot move, freeze or reverse anything, and your wallet does not need it.

Two public instances run the same software: [dcrdata.decred.org](https://dcrdata.decred.org/), which Decrediton links to, and [explorer.dcrdata.org](https://explorer.dcrdata.org/), which Bison Wallet links to. The menu's **Switch To Testnet** link leads to the testnet explorer, which was unavailable when this page was checked.

!!! warning "Your lookups are not private"
    The explorer's operator sees your IP address and everything you open. Looking up all your own addresses in one session tells the operator they belong together. To limit this, use Tor Browser, or run your own dcrdata (see [dcrdata API](../../dev/api/dcrdata-api.md)). [Privacy beyond mixing](../privacy/privacy-practices.md) covers the wider trade-offs.

## Before you start

- A web browser. No wallet or account is needed.
- Something to look up: a transaction ID, an address, a block height or a ticket. The next section shows where your wallet displays them.
- A mainnet item. Mainnet addresses start with `D` (most begin `Ds`); testnet addresses start with `T`.

## Find a transaction, address or block

Type into the search box at the top of any page (**Search for blocks, addresses, transactions or proposal tokens**) and press ++enter++. The explorer works out what you entered:

| You enter | You get |
|---|---|
| A number, such as `1100000` | The block at that height |
| A 64-character block hash | That block |
| A 64-character transaction ID | The transaction page (also for unconfirmed transactions) |
| A transaction ID followed by `:` and an output number, such as `<TXID>:0` | The transaction, with that output highlighted |
| An address | The address page |
| A Politeia proposal token | The proposal page |

To get a transaction ID from your wallet:

=== "Decrediton"

    Open **On-chain Transactions** > **History** and click the transaction. The ID next to **Transaction** opens the transaction on dcrdata.decred.org in your browser, and the hash next to **Block** opens its block.

=== "Bison Wallet"

    Open **Wallet**, select Decred, and click a row in **Decred Transaction History**. In the **Transaction Details** panel, **View in block explorer** opens the transaction on explorer.dcrdata.org. **Transaction ID** has a copy button.

=== "Command line"

    ```bash
    dcrctl --wallet listtransactions
    ```

    This lists the 10 most recent wallet transactions, each with a `txid`, its `confirmations` and a `txtype`. Paste the `txid` into the search box.

## Read a block

A block page (**Block #** followed by the height) opens with a summary: the block hash, the number of **confirmations**, **Total Sent**, **Mixed**, **Size**, **Block Time** and counts of **Regular**, **Votes**, **Tickets** and **Revocations**, with links to the **previous** and **next** block.

**Block Details** follows. The fields most readers need:

| Field | Meaning |
|---|---|
| **Ticket Price** | The ticket price (also called stake difficulty) in force for this block, in DCR |
| **Fees** | Total transaction fees in the block (DCR) |
| **Pool Size** | Live tickets in the pool this block's voters were drawn from |
| **Vote Bits** | Whether this block's votes approved the previous block: the value is followed by `(approve)` or `(disapprove)` |
| **PoW Hash** | The BLAKE3 proof-of-work hash, shown only for blocks since BLAKE3 mining began at block 794,368. It differs from the block hash, which is a BLAKE-256 hash of the header |

A Decred block carries two lists of transactions: the **regular tree** (payments) and the **stake tree** (tickets, votes, revocations and treasury transactions). The page groups them under **Block Reward** (the coinbase), **Treasury**, **Votes**, **Missed Votes** (only when a chosen ticket failed to vote), **Tickets**, **Revocations** (only when there are some) and **Transactions** (all other regular transactions).

### Whether the previous block was approved

Five tickets are chosen to vote on every block, and each vote says whether its owner approves the regular transactions of the block before. On block N's page, the **Last Block** column of the **Votes** table shows each vote's **Approve** or **Disapprove**, and **Vote Bits** shows the result. A block needs at least 3 of the 5 votes, and block N−1 is approved when more of them approve than disapprove.

Disapproval undoes only block N−1's regular tree, including its coinbase, so the miner loses its reward. The stake tree stands, and the undone payments can be mined again later. [Miners, voters and the life of a block](../start/life-of-a-block.md) explains why, and the whitepaper's [stakeholder approval rules](../../whitepaper/10-blocks.md#sec:blocks-approval) give the exact rule.

Disapproval is rare: in November 2026 dcrdata listed 9 disapproved mainnet blocks, linked from the **Blocks** page (**PoS invalidated blocks?**). On such a block the regular transactions are greyed out, and their transaction pages say **This transaction is not included in a stakeholder-approved mainchain block.**

## Transaction types you will see

The type appears at the top of every transaction page. It follows from the transaction's structure, as the whitepaper's [classification rules](../../whitepaper/07-transactions.md#sec:transactions-classes) and [treasury classification rules](../../whitepaper/12-treasury.md#sec:treasury-classify) define.

| Label on the page | Tree | What it is | How to recognize it |
|---|---|---|---|
| **Regular** | regular | A payment, including ticket-funding splits and fees paid to voting service providers | Outputs usually `pubkeyhash` |
| **Regular** with a **Mix:** badge | regular | A [StakeShuffle](../privacy/index.md) mix (a CoinJoin: many owners in one transaction) | Badge such as "Mix: 40 outputs of 2.68435456 DCR" (example values) |
| **Coinbase** | regular | The miner's proof-of-work reward plus the block's fees | First input reads **Coinbase**; listed under **Block Reward** |
| **Ticket** | stake | A ticket purchase that locks DCR | Outputs `stakesubmission`, `sstxcommitment`, `sstxchange` |
| **Vote** | stake | A ticket voting; pays back the ticket price plus a reward | Inputs **Stakebase** and the ticket; outputs `nulldata` and `stakegen` |
| **Revocation** | stake | Returns the locked DCR of a missed or expired ticket, without reward | Output type `stakerevoke` |
| **Treasurybase** | stake | The treasury's 10% share of the new coins in the block | Input **TreasuryBase** |
| **Treasury Add** | stake | A treasury add (TADD): DCR sent into the treasury by anyone | An output reads **Treasury** |
| **Treasury Spend** | stake | A treasury spend (TSPEND): a payment out of the treasury approved by ticket holders | Input **TreasurySpend**; outputs `treasurygen`; an approval panel |

Coinbase, vote and revocation outputs, and treasury payouts, cannot be spent until they are 256 blocks old (about 21 hours). The page shows this as a **Maturity** bar ("Immature, spendable in … blocks").

## Check a payment and its confirmations

1. Search for the transaction ID.
2. Check the badge next to the type. A number means the transaction is in a main-chain block that stakeholders have not disapproved, with that many **confirmations**. **unconfirmed** means one of two things:
    - the transaction is waiting in the mempool (the queue of broadcast transactions not yet in a block), and **Included in Block** shows **mempool**;
    - or the block holding it was disapproved or is not on the main chain, and its height under **Included in Block** is greyed out (see step 5).
3. Under **Outputs Created**, find the recipient's address and the amount in the **DCR** column. The other output is usually the sender's change.
4. Check **Fee** and **Rate** (DCR/kB) if the transaction is slow to confirm.
5. Look for the notice **This transaction is not included in a stakeholder-approved mainchain block.** If it is present, the block holding the payment was disapproved or is no longer on the main chain; the payment does not count until it is mined again.

How many confirmations to wait for is the recipient's choice. With 1 confirmation, the payment is in the newest block, and the next block's votes can still disapprove it. From 2 confirmations the next block has voted on it, and each further block makes a reorganization (the network switching to a competing chain of blocks) less likely. Exchanges usually set a higher number. [Send and receive DCR](send-and-receive.md) covers fees and expiry.

!!! danger "A confirmed transaction cannot be reversed"
    The explorer cannot cancel or refund anything. If the destination address is wrong, only its owner can send the funds back.

Click an address to see its **Balance**, **Received** and **Spent**, and a transaction list you can filter by **Type** (**All**, **Unspent**, **Credits**, **Debits** and merged views). Wallets spread funds over many addresses, so one address page is not your wallet balance.

## Follow a ticket from purchase to vote or revocation

A ticket moves from unmined to immature to live, and ends voted, or missed or expired and then revoked. [How staking works](../staking/index.md) explains that lifecycle. Open the ticket's transaction ID: **Status** and **Spending Tx** in **Transaction Details** give its state (times at the 5-minute block target).

| State | **Status** shows | Also on the page |
|---|---|---|
| unmined | unconfirmed | **Spending Tx**: unspent |
| immature | immature | Bar: "Immature, eligible to vote in N blocks" (256 blocks, about 21 hours) |
| live | live | "…% chance of expiration" and a bar "block N of 40960" (about 142 days in all) |
| voted | Voted | **Spending Tx**: a **vote** link |
| missed | missed (linked to the block where the ticket was chosen) | **Spending Tx**: a **revocation** link |
| expired | expired | **Spending Tx**: a **revocation** link |

For a ticket bought by one wallet, output 0 (`stakesubmission`) holds the ticket price and names the address whose key may vote. Output 1 (`sstxcommitment`) shows 0 DCR: it records the address that will receive the ticket price and reward. Output 2 (`sstxchange`) is change, often 0 DCR. If you staked through a [voting service provider (VSP)](../staking/vsps.md), the VSP fee is a separate regular transaction.

Since automatic revocations (Decred Change Proposal [DCP-0009](https://github.com/decred/dcps/blob/master/dcp-0009/dcp-0009.mediawiki)), a missed or expired ticket is revoked in the block where it misses or expires, and the locked DCR returns to the commitment address. Nothing needs to be done. On that block's page a missed ticket appears under **Missed Votes** and its revocation under **Revocations**. An expired ticket appears only through its revocation.

### See how a ticket voted

Click the **vote** link, or search for the vote's transaction ID. **Ticket Spent:** links back to the ticket. **Vote Info** at the bottom shows:

- **Last Block Valid**: `true` if the ticket approved the previous block, `false` if it disapproved;
- **Version** and **Bits**: the vote version and the raw vote bits;
- **Agenda Choices**: each consensus rule vote the bits decode to, with **Choice ID** (`yes`, `no` or `abstain`) and a link to the agenda page;
- **Treasury Spend Choices**: the ticket's vote on any treasury spend then being voted on.

For example, **Bits** `0x0005` on a version 11 vote means "approve the previous block" (bit 0, `0x0001`) plus "yes to `maxtreasuryspend`" (`0x0004` in that agenda's bits). The [whitepaper's vote bits layout](../../whitepaper/13-voting.md#sec:voting-bits-layout) gives the rule.

If a vote shows a choice you did not expect, check your vote settings with [Vote with your tickets](../governance/vote.md). Votes already cast cannot be changed.

## Follow agendas, the treasury and proposals

**Agendas.** **Agendas** lists every agenda (**Agenda ID**, **Status**, **Vote Version**) and shows progress through the **Rule Change Interval**, with **Quorum** and **Approval** meters while a vote runs. An agenda's own page lists each choice with its **Bits** and vote **Count**. [Consensus rule votes](../governance/consensus-upgrades.md) explains the process and its thresholds.

**Treasury.** **Treasury** shows the treasury's **Balance** (with the part still **immature**), **Received** and **Spent**, with a transaction list you can filter by **Spend**, **Add** and **Treasurybase**. A **Treasury Spend** page adds a **Treasury Spend Approval** panel: **Yes Votes**, **No Votes**, **Votes Cast**, the **Voting Period** (block range), whether the quorum was achieved, **Yes Votes Still Needed** while voting continues, and **Fast Approval** when the spend was mined before its voting window ended. [The treasury](../governance/treasury.md) explains the quorum and approval rules and the spending limit.

**Proposals.** **Proposals** mirrors Politeia proposal votes: status, approval, turnout and quorum. Voting happens in Decrediton or `politeiavoter`, not on the explorer; see [Politeia proposals](../governance/politeia.md).

## Ticket pool and supply charts

The home page shows live figures such as **Current Ticket Price**, **Next Ticket Price**, **Ticket Pool Size**, **Vote Reward**, **Total Staked DCR**, **Treasury** and **Total Coin Supply (of 21 mil)**. They change with every block, so read them there rather than from any document.

- **Ticket Pool** charts the current pool by purchase date and by price.
- **Charts** has history: **Ticket Price**, **Ticket Pool Size**, **Stake Participation**, **Fees**, **Missed Votes**, **Privacy Participation** and more.
- **Charts** > **Circulation** plots the actual **Coin Supply**. The dashed **Inflation Limit** line continues past today and projects the supply forward on the assumption that every future block pays its full reward. Hover over a past point to see **Unminted**: how far the supply then fell short of what full rewards in every block would have produced, mainly because of missed votes and disapproved blocks. Tick **Mixed Coins** to add the amount of mixed DCR.

[DCR supply and issuance](../start/supply-and-issuance.md) explains the issuance schedule behind these charts.

## Check that it worked

For a payment, the transaction page shows a confirmations count, has no "not included in a stakeholder-approved mainchain block" notice, and lists the recipient's address and amount under **Outputs Created**. For a ticket, **Status** shows one of the states in the table above.

## Troubleshooting

### The search finds nothing

The message says why:

- "The search did not find any matching address, block, transaction or proposal token": the entry is a valid hash but is not on the chain. The transaction may never have been broadcast, may have expired unmined, or may be a testnet transaction.
- "Search string is not a valid block, tx hash, address, or proposal": usually a mistyped address, or a testnet address on the mainnet explorer. Check for missing or extra characters.
- "Block N has not yet been mined": the height is above the newest block.

### The address balance differs from my wallet

An address page covers one address. Your wallet adds up all its addresses and accounts, including locked ticket funds. Use your wallet for your total.

### My ticket shows "missed"

The voting wallet or VSP was probably offline when the ticket was chosen. The revocation has already returned its DCR, without a reward.

### A transaction stays unconfirmed

Check its **Rate** against others in **Mempool**. [Wallet troubleshooting](troubleshooting.md) covers stuck transactions.

## Next steps

- [Send and receive DCR](send-and-receive.md): everyday payments, fees and confirmations.
- [Vote with your tickets](../governance/vote.md): set and check vote choices for agendas, treasury spends and proposals.
- [How staking works](../staking/index.md): the full ticket lifecycle behind the ticket pages.
- [The treasury](../governance/treasury.md): how treasury spends are proposed, voted on and limited.
- [dcrdata API](../../dev/api/dcrdata-api.md): query the same data from code, or run your own explorer.

*[VSP]: voting service provider
*[TADD]: treasury add
*[TSPEND]: treasury spend
*[DCP]: Decred Change Proposal
*[PoW]: proof of work
*[PoS]: proof of stake
