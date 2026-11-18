---
description: "The checklist every Decred integration shares (confirmations, stake maturity, addresses, expiry, mandatory upgrades) and where each guide starts."
---

# Integrating Decred

These guides are for teams adding DCR to an exchange, payment service, custodian, wallet or trading tool. Decred looks like Bitcoin from a distance, but a few of its rules change how deposits are credited and coins are spent. The checklist below names them, with links to the details.

## In this section

<div class="grid cards" markdown>

-   **[Integrate DCR into an exchange or service](exchange.md)**

    ---

    Deploy `dcrd` and `dcrwallet`, credit deposits only after disapproval and reorganization risk has passed, send withdrawals and keep up with upgrades.

-   **[Add Decred to a wallet](wallet-support.md)**

    ---

    Derivation, signing, light-client sync, fees, and optional staking and mixing.

-   **[Building on DCRDEX](dcrdex.md)**

    ---

    Script Bison Wallet with `bwctl`, read the protocol specification and add assets.

</div>

## The checklist

- [ ] **Choose the network on purpose.** Standard mainnet payment addresses start with `Ds` (pay-to-pubkey-hash) or `Dc` (pay-to-script-hash), and testnet3 ones with `Ts` or `Tc`. Each network has its own remote procedure call (RPC) ports (`dcrd` 9109 on mainnet, 19109 on testnet3). Rehearse on testnet3 or a private simnet, where timings differ: coinbase maturity there is 16 blocks, not 256. See [Networks](../environment/index.md).
- [ ] **Never credit at one confirmation.** The votes in the next block can **disapprove** the newest block's regular tree, returning its transactions to the mempool, and `dcrd`'s `confirmations` field ignores this. Check bit 0 of the next header's `VoteBits`, roll back on `blockdisconnected`, and require at least 2 confirmations for small amounts and 6 for withdrawable balances. See [Blocks, confirmations and reorganizations](../protocol/blocks-and-confirmations.md) and the whitepaper's [consequences of disapproval](../../whitepaper/10-blocks.md#sec:blocks-approval-consequences).
- [ ] **Treat vote, revocation and treasury spend outputs as immature for 256 blocks.** Like coinbase outputs, they mature 256 blocks (about 21 hours) after their block; ticket change outputs need only 1 block. Activating the `treasury` agenda (Decred Change Proposal DCP-0006) raised this from 1 block for votes and revocations, through the agenda's code rather than the DCP text. `dcrd` rejects an early spend outright. See [Transactions for builders](../protocol/transactions.md) and the whitepaper's [maturity of vote and revocation outputs](../../whitepaper/12-treasury.md#sec:treasury-stake-maturity).
- [ ] **Validate addresses by decoding them** with your network's parameters (`stdaddr.DecodeAddress` in Go, or `validateaddress` on `dcrd` or `dcrwallet`), never by the first letter, and accept only the address types you pay to. See [Keys, addresses and seeds](../protocol/keys-and-addresses.md).
- [ ] **Leave expiry at 0 unless you mean it.** A transaction with a nonzero `Expiry` E can be mined only in a block below height E, and all its outputs then need 256 blocks before they can be spent. See [Transactions for builders](../protocol/transactions.md).
- [ ] **Plan deposit addresses around the gap limit.** By default `dcrwallet`'s `getnewaddress` refuses more than 20 unused addresses in a row (`gaplimit`), because a seed restore stops looking after that many. If you raise `gaplimit`, restore with the same value. See [Integrate DCR into an exchange or service](exchange.md).
- [ ] **Stay in consensus through mandatory releases.** Run 2.1.6 or later (2.1.7 is current): 2.1.6 fixed a critical consensus vulnerability, and a node that skips a mandatory release can end up on an abandoned chain. See [Upgrading and mandatory releases](../../user/run/upgrades.md).

## Choosing an architecture

Most integrations take one of three shapes, differing in where the keys live and whose node you trust.

| Shape | What you run | Keys | Trade-off |
|---|---|---|---|
| Full node and wallet | `dcrd` and `dcrwallet`, called over JSON-RPC or gRPC | Hot, on the wallet server | Full validation and the simplest code, but anyone with the wallet's credentials can spend while it is unlocked |
| Watching-only plus offline signing | Online, a watching-only `dcrwallet` (`--createwatchingonly` or `importxpub`) issues addresses and builds transactions; offline, one with `offline=1` signs them (`signrawtransaction`) | Offline | Keys never touch a networked machine, but every spend needs a manual round trip |
| dcrdata | The dcrdata REST API, public at [dcrdata.decred.org](https://dcrdata.decred.org/) or self-hosted with `dcrd` (`txindex=1`) and PostgreSQL | None | Address history without an indexer of your own, but the public instance sees every address you query |

[Cold storage with an offline wallet](../../user/security/cold-storage.md) walks through the second shape, and [The Decred software stack](../start/software-stack.md) shows how the programs connect.

## Next steps

- [Blocks, confirmations and reorganizations](../protocol/blocks-and-confirmations.md): the confirmation policy and its code.
- [Choosing an API](../api/index.md): connect to `dcrd` and `dcrwallet` over TLS.
- [Set up a private simnet](../environment/simnet.md): rehearse a disapproval and a reorganization.

*[DCP]: Decred Change Proposal
*[RPC]: remote procedure call
