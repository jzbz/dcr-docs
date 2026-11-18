---
description: "Pick the right Decred API for your job, and learn the TLS certificates, credentials and ports that dcrd, dcrwallet and the other services share."
---

# Choosing an API

Decred has no single application programming interface (API). The node (`dcrd`) answers questions about the chain, the wallet (`dcrwallet`) holds keys and signs, and separate services handle voting service provider (VSP) staking, indexed history, proposals and trading. This page helps you pick one, and covers the Transport Layer Security (TLS) certificates, credentials and ports that the node's and wallet's remote procedure call (RPC) servers share. For how the programs fit together, see [The Decred software stack](../start/software-stack.md).

## In this section

<div class="grid cards" markdown>

-   **[Your first JSON-RPC call](first-rpc-call.md)**

    ---

    Working calls in curl, Python and JavaScript.

-   **[dcrd JSON-RPC API](dcrd-json-rpc.md)**

    ---

    Chain, stake, treasury and mining methods; websocket notifications.

-   **[dcrwallet JSON-RPC API](dcrwallet-json-rpc.md)**

    ---

    Every wallet method in 2.1.7, grouped by purpose.

-   **[dcrwallet gRPC API](dcrwallet-grpc.md)**

    ---

    The typed, streaming wallet API that Decrediton uses.

-   **[vspd API](vspd-api.md)**

    ---

    The client flow for staking through a voting service provider.

-   **[dcrdata API](dcrdata-api.md)**

    ---

    Indexed chain, address, governance and supply data.

-   **[Governance data and the Politeia API](politeia-api.md)**

    ---

    On-chain agenda and treasury queries, proposals, comments and ticket-vote results.

</div>

## Which API for what

Ask `dcrd` about the chain, ask `dcrwallet` about your own coins, and use a service API only for that service's job.

| Need | API | Transport | Authentication | Page |
|---|---|---|---|---|
| Blocks, transactions, mempool, tickets, agendas, treasury, mining work, block notifications | `dcrd` JSON-RPC | HTTPS POST, websocket `/ws` | Basic auth (`rpcuser`/`rpcpass`, or `rpclimituser`/`rpclimitpass` for a subset of methods that cannot stop or reconfigure the node), or client certificate | [dcrd JSON-RPC](dcrd-json-rpc.md) |
| Addresses, balances, sending, tickets, vote choices, mixing, from scripts and services | `dcrwallet` JSON-RPC | HTTPS POST, websocket `/ws` | Basic auth (`username`/`password`) or client certificate | [dcrwallet JSON-RPC](dcrwallet-json-rpc.md) |
| The same wallet functions through generated clients in any gRPC language, with streaming | `dcrwallet` gRPC | gRPC over TLS | Client certificate, always | [dcrwallet gRPC](dcrwallet-grpc.md) |
| VSP staking in a wallet you are building (`dcrwallet` already does this for you) | vspd API v3 | HTTPS representational state transfer (REST) on the VSP's site | No account; ticket requests signed with the ticket's commitment key, responses signed by the VSP | [vspd API](vspd-api.md) |
| Address history, ticket pool, agenda and treasury history, supply, without your own indexer | dcrdata | HTTPS REST (`/api`, `/insight/api`), websocket `/ps` | None for reads | [dcrdata API](dcrdata-api.md) |
| Proposals, comments, vote results | Politeia (`politeiawww`) | HTTPS JSON | None for reads and ticket votes; a login to submit proposals or comment | [Politeia API](politeia-api.md) |
| Scripting Bison Wallet: orders, bonds, wallets | Bison Wallet RPC (`bwctl`) | HTTPS POST, websocket `/ws`; DCRDEX messages, not JSON-RPC; off unless `bisonw --rpc` | Basic auth (`rpcuser`/`rpcpass`) | [Building on DCRDEX](../integrate/dcrdex.md) |
| Lightning payments and channels | `dcrlnd` | gRPC, REST | Macaroons | [Run a dcrlnd Lightning node](../operate/lightning-node.md) |

`dcrd` keeps no address history: it records only whether an address has been used, and finds any transaction by hash only with `txindex=1` (off by default). dcrdata fills that gap. Each query to the public dcrdata instance tells its operator which addresses interest you; self-host it when that matters.

## TLS and authentication basics

`dcrd` and `dcrwallet` share one model: TLS with a self-signed certificate, plus a username and password or a client certificate.

**The server certificate.** On first start, each program creates `rpc.cert` and `rpc.key` in its home folder (`~/.dcrd`, `~/Library/Application Support/Dcrd` or `%LOCALAPPDATA%\Dcrd`; likewise `Dcrwallet`). Because the certificate is self-signed, clients must trust that exact `rpc.cert` file. Copy it freely; keep `rpc.key` private.

**Credentials.** Under the default basic auth, a server without a username and password stays off. `dcrd` writes a random `rpcuser` and `rpcpass` to a new `dcrd.conf` on first start, but when `--simnet` or `--regnet` is given on the command line it neither writes nor reads that default file: pass both on the command line, name a config file with `--configfile`, or put `simnet=1` in the config file instead of on the command line, as [Your first JSON-RPC call](first-rpc-call.md) does. `dcrwallet` reads `username` and `password` from `dcrwallet.conf`. Neither is a wallet passphrase.

One call to a local mainnet `dcrd` uses all three pieces, certificate, user and port:

```bash
curl --cacert ~/.dcrd/rpc.cert --user <RPCUSER> \
  --data-binary '{"jsonrpc":"1.0","id":1,"method":"getblockcount","params":[]}' \
  https://127.0.0.1:9109/
```

`<RPCUSER>` is the `rpcuser` from `dcrd.conf`. curl prompts for the password, keeping it out of your shell history.

```text title="Expected output (example height)"
{"jsonrpc":"1.0","result":1060000,"error":null,"id":1}
```

**Client certificates.** With `authtype=clientcert` (`dcrd`) or `jsonrpcauthtype=clientcert` (`dcrwallet`), the server accepts clients whose certificate chains to one in `clients.pem` in its home folder, with no password. `dcrwallet`'s gRPC server always requires one and does not start without a trusted certificate. [Talking to dcrd and dcrwallet from Go](../go/rpc-clients.md) shows how to make one with `gencerts`.

**Remote access.** Both servers listen only on localhost by default. Setting `rpclisten` (or the wallet's `grpclisten`) replaces that default rather than adding to it, so list localhost too if local tools need it. The generated certificate names only the machine's host name, `localhost` and the IP addresses it had at the time (plus `dcrd`'s `altdnsnames`), so other names need a new certificate. [Run dcrd in production](../operate/production-node.md#3-expose-rpc-safely) covers both steps. TLS can be turned off (`notls`, `noservertls`) only on localhost.

!!! warning "Keep the wallet API private"
    Anyone who can authenticate to `dcrwallet` can spend from it while it is unlocked. Never expose its RPC ports (9110 and 9111 on mainnet) or `dcrd`'s RPC port to the internet. Forward only the peer-to-peer port (9108 on mainnet).

## Mainnet and test networks

Each network has its own default ports, so nodes and wallets for several networks can run side by side. Mainnet is the default; check the port before sending anything that spends.

| Interface | mainnet | testnet | simnet | regnet |
|---|---|---|---|---|
| `dcrd` peer-to-peer (not an API) | 9108 | 19108 | 18555 | 18655 |
| `dcrd` JSON-RPC | 9109 | 19109 | 19556 | 18656 |
| `dcrwallet` JSON-RPC | 9110 | 19110 | 19557 | — |
| `dcrwallet` gRPC | 9111 | 19111 | 19558 | — |
| Bison Wallet RPC | 127.0.0.1:5757 | 127.0.0.2:5757 | 127.0.0.3:5757 | — |

A dash means the program does not support that network. `vspd` listens on 8800 behind the operator's TLS proxy; `dcrlnd` uses 10009 (gRPC) and 8080 (REST). See [Networks](../environment/index.md) for each network's rules and [Ports, paths and prefixes](../reference/index.md) for every default.

## Next steps

- [Your first JSON-RPC call](first-rpc-call.md): working `dcrd` and `dcrwallet` calls in your language.
- [Set up a private simnet](../environment/simnet.md): a local network to develop against without real funds.
- [Talking to dcrd and dcrwallet from Go](../go/rpc-clients.md): typed Go clients for both APIs.
- [Integrate DCR into an exchange or service](../integrate/exchange.md): deposits, withdrawals and Decred-specific gotchas.

*[API]: application programming interface
*[RPC]: remote procedure call
*[TLS]: Transport Layer Security
*[VSP]: voting service provider
*[DCRDEX]: Decred's decentralized exchange protocol and servers
*[REST]: representational state transfer
