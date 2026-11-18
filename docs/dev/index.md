---
description: "Where to start as a Decred developer: paths by goal, how the whitepaper relates to dcrd, and the software versions these docs describe."
---

# Developer docs

These pages are for people who build on Decred or work on its software: exchange and service integrators, wallet developers, infrastructure operators, contributors and anyone implementing the protocol. They assume programming experience but no prior knowledge of Decred.

New to Decred? Start with [The Decred software stack](start/software-stack.md); coming from Bitcoin, also read [Decred for Bitcoin developers](start/decred-for-bitcoin-developers.md).

## Pick your path

<div class="grid cards" markdown>

-   **[Integrate an exchange or service](integrate/index.md)**

    ---

    The shared integrator checklist, then guides for exchanges, wallets and DCRDEX.

-   **[Add Decred to a wallet](integrate/wallet-support.md)**

    ---

    Derivation, signing, light-client sync, staking and mixing.

-   **[Use the node and wallet APIs](api/index.md)**

    ---

    dcrd and dcrwallet JSON-RPC, gRPC, vspd, dcrdata and Politeia.

-   **[Build with Go modules](go/index.md)**

    ---

    Pick dcrd modules, then connect, build and sign from Go.

-   **[Run infrastructure](operate/index.md)**

    ---

    Nodes, voting service providers (VSPs), mining, DCRDEX and Lightning.

-   **[Test on a private network](environment/simnet.md)**

    ---

    Local nodes and wallets for tickets, votes, agendas and treasury spends.

-   **[Implement the protocol](protocol/index.md)**

    ---

    Builder guides to transactions, scripts, keys, staking and mixing.

-   **[Look up ports, options and prefixes](reference/index.md)**

    ---

    Ports, data directories, prefixes, coin types and config options.

-   **[Contribute](contributing/index.md)**

    ---

    Conventions, review, testing, consensus changes and paid work.

</div>

## The whitepaper and dcrd

The [Decred whitepaper](../whitepaper/index.md) specifies the protocol as deployed on mainnet, written so that an implementation built from it alone accepts and rejects exactly the same blocks as `dcrd`. Developer pages link to it for consensus rules instead of restating them.

Four of its [conventions](../whitepaper/02-conventions.md#ch:conventions) matter:

- **Consensus rules** sit in numbered boxes naming the `dcrd` file and function that enforce them, all listed in the [index of consensus rules](../whitepaper/B-rule-index.md#ch:rule-index).
- **Policy rules** (relay, mempool, mining) are separate, in [relay policy and mining](../whitepaper/17-policy.md#ch:policy): nodes may differ on them without splitting the network.
- **History boxes** give earlier forms of changed rules. Full nodes validate from genesis, so old rules bind as much as current ones.
- **`dcrd` is the reference:** [where the two disagree, `dcrd` is correct](../whitepaper/02-conventions.md#conv:reference). Each consensus change put to a vote is documented in a Decred Change Proposal (DCP).

[Protocol guides](protocol/index.md) maps common questions to whitepaper chapters.

## Versions these docs describe

| Software | Version | Read code and docs at |
| --- | --- | --- |
| `dcrd`, `dcrwallet`, `dcrctl`, Decrediton | 2.1.7 (October 14, 2026) | tag `release-v2.1.7` of each repository |
| Bison Wallet (`bisonw`, `bwctl`) | 1.0.6 | tag `v1.0.6` of decred/dcrdex |
| `vspd` | 1.5.0 | tag `release-v1.5.0` |
| `dcrlnd` | 0.8.1, as built in the Decred 2.1.7 bundle | tag `v0.8.1` |

- **Default branches are ahead.** `dcrd` and `dcrwallet` `master` report 2.2.0-pre; options and RPCs found there may not exist in 2.1.7. Bison Wallet 1.1 (v1.1.0-rc2) is unreleased, cannot trade with 1.0.x and is not covered.
- **Go module versions are separate.** Decred 2.1.7 builds `decred.org/dcrwallet/v5` v5.1.2, and `dcrd`'s modules have their own major versions (`rpcclient/v8`): see [dcrd Go modules](go/index.md).
- **Run 2.1.6 or later.** 2.1.6 fixed a critical consensus vulnerability; nodes that did not upgrade risk being forked. See [Operating Decred infrastructure](operate/index.md).

## Upstream documentation

Some documentation lives next to the code. These pages summarize it and link to it:

| Topic | Upstream source |
| --- | --- |
| `dcrd` JSON-RPC methods and websocket notifications | [`docs/json_rpc_api.mediawiki`](https://github.com/decred/dcrd/blob/release-v2.1.7/docs/json_rpc_api.mediawiki) in dcrd |
| `dcrwallet` gRPC API | [`rpc/documentation/api.md`](https://github.com/decred/dcrwallet/blob/release-v2.1.7/rpc/documentation/api.md) in dcrwallet |
| `dcrwallet` JSON-RPC | Help text built into the binary: `dcrctl --wallet help` lists the methods, and `dcrctl --wallet help <METHOD>` describes the method you name |
| `vspd` API, deployment and accountability | [`docs/`](https://github.com/decred/vspd/tree/release-v1.5.0/docs) in vspd |
| DCRDEX protocol | [`spec/`](https://github.com/decred/dcrdex/tree/v1.0.6/spec) in dcrdex |
| Consensus changes | [Decred Change Proposals](https://github.com/decred/dcps) |

## Where to ask

- **Bugs and code questions:** search, then open an issue in the project's repository under [github.com/decred](https://github.com/decred).
- **Chat:** the `#dev:decred.org` room on Decred's Matrix server, which you can join in a browser at [chat.decred.org](https://chat.decred.org/) or from any Matrix client. The current channel list is on [decred.org/community](https://decred.org/community/), and [Get help and join the community](../user/reference/index.md) explains how to avoid scammers.
- **Security vulnerabilities:** never post the details publicly. For `dcrd`, `dcrwallet`, Decrediton, `vspd`, `dcrlnd`, dcrwebapi and cspp's `csppsolver`, report privately through the [Decred bug bounty](https://bounty.decred.org/). For other software, including Bison Wallet, open an issue that asks a maintainer for a private channel and gives no details. [Contributing to Decred software](contributing/index.md) covers disclosure.

## Next steps

- [The Decred software stack](start/software-stack.md): what each program does and how they talk to each other.
- [Your first JSON-RPC call](api/first-rpc-call.md): working `dcrd` and `dcrwallet` calls from curl, Python or JavaScript.
- [Integrate DCR into an exchange or service](integrate/exchange.md): deposits and withdrawals done right.
- [Building on DCRDEX](integrate/dcrdex.md): script Bison Wallet with `bwctl`, read the DCRDEX specification and add assets.
- [Networks](environment/index.md): ports, prefixes and rules for mainnet, testnet3, simnet and regnet.
- [Contributing to Decred software](contributing/index.md): your first change to `dcrd` or `dcrwallet`.

*[DCP]: Decred Change Proposal
*[RPC]: remote procedure call
*[VSPs]: voting service providers
