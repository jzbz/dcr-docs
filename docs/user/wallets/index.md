---
description: Pick the right Decred wallet for holding, staking, mixing, trading, hardware security or servers, and find every wallet guide in this section.
---

# Choose a wallet

This page matches each goal to a Decred wallet and lists the guides in this section. New to wallets? The tutorial [Your first Decred wallet](../start/first-wallet.md) walks you through one from start to finish.

## A wallet holds keys, not coins

Your DCR is recorded on the Decred blockchain, not inside an app. A wallet holds the private keys that can spend it, all derived from one **seed**: a list of words the wallet shows you when you create it. Whoever has the seed controls the coins. Lose both the seed and the device and the funds are gone for good. See [How a Decred wallet works](how-wallets-work.md).

A **full node** wallet checks every block. A **light wallet (SPV)** fetches block headers, the filters committed in them and only the blocks that concern you. It syncs much faster, but relies on proof of work instead of checking every transaction itself. It [cannot vote](../../whitepaper/19-ecosystem.md#sec:ecosystem-wallets), so its tickets vote through a [voting service provider (VSP)](../staking/vsps.md) or a separate full-node voting wallet you run.

## The quick answer

- **Stake and vote**: Decrediton or Bison Wallet, through a VSP. For [solo voting](../staking/solo-voting.md), the command-line suite with a full node.
- **Mix for privacy**: Decrediton, Bison Wallet or `dcrwallet`, with StakeShuffle, Decred's mixing protocol. See [Privacy and mixing](../privacy/index.md).
- **Trade without handing your coins to an exchange**: Bison Wallet, or the **DEX** section in Decrediton. See [DCRDEX](../dex/index.md).
- **Lightning payments** (fast off-chain payments through payment channels): Decrediton or the command-line suite. See [Lightning on Decred](../lightning/index.md).
- **On a phone**: the Decred release has no mobile app; decred.org lists Cryptopower and the third-party wallets below.
- **Hardware security**: a Trezor or Ledger with Decrediton. A hardware-backed wallet there cannot stake, mix, vote, use Lightning or trade on the DEX, and a Ledger wallet cannot sign messages. See [Use a hardware wallet](hardware-wallets.md).
- **Servers and scripts**: the command-line suite (`dcrd`, `dcrwallet`, `dcrctl`).
- **A large amount held for years**: [cold storage](../security/cold-storage.md) with an offline signing wallet.

## Feature comparison

Decrediton, Bison Wallet and the command-line suite ship in the signed Decred v2.1.7 release and are built on the same wallet engine, `dcrwallet` (Bison Wallet 1.0.6 embeds the dcrwallet 2.1.3 code). Cryptopower comes from an independent team; its column is taken from its README and code.

| | Decrediton 2.1.7 | Bison Wallet 1.0.6 | Command line 2.1.7 | Cryptopower 2.1.1 |
|---|---|---|---|---|
| Platforms | Windows, macOS, Linux | Windows, macOS, Linux, FreeBSD, OpenBSD | Windows, macOS, Linux, FreeBSD, OpenBSD | Android, iOS, Windows, macOS, Linux, FreeBSD |
| Follows the chain as | Light or full node | Light (built-in wallet) or an external `dcrwallet` | Light or full node | Light |
| Staking | Through a VSP | Through a VSP | Through a VSP, or solo voting | Through a VSP |
| Mixing | Yes | Yes (built-in wallet) | Yes | Yes |
| Votes on | Agendas, treasury spends, Politeia proposals | Agendas, treasury spends | Agendas, treasury spends; proposals with `politeiavoter` | Agendas, treasury spends, proposals |
| DCRDEX trading | **DEX** section | Yes, its main purpose | No | Beta |
| Lightning | Yes | No | Yes (`dcrlnd`) | Not listed |
| Hardware wallets | Trezor, Ledger | No | No | Not listed |

Agendas are consensus rule votes, treasury spends (TSPENDs) are payments from the project treasury that tickets approve or reject, and Politeia proposals, such as funding requests, are voted on off chain. See [How Decred is governed](../governance/index.md).

Cryptopower 2.1.1 (August 2025) is built on `dcrwallet` 2.0.6 and its last maintenance proposal was rejected on Politeia, so check its [releases](https://github.com/crypto-power/cryptopower/releases) before relying on it.

### Third-party wallets

These are also listed on [decred.org/wallets](https://decred.org/wallets/). Each row repeats only what the vendor says about DCR (checked November 2026); none documents ticket buying, mixing or voting.

| Wallet | Platforms | DCR support, per the vendor |
|---|---|---|
| [Cake Wallet](https://docs.cakewallet.com/cryptos/decred/) | Mobile, desktop | Light wallet (SPV) |
| [Exodus](https://www.exodus.com/decred/) | — | Not confirmed: the vendor's Decred page could not be read when checked. [Trezor's Decred page](https://trezor.io/coins/wallet/decred) names Exodus as the app for DCR on a Trezor |
| [Coinomi](https://www.coinomi.com/downloads/) | Android, iOS, Windows, Linux | Hold, send, receive and swap; keys stay on the device |
| [Ledger Wallet](https://www.ledger.com/coin/wallet/decred) app (listed as Ledger Live) | Desktop, mobile | Holds DCR on a Ledger device |

## Official and third-party: What you trust

The official wallets are open source, and their release manifests are signed by the Decred release key, which you can [verify](../security/verify-downloads.md). A third-party wallet adds its vendor's code, release schedule and often servers, which can then see your addresses and balances. A vendor can also drop DCR.

Seeds do not always carry across. Decrediton and `dcrwallet` use a 33-word seed, and Bison Wallet uses its own **app seed**. Cake Wallet uses BIP39 for Decred wallets created since v6.4.2 and a 15-word seed for older ones. To switch wallets, create the new one and send your funds to it.

## An exchange balance is not a wallet

On an exchange, the exchange holds the keys. It can freeze withdrawals, be hacked or close, and you cannot stake or vote with that DCR. Withdraw to a wallet whose seed you hold; [Get DCR](../start/get-dcr.md) shows how.

!!! warning "Fake wallets and lookalike sites"
    Scammers publish copies of Decred wallets that steal seeds and coins. Download only from links on decred.org/wallets or the [Decred v2.1.7 release page](https://github.com/decred/decred-binaries/releases/tag/v2.1.7), and verify the file before you run it. No official wallet is a browser extension or a mobile app. Nobody needs your seed: type it only into your own wallet's restore screen. See [Keep your DCR safe](../security/index.md).

## In this section

<div class="grid cards" markdown>

-   **[How a Decred wallet works](how-wallets-work.md)**

    ---

    Seeds, keys, accounts and light versus full node.

-   **[Back up and restore your wallet](back-up-and-restore.md)**

    ---

    What to back up and how to restore from a seed.

-   **[Install and use Decrediton](decrediton.md)**

    ---

    The full-featured desktop wallet, section by section.

-   **[Install and set up Bison Wallet](bison-wallet.md)**

    ---

    A light multi-asset wallet that stakes, mixes and trades.

-   **[Set up the command-line wallet](command-line.md)**

    ---

    `dcrd`, `dcrwallet` and `dcrctl` with config files.

-   **[Use a hardware wallet](hardware-wallets.md)**

    ---

    Trezor and Ledger, and what they cannot do.

-   **[Send and receive DCR](send-and-receive.md)**

    ---

    Addresses, fees, confirmations and signed messages.

-   **[Manage accounts and passphrases](accounts-and-passphrases.md)**

    ---

    Accounts, balances and passphrase changes.

-   **[Use the block explorer](block-explorer.md)**

    ---

    Check payments, tickets and votes on dcrdata.

-   **[Wallet troubleshooting](troubleshooting.md)**

    ---

    Fixes for common wallet problems.

</div>

## Next steps

- [Your first Decred wallet](../start/first-wallet.md): install, back up and test a wallet in about 20 minutes.
- [Verify your download](../security/verify-downloads.md): check that a wallet file is genuine before you run it.
- [How staking works](../staking/index.md): what your wallet does with tickets.

*[SPV]: simplified payment verification
*[VSP]: voting service provider
*[DEX]: decentralized exchange
*[TSPEND]: treasury spend
*[BIP39]: Bitcoin Improvement Proposal 39, a seed-phrase standard
