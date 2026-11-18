---
description: What Decred is, a reading path for newcomers, links to every common task, three safety rules, and the software versions these docs describe.
---

# User docs

These guides are for anyone who holds DCR or wants to: newcomers, stakers, voters, traders and node operators. No programming is needed; pages for command-line users say so.

## Decred in two sentences

Decred is a cryptocurrency run by its holders: people who lock DCR in tickets vote to approve or disapprove each block miners produce, to change the consensus rules, and to authorize every payment from a treasury that receives 10% of each block's new coins to fund the project. Decred's own wallet apps also include mixing for privacy (StakeShuffle) and trading without depositing coins with an exchange (DCRDEX).

## New here? Read in this order

1. [What is Decred?](start/what-is-decred.md): the whole system in plain language.
2. [Miners, voters and the life of a block](start/life-of-a-block.md): why five tickets vote on every block.
3. [Your first Decred wallet](start/first-wallet.md): install a verified wallet, write down your seed, send a test amount.
4. [Back up and restore your wallet](wallets/back-up-and-restore.md): how the seed gets your coins back.
5. [How staking works](staking/index.md): tickets, rewards, lock-up and voting service providers (VSPs).
6. [Privacy and mixing](privacy/index.md): what the chain reveals and what mixing hides.
7. [How Decred is governed](governance/index.md): every decision tickets make.

Returning after some time away? Many older guides and videos describe features that no longer exist. [What changed](reference/whats-changed.md) maps each to its replacement.

## Go straight to a task

<div class="grid cards" markdown>

-   **[Choose a wallet](wallets/index.md)**

    ---

    Match an app to your goal.

-   **[Get DCR](start/get-dcr.md)**

    ---

    Acquire DCR and move it to your own wallet.

-   **[Stake](staking/stake.md)**

    ---

    Buy tickets through a VSP.

-   **[Mix](privacy/mix-your-dcr.md)**

    ---

    Run StakeShuffle and keep mixed coins private.

-   **[Vote](governance/vote.md)**

    ---

    Rule changes, treasury spends and Politeia proposals.

-   **[See the treasury](governance/treasury.md)**

    ---

    How it is funded, approved and audited.

-   **[Trade on DCRDEX](dex/first-trade.md)**

    ---

    A first small trade in Bison Wallet.

-   **[Use Lightning](lightning/use-lightning.md)**

    ---

    Open a channel and pay invoices.

-   **[Run a node](run/full-node.md)**

    ---

    Verify the chain yourself with `dcrd`.

-   **[Recover a wallet](wallets/back-up-and-restore.md)**

    ---

    Restore from your seed.

-   **[Verify a download](security/verify-downloads.md)**

    ---

    Check signature and hash before installing.

</div>

## Three safety rules

!!! danger "Three safety rules before you start"

    1. **Your seed belongs only in the official wallet's restore screen.** Anyone who has it can take every coin, and sent transactions cannot be reversed. Never type it into a website, chat or form, and never store it online.
    2. **Download Decred's own wallets only from decred.org or github.com/decred, then verify.** Fake wallets steal coins. Decrediton, Bison Wallet and the command-line apps are linked from the [wallets page](https://decred.org/wallets/); [verify the download](security/verify-downloads.md) before installing. For a third-party wallet, use only the link on that page.
    3. **Nobody legitimate messages you first.** Treat anyone who contacts you privately with support, an investment or a giveaway as a scammer. Ask for help in public channels.

    More in [Keep your DCR safe](security/index.md).

## Software these docs describe

| Software | Version | Includes |
| --- | --- | --- |
| Decred | 2.1.7 (October 2026) | Decrediton, `dcrd`, `dcrwallet`, `dcrctl`; the command-line bundle also ships `dcrlnd` 0.8.1 for Lightning |
| Bison Wallet | 1.0.6 | The standalone app, published with the [Decred 2.1.7 release](https://github.com/decred/decred-binaries/releases/tag/v2.1.7) on github.com/decred/decred-binaries (the dcrdex Releases page stops at 1.0.5); Decrediton's **DEX** tab uses the same version |

Each how-to states the versions it was checked against in an **Applies to** box.

Running anything older than 2.1.6? Upgrade now: 2.1.6 fixed a critical consensus vulnerability, and its release notes warn that anyone who does not upgrade risks being forked from the network. See [Upgrading and mandatory releases](run/upgrades.md).

Bison Wallet 1.1 is only a release candidate as of November 2026, cannot trade with 1.0.x, and is not covered here.

## Need protocol detail?

The [whitepaper](../whitepaper/index.md) specifies every consensus rule, parameter and algorithm as deployed on mainnet. User pages summarize it and link to the exact section; start with [the system at a glance](../whitepaper/01-intro.md#sec:intro-overview).

## Getting help

[Get help and join the community](reference/index.md) lists the official channels and how to ask safely. For quick lookups, see the [FAQ](reference/faq.md) and [glossary](reference/glossary.md).

## Next steps

- [What is Decred?](start/what-is-decred.md): begin the reading path.
- [Choose a wallet](wallets/index.md): pick the app that fits your goal.
- [Your first Decred wallet](start/first-wallet.md): a verified wallet with a backed-up seed.
- [How staking works](staking/index.md): how tickets earn rewards and give you a vote.

*[VSP]: voting service provider
*[VSPs]: voting service providers
