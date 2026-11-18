---
description: Short answers to the questions newcomers ask first about Decred, from pronunciation and supply to staking, privacy, wallets and retired features.
---

# Frequently asked questions

Short answers to the general questions people ask first about Decred. Each answer ends with a link to the page that covers the topic properly. For staking details see the [Staking FAQ](../staking/faq.md); for wallet problems see [Wallet troubleshooting](../wallets/troubleshooting.md).

## The basics

### How do you pronounce Decred? Is it Decred or DCR?

The opening line of the Decred Constitution gives the pronunciation as /ˈdi:ˈkred/ or /dɪˈkred/: "dee-cred", with a long *e* as in "decentralized". **Decred** is the name of the project and the network. **DCR** is the currency and its ticker, written in capitals with a space before it: "2.5 DCR". The smallest unit is the *atom*: 1 DCR = 100,000,000 atoms. See [The Decred Constitution](../governance/constitution.md).

### Who created Decred? Is there a company?

Decred grew out of MemCoin2, a 2013 design for a hybrid proof-of-work and proof-of-stake currency by Adam Mackenzie (known online as tacotime).[^origins] It was built by the developers of btcsuite, the project behind the Go Bitcoin full node btcd, through their company Company 0, LLC, and its mainnet launched on 8 February 2016. Today no company owns or controls Decred. The software is open source under the ISC license, and most of the people who work on it are independent contractors, paid from the treasury for work that ticket holders approved. See [A short history of Decred](history.md).

### Is Decred a fork of Bitcoin?

Its code is, its coins are not. `dcrd` descends from btcd, the btcsuite node, so the transaction model and much of the code will look familiar to Bitcoin users. But Decred is a separate blockchain with its own genesis block of 8 February 2016: nobody received DCR for holding bitcoin, and the consensus rules differ in block time, voting, funding and mining. See [What is Decred?](../start/what-is-decred.md) and the whitepaper's [system at a glance](../../whitepaper/01-intro.md#sec:intro-overview), which sets out the roles of miners, stakeholders and nodes.

## Coins and blocks

### How many DCR will there ever be?

About 21 million. Every block creates new DCR (the *block subsidy*), which started at 31.19582664 DCR and is multiplied by 100/101 every 6,144 blocks (about 21.3 days), so it shrinks by slightly less than 1% at each step instead of halving every few years. The schedule caps the total at 21,000,015.55 DCR, and the last new coins are created in block 10,979,328, about 104 years after launch. The real total will stay a little below that ceiling, because missed votes and disapproved blocks leave part of the subsidy uncreated. The current supply changes with every block: read it on the [dcrdata explorer](https://dcrdata.decred.org/) as **Total Coin Supply**. See [DCR supply and issuance](../start/supply-and-issuance.md).

### Is there an airdrop or a giveaway?

No. Decred had one airdrop, at launch: block one paid 1.68 million DCR (8% of 21 million), half to people who had registered for the airdrop and half to the founding developers. No rule can create coins any other way, so there will never be a second airdrop. Treat any "DCR airdrop", giveaway or "send 1 DCR, get 2 back" offer as a scam, and never type your seed into a site that promises one. See [Keep your DCR safe](../security/index.md).

### How fast are blocks, and how many confirmations are enough?

The target is one block every five minutes on mainnet, and the difficulty is adjusted every block to hold the average there. A payment in the newest block is not settled yet: the tickets voting in the next block can still disapprove that block's ordinary transactions and send them back to the waiting pool. Once the next block approves it (Decrediton then shows "1 confirmation"), an everyday payment is settled. For large amounts, wait for several more blocks, since each one makes a chain reorganization less likely. There is no protocol rule for how many is enough, and exchanges set their own number. See [Send and receive DCR](../wallets/send-and-receive.md).

### How is development funded?

By the treasury. Ten percent of every block's subsidy goes to it, and coins leave it only through a *treasury spend* (TSPEND), a transaction that ticket holders approve or reject in an on-chain vote and that must stay within a spending limit set by the consensus rules. What to fund is decided first on [Politeia](https://proposals.decred.org/), where anyone can propose work and tickets vote on it for about one to two weeks. Contractors then bill for approved work, and the payments go out through treasury spends, so stakeholders vote on funding twice. Before May 2021 the treasury's share went to an address held by Decred Holdings Group, which paid contributors by hand. See [The treasury](../governance/treasury.md) and [Politeia proposals](../governance/politeia.md).

## Staking, mining and privacy

### Is Decred private?

Not by default. Like Bitcoin, Decred is a public ledger: amounts, addresses and the trail of every coin are visible to anyone, though no names are recorded. Decred's official wallets include **StakeShuffle**, an opt-in mixing protocol that joins your coins with other wallets' in shared transactions with equal-sized outputs, breaking the link between your old and new coins. Mixing runs peer to peer through Decred's own nodes, with no central server, but it does not make you anonymous: careless spending afterwards, address reuse, your IP address and records an exchange already holds can still identify you. See [Privacy and mixing](../privacy/index.md).

### Can I stake a small amount?

Only if you can afford one whole ticket. To stake you buy a *ticket*, and every ticket costs the current *ticket price* (also called stake difficulty), plus a small transaction fee and, if a voting service provider (VSP) votes it for you, a VSP fee. The network resets the price every 144 blocks (about 12 hours); its consensus floor is 2 DCR, but the real price has long been far above that, so read it live on the **Staking** page of Decrediton or as **Current Ticket Price** on dcrdata. Current wallets cannot split one ticket between several people. Before you buy, remember that a ticket cannot be cancelled: your DCR is locked for about 30 days on average and up to about 144 days. See [How staking works](../staking/index.md) and [Ticket price, rewards and costs](../staking/ticket-price-and-rewards.md).

### Can I mine DCR?

Yes, but mining is a small part of Decred's economy: since 2023 the miner of a block gets 1% of its subsidy plus the transaction fees, while 89% goes to the five tickets that vote on it and 10% to the treasury. Proof of work has used the BLAKE3 hash since block 794,368 (August 2023). `dcrd`'s built-in CPU miner works only on test networks, and `gominer`, the project's graphics-card miner, has no ready-made downloads and must be built from source. For most holders, staking rather than mining is how to earn new DCR. See [Mining Decred](../run/mining.md).

## Wallets and getting DCR

### Which wallet should I use?

**Decrediton**, the desktop wallet, covers staking, mixing, governance voting, Lightning and trading in one app. **Bison Wallet** is a light multi-asset wallet built for trading on DCRDEX that can also stake and mix DCR. The **command-line suite** (`dcrd`, `dcrwallet`, `dcrctl`) suits servers and solo voting. The Decred release bundle has no mobile app, but decred.org lists Cryptopower, a multi-coin light wallet that also runs on Android and iOS, among its core software, alongside a separate group of third-party wallets. Download only from [decred.org/wallets](https://decred.org/wallets/) or the official release page, and [verify the file](../security/verify-downloads.md) before you run it. See [Choose a wallet](../wallets/index.md).

### Where can I get DCR?

If you already hold another cryptocurrency, you can trade it for DCR on DCRDEX, Decred's exchange without custody, where the coins move directly between the two traders' wallets. Otherwise, buy DCR on one of the exchanges listed on [decred.org/exchanges](https://decred.org/exchanges/) and withdraw it to a wallet whose seed you hold: an exchange can freeze or lose coins left with it, and you cannot stake them there. Send a small test withdrawal first, and be wary of anyone in a chat offering to sell you DCR directly. See [Get DCR](../start/get-dcr.md).

## How it works under the hood

### Why does Decred have two transaction trees? What does a disapproved block mean?

Every block holds two lists of transactions: the **regular tree**, with ordinary payments and the miner's reward, and the **stake tree**, with tickets, votes, revocations and treasury transactions. The tickets voting in the next block approve or disapprove the previous block's regular tree, and unless more of the included votes approve than disapprove (so a two-to-two tie disapproves), that block keeps its place in the chain but its regular tree is treated as never mined: its payments go back to the waiting pool and its miner is not paid. The stake tree always stands, so votes keep their rewards and the chain can keep moving. This veto is rare in practice: dcrdata lists nine disapproved blocks on mainnet, all from late 2016. See [Miners, voters and the life of a block](../start/life-of-a-block.md) and the whitepaper's [consequences of disapproval](../../whitepaper/10-blocks.md#sec:blocks-approval-consequences).

### What happened to stakepools, CSPP servers and manual revocations?

All three are retired, so guides that mention them are out of date:

- **Stakepools** gave way to voting service providers (VSPs) running `vspd`, supported from Decred 1.6 (January 2021). A VSP needs no account and is paid in a separate transaction for each ticket, and current wallets have no stakepool settings.
- **The CoinShuffle++ (CSPP) server** that coordinated mixing is gone. Since Decred 2.0 (May 2024), StakeShuffle mixing runs peer to peer and wallets have no mixing-server setting.
- **Manual revocations** ended at block 657,280 (May 2022, Decred Change Proposal DCP-0009). Every block now revokes the tickets that missed or expired in it, and the ticket price comes back without you doing anything.

See [What changed: Coming back to Decred](whats-changed.md).

## Next steps

- [What is Decred?](../start/what-is-decred.md): the whole system in ten minutes, the natural first read for newcomers.
- [Your first Decred wallet](../start/first-wallet.md): install a verified wallet and make a first small transaction.
- [How staking works](../staking/index.md): what a ticket is and what happens to your DCR.
- [Glossary](glossary.md): plain definitions of every term on this page.
- [Get help and join the community](index.md): where to ask a question this page does not answer, safely.

[^origins]: The MemCoin2 paper is dated 2013; the whitepaper's [motivation section](../../whitepaper/01-intro.md#sec:intro-motivation) cites it as one of the designs Decred built on.

*[TSPEND]: treasury spend
*[VSP]: voting service provider
*[CSPP]: CoinShuffle++
*[DCRDEX]: Decred's decentralized exchange protocol and server network
*[DCP]: Decred Change Proposal
*[CPU]: central processing unit
