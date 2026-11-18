---
description: "Default ports, data directories, file names, address and key prefixes, and HD coin types for every Decred program and network, checked against release code."
---

# Ports, paths and prefixes

This is the lookup page for the defaults that every Decred program and network uses: listening ports, data directories, the files inside them, address and key prefixes, and HD (hierarchical deterministic) coin types. Values come from the code at these versions: dcrd, dcrwallet, dcrctl and Decrediton 2.1.7, Bison Wallet 1.0.6, vspd 1.5.0, and dcrlnd v0.8.1 and politeiavoter v1.5.0 as built into the Decred 2.1.7 command-line bundle, plus dcrpool `release-v2.0.0` and dcrdata master. Checked November 2026.

<div class="grid cards" markdown>

-   **[dcrd configuration](dcrd-config.md)**

    ---

    Every `dcrd` option with its default and config-file key, from `config.go` at `release-v2.1.7`.

-   **[dcrwallet configuration](dcrwallet-config.md)**

    ---

    Every `dcrwallet` option, including the `ticketbuyer` and `vsp` namespaces and the mixing options, plus the removed legacy options.

</div>

## Default ports

Every port below is a default that the program's own option can change. Which network a program runs on decides several of them, so the per-network table comes first. [Networks](../environment/index.md) explains how to select a network in each tool, and [The Decred software stack](../start/software-stack.md) shows which program connects to which.

### dcrd and dcrwallet

Sources: `DefaultPort` in dcrd's `chaincfg/*params.go`, `rpcPort` in dcrd's `params.go`, and `internal/netparams/params.go` in dcrwallet.

| Listener | mainnet | testnet3 | simnet | regnet | Default bind |
|---|---|---|---|---|---|
| `dcrd` peer-to-peer (P2P) | 9108 | 19108 | 18555 | 18655 | All interfaces |
| `dcrd` JSON-RPC and websocket | 9109 | 19109 | 19556 | 18656 | localhost |
| `dcrwallet` JSON-RPC and websocket | 9110 | 19110 | 19557 | not supported | localhost |
| `dcrwallet` gRPC | 9111 | 19111 | 19558 | not supported | localhost |

What the table does not show:

- **Testnet ports are the mainnet ports plus 10,000.** Simnet and regnet follow no pattern.
- **dcrd's RPC server is off without credentials.** Under the default `authtype=basic`, dcrd disables RPC unless `rpcuser` and `rpcpass` (or `rpclimituser` and `rpclimitpass`) are set. On its first start on mainnet or testnet, dcrd writes a `dcrd.conf` containing a random `rpcuser` and `rpcpass`. When started with `--simnet` or `--regnet` on the command line, it neither creates nor reads the `dcrd.conf` in its home directory; pass `--configfile` to name a config file, or use flags.
- **dcrd stops listening for peers** when `proxy` or `connect` is set and `listen` is not.
- **dcrwallet connects to dcrd** on `localhost` at the dcrd RPC port of its network (9109, 19109 or 19556) unless `rpcconnect` says otherwise. In light (SPV, simplified payment verification) mode it connects to peers' P2P ports instead.
- **A dcrwallet started by Decrediton does not use 9110 or 9111.** Its gRPC server listens on a random 127.0.0.1 port, and its JSON-RPC server is off unless the wallet's DEX is turned on. The [Decrediton](#decrediton) file table shows where its certificate and log go.
- **dcrctl picks the port from its flags**: 9109 by default, 9110 with `--wallet`, and the testnet or simnet equivalents with `--testnet` or `--simnet`. It has no regnet flag; use `-s 127.0.0.1:18656`.
- **Forward only the P2P port.** dcrd's `docs/default_ports.md` says to open only the P2P port to the internet unless remote RPC access is specifically needed. An RPC port with admin credentials gives full control of the node or wallet.

### Other programs

The ports in this table are the same on every network unless the row says otherwise.

| Program | Port | Purpose | Default bind | Source |
|---|---|---|---|---|
| Bison Wallet (`bisonw`) | 5758 | Web interface | 127.0.0.1 on mainnet, 127.0.0.2 on testnet, 127.0.0.3 on simnet | `client/app/config.go` (v1.0.6) |
| Bison Wallet (`bisonw`) | 5757 | RPC for `bwctl`; off unless `bisonw` runs with `--rpc` | Same hosts as the web interface | `client/app/config.go` |
| DCRDEX server (`dcrdex`) | 7232 | Client connections (websocket over TLS) | 127.0.0.1 | `server/cmd/dcrdex/config.go` (v1.0.6) |
| DCRDEX server (`dcrdex`) | 6542 | Admin API (HTTPS); off unless `dcrdex` runs with `--adminsrvon` | 127.0.0.1 | same |
| DCRDEX server (`dcrdex`) | 7252 | Tor hidden-service listener, only when `hiddenservice` is set; no TLS | Loopback | same |
| `vspd` | 8800 | HTTP API (`/api/v3`) and web pages | All interfaces (`:8800`) | `internal/vspd/config.go` (1.5.0) |
| `dcrpool` | 5550 | Miner (stratum) connections | All interfaces (`0.0.0.0`) | `config.go` (`release-v2.0.0`) |
| `dcrpool` | 8080 | Statistics web interface, HTTPS unless `noguitls` is set | All interfaces (`0.0.0.0`) | same |
| `dcrlnd` | 9735 | Lightning peer connections | All interfaces | `config.go` (v0.8.1) |
| `dcrlnd` | 10009 | gRPC API | localhost | same |
| `dcrlnd` | 8080 | REST API | localhost | same |
| `dcrlnd` | 9911 | Watchtower, only when `watchtower.active` is set | All interfaces | `watchtower/config.go` (v0.8.1) |
| `dcrdata` | 7777 mainnet, 17778 testnet, 17779 simnet | Web explorer, REST, Insight and websocket APIs (plain HTTP) | localhost | `cmd/dcrdata/config.go` (master) |

Outbound connections:

- **`politeiavoter`** connects to dcrwallet's gRPC port: 9111, or 19111 with `--testnet`.
- **Bison Wallet's built-in DCRDEX servers** are `dex.decred.org:7232` on mainnet and `bison.exchange:17232` on testnet (`client/core/core.go`). A server address entered without a port gets 7232. The testnet server did not resolve in November 2026; [Networks](../environment/index.md) records the state of testnet services.
- **`vspd`** connects to `dcrd` and its voting wallets at the ports in the first table (9109 and 9110 on mainnet).

!!! warning "Two programs default to port 8080"
    `dcrpool`'s web interface and `dcrlnd`'s REST API both default to 8080. On a host that runs both, move one with `guilisten` (dcrpool) or `restlisten` (dcrlnd), or turn off the REST API with `norest`.

## Data directories

### Where each program keeps its files

The Go programs all compute their home directory with `AppDataDir` from dcrd's `dcrutil` package (`dcrutil/appdata.go`), which applies one rule to the program's name:

- **Linux, FreeBSD and OpenBSD**: `~/.name`, in lowercase with a leading dot.
- **macOS**: `~/Library/Application Support/Name`, with a capital first letter.
- **Windows**: `%LOCALAPPDATA%\Name`, falling back to `%APPDATA%\Name` when `LOCALAPPDATA` is not set.

Decrediton is an Electron app and sets its own path in `app/main_dev/paths.js`.

| Program | Linux and BSD | macOS | Windows | Change with |
|---|---|---|---|---|
| `dcrd` | `~/.dcrd` | `~/Library/Application Support/Dcrd` | `%LOCALAPPDATA%\Dcrd` | `--appdata` (`-A`) |
| `dcrwallet` | `~/.dcrwallet` | `~/Library/Application Support/Dcrwallet` | `%LOCALAPPDATA%\Dcrwallet` | `--appdata` (`-A`) |
| `dcrctl` | `~/.dcrctl` | `~/Library/Application Support/Dcrctl` | `%LOCALAPPDATA%\Dcrctl` | `--configfile` (`-C`); only the config and client certificate live here |
| Decrediton | `~/.config/decrediton` | `~/Library/Application Support/decrediton` | `%USERPROFILE%\AppData\Local\Decrediton` | No option |
| Bison Wallet (`bisonw` and the desktop app) | `~/.dexc` | `~/Library/Application Support/Dexc` | `%LOCALAPPDATA%\Dexc` | `--appdata` |
| `bwctl` | `~/.dexcctl` | `~/Library/Application Support/Dexcctl` | `%LOCALAPPDATA%\Dexcctl` | `--config` (`-C`) |
| `vspd` | `~/.vspd` | `~/Library/Application Support/Vspd` | `%LOCALAPPDATA%\Vspd` | `--homedir` |
| `dcrlnd`, `dcrlncli` | `~/.dcrlnd` | `~/Library/Application Support/Dcrlnd` | `%LOCALAPPDATA%\Dcrlnd` | `--lnddir` |
| `dcrpool` | `~/.dcrpool` | `~/Library/Application Support/Dcrpool` | `%LOCALAPPDATA%\Dcrpool` | `--appdata` |
| DCRDEX server (`dcrdex`) | `~/.dcrdex` | `~/Library/Application Support/Dcrdex` | `%LOCALAPPDATA%\Dcrdex` | `--appdata` (`-A`) |
| `dcrdata` | `~/.dcrdata` | `~/Library/Application Support/Dcrdata` | `%LOCALAPPDATA%\Dcrdata` | `--appdata` (`-A`) |
| `politeiavoter` | `~/.politeiavoter` | `~/Library/Application Support/Politeiavoter` | `%LOCALAPPDATA%\Politeiavoter` | `--appdata` (`-A`) |

Two programs share directories with others:

- **Decrediton in full-node mode runs `dcrd` with dcrd's own home directory**, so it shares the blockchain, `dcrd.conf` and `rpc.cert` with a standalone `dcrd` on the same account. Decrediton writes the macOS path as `~/Library/Application Support/dcrd`; on the default case-insensitive macOS file system that is the same folder as `Dcrd`. To point Decrediton at another folder, set **Settings** > **Connectivity** > **Adv. Daemon Startup** to **Enabled**. At the next start, turn on **Different Local Daemon Location** and enter the folder in **Daemon Data Directory**.
- **Bison Wallet's folder keeps the app's former name**, `dexc`, and so do its config and log files.

### Network subfolder names

Most programs keep each network's data in its own subfolder. The exceptions are `dcrpool`'s database (`data/dcrpool.kv`) and `politeiavoter`'s `vote/` folder, which all networks share. The programs also do not agree on the name of the test network: a script that looks for `testnet3` in a Bison Wallet folder finds nothing.

| Program | mainnet | testnet | simnet | regnet |
|---|---|---|---|---|
| `dcrd`, `dcrwallet`, `vspd`, `dcrpool`, `dcrdata` | `mainnet` | `testnet3` | `simnet` | `regnet` (`dcrd` only) |
| `politeiavoter` (log folder only) | `mainnet` | `testnet3` | — | — |
| Bison Wallet, DCRDEX server | `mainnet` | `testnet` | `simnet` | — |
| `dcrlnd` | `mainnet` | `testnet` | `simnet` | `regnet` (with `regtest`) |
| Decrediton (`wallets` folder) | `mainnet` | `testnet` | — | — |
| Decrediton (wallet database inside each wallet) | `mainnet` | `testnet3` | — | — |

## Files in each directory

In the tables, `<NET>` is the network subfolder from the table above, and paths are relative to the program's home directory.

### dcrd

Source: `config.go`, `blockdb.go`, `internal/blockchain/utxobackend.go`, `addrmgr/addrmanager.go` and `server.go` at `release-v2.1.7`.

| Path | What it is | Change with |
|---|---|---|
| `dcrd.conf` | Configuration file; created on first start on mainnet or testnet | `--configfile` |
| `rpc.cert`, `rpc.key` | Self-signed TLS certificate and key of the RPC server, generated when missing. Clients need `rpc.cert` | `--rpccert`, `--rpckey` |
| `clients.pem` | Certificate authorities trusted for client certificates; read only with `authtype=clientcert` | `--clientcafile` |
| `data/<NET>/blocks_ffldb/` | Block database | `--datadir` (the network subfolder is appended) |
| `data/<NET>/utxodb/` | Unspent transaction output (UTXO) set | `--datadir` |
| `data/<NET>/feesdb` | Fee estimator database | `--datadir` |
| `data/<NET>/peers.json` | Peer address book | `--datadir` |
| `logs/<NET>/dcrd.log` | Log, rotated at 10 MiB by default | `--logdir`, `--logsize`, `--nofilelogging` |

On regnet, dcrd deletes both the block database and the UTXO database at every start.

### dcrwallet

Source: `config.go`, `walletsetup.go`, `rpcserver.go` and `dcrwallet.go` at `release-v2.1.7`.

| Path | What it is | Change with |
|---|---|---|
| `dcrwallet.conf` | Configuration file; never created automatically | `--configfile` |
| `rpc.cert`, `rpc.key` | TLS certificate and key, shared by the JSON-RPC and gRPC servers, generated when missing | `--rpccert`, `--rpckey` |
| `clients.pem` | Certificate authorities trusted for client certificates | `--clientcafile` |
| `dcrd.cert` | Optional copy of dcrd's `rpc.cert`. If it is missing and dcrd is on localhost, dcrwallet uses `rpc.cert` from dcrd's default home directory | `--cafile` |
| `dcrd-client.cert`, `dcrd-client.key` | Client certificate presented to dcrd when `dcrdauthtype=clientcert` | `--dcrdclientcert`, `--dcrdclientkey` |
| `<NET>/wallet.db` | Wallet database: keys, addresses, transactions and tickets | `--appdata` |
| `<NET>/peers.json` | Peer address book used in light (SPV) mode | `--appdata` |
| `logs/<NET>/dcrwallet.log` | Log, rotated at 10 MiB by default | `--logdir`, `--logsize`, `--nofilelogging` |

### dcrctl

Source: `config.go` at `release-v2.1.7`.

| Path | What it is | Change with |
|---|---|---|
| `dcrctl.conf` | Configuration file. When it is missing, dcrctl creates it with the `rpcuser` and `rpcpass` from dcrd's default `dcrd.conf`, if that file exists and contains both | `--configfile` |
| `client.pem`, `client-key.pem` | Client certificate and key for `authtype=clientcert` | `--clientcert`, `--clientkey` |

dcrctl verifies the server with dcrd's `rpc.cert` from dcrd's default home directory. With `--wallet` it switches to `rpc.cert` from dcrwallet's home directory, but only when `rpccert` has not been set; a `rpccert` line in `dcrctl.conf` applies to both servers.

### Decrediton

Source: `app/main_dev/paths.js`, `app/main_dev/launch.js`, `app/main_dev/logging.js` and `app/config.js` in Decrediton 2.1.7.

| Path | What it is |
|---|---|
| `config.json` | Application settings |
| `decrediton.log` | Decrediton's own log |
| `politeia/` | Cached lists of the tickets eligible to vote on each Politeia proposal |
| `wallets/<NET>/<WALLET>/` | One folder per wallet, named after the wallet |
| `wallets/<NET>/<WALLET>/config.json` | That wallet's settings |
| `wallets/<NET>/<WALLET>/dcrwallet.conf` | dcrwallet configuration written by Decrediton: `appdata` is the wallet folder, gRPC listens on a random loopback port, and JSON-RPC is off unless the wallet's DEX is turned on |
| `wallets/<NET>/<WALLET>/rpc.cert` | dcrwallet's TLS certificate, regenerated at each start; the key is never written to disk |
| `wallets/<NET>/<WALLET>/logs/mainnet/dcrwallet.log` | dcrwallet's log (`logs/testnet3/dcrwallet.log` on testnet) |
| `wallets/<NET>/<WALLET>/mainnet/wallet.db` | Wallet database (`testnet3/wallet.db` on testnet) |
| `wallets/<NET>/<WALLET>/politeia/` | Proposal votes cast from this wallet |
| `wallets/<NET>/<WALLET>/dcrlnd/` | This wallet's Lightning node: `dcrlnd.conf`, `tls.cert`, `admin.macaroon`, `data/`, `logs/` |
| `wallets/<NET>/<WALLET>/dexc/` | This wallet's DEX client: `dex.db` and `logs/dexc.log` |

### Bison Wallet

Source: `client/app/config.go`, `client/core/core.go` and `client/db/bolt/db.go` at v1.0.6.

| Path | What it is | Change with |
|---|---|---|
| `dexc.conf` | Configuration file (optional) | `--config` |
| `rpc.cert`, `rpc.key` | TLS certificate and key of the RPC server used by `bwctl` | `--rpccert`, `--rpckey` |
| `web.cert`, `web.key` | TLS certificate and key of the web interface, used with `--webtls` or a publicly routable `webaddr` | — |
| `<NET>/dexc.db` | Application database | `--db` |
| `<NET>/backup/dexc.db` | Copy of the database written at shutdown | `--no-db-backup` turns it off |
| `<NET>/logs/dexc.log` | Log | `--logpath` |
| `<NET>/assetdb/<ASSET>/` | Built-in wallets, one folder per asset; the Decred wallet is in `assetdb/dcr/` | — |
| `<NET>/mm_cfg.json`, `<NET>/eventlog.db` | Market-making bot settings and event log | — |

`bwctl` reads `rpc.cert` from its own folder and, when none is there, from Bison Wallet's folder.

### Service programs

| Program | Configuration | Data | Log | Other files |
|---|---|---|---|---|
| `vspd` 1.5.0 | `vspd.conf` | `data/<NET>/vspd.db` | `logs/<NET>/vspd.log` | — |
| `dcrlnd` v0.8.1 | `dcrlnd.conf` | `data/chain/decred/<NET>/`: `admin.macaroon`, `readonly.macaroon`, `invoice.macaroon`, `channel.backup` | `logs/decred/<NET>/lnd.log` | `tls.cert`, `tls.key` |
| `dcrpool` `release-v2.0.0` | `dcrpool.conf` | `data/dcrpool.kv` (or PostgreSQL) | `log/<NET>/dcrpool.log` | `dcrpool.cert`, `dcrpool.key` (web interface TLS); `wallet.cert`, `wallet.key` (client certificate for dcrwallet gRPC) |
| DCRDEX server | `dcrdex.conf`, `markets.json` | `data/<NET>/`, plus the PostgreSQL database `dcrdex_<NET>` | `logs/<NET>/dcrdex.log` | `sigkey` (the server's signing key), `rpc.cert`, `rpc.key` |
| `dcrdata` (master) | `dcrdata.conf` | `data/<NET>/`, plus PostgreSQL | `logs/<NET>/dcrdata.log` | — |
| `politeiavoter` v1.5.0 | `politeiavoter.conf` | `vote/` | `logs/<NET>/politeiavoter.log` | `client.pem`, `client-key.pem` (client certificate for dcrwallet gRPC) |

Two defaults surprise operators: `vspd` starts on testnet unless `network=mainnet` is set, and `dcrpool` starts on simnet unless `activenet` is set. [Run a voting service provider](../operate/vsp.md) and [Mining infrastructure](../operate/mining.md) cover both.

## Address and key prefixes

Every encoded address and key starts with a fixed prefix that names its network and type, so a string for one network fails to decode on another. Source: the `NetworkAddressPrefix`, `*AddrID`, `PrivateKeyID`, `HDPrivateKeyID` and `HDPublicKeyID` fields in dcrd's `chaincfg/*params.go`. Each cell gives the leading characters and the prefix bytes in hexadecimal, in serialization order. The whitepaper's [network prefixes](../../whitepaper/05-addresses.md#sec:addresses-prefixes) section is the normative table, and its [overview](../../whitepaper/05-addresses.md#sec:addresses-overview) gives the lengths.

| Object | mainnet | testnet3 | simnet | regnet | Length (characters) |
|---|---|---|---|---|---|
| First character of every address | `D` | `T` | `S` | `R` | — |
| Pay-to-pubkey-hash (P2PKH), secp256k1 ECDSA: the normal wallet address | `Ds` `073f` | `Ts` `0f21` | `Ss` `0e91` | `Rs` `0e00` | 35 |
| P2PKH, Ed25519 | `De` `071f` | `Te` `0f01` | `Se` `0e71` | `Re` `0de0` | 35 |
| P2PKH, secp256k1 Schnorr | `DS` `0701` | `TS` `0ee3` | `SS` `0e53` | `RS` `0dc2` | 35 |
| Pay-to-script-hash (P2SH) | `Dc` `071a` | `Tc` `0efc` | `Sc` `0e6c` | `Rc` `0ddb` | 35 |
| Pay-to-pubkey (P2PK), all signature types | `Dk` `1386` | `Tk` `28f7` | `Sk` `276f` | `Rk` `25e5` | 53 |
| WIF (wallet import format) private key | `Pm` `22de` | `Pt` `230e` | `Ps` `2307` | `Pr` `22fe` | 53 |
| Extended private key | `dprv` `02fda4e8` | `tprv` `04358397` | `sprv` `0420b903` | `rprv` `eab40448` | 111; 112 on regnet |
| Extended public key | `dpub` `02fda926` | `tpub` `043587d1` | `spub` `0420bd3d` | `rpub` `eab4f987` | 111; 112 on regnet |
| Lightning invoice (Bech32 human-readable part) | `lndcr` | `lntdcr` | `lnsdcr` | `lnrdcr` | Varies |

Notes:

- **The WIF prefix starts with `P` on every network.** Only the second character tells the networks apart.
- **The first character is informative only.** Decoders must check the two prefix bytes, not the leading letters.
- **No Decred address uses Bech32.** dcrd ships a `bech32` package, but its only user is Lightning invoices, whose prefix is `ln` plus the network part defined in dcrlnd's `zpay32/invoice.go`.
- **Decred encodings are not Bitcoin's.** The Base58Check checksum uses BLAKE-256, so a Bitcoin library produces strings that Decred software rejects. [Keys, addresses and seeds](../protocol/keys-and-addresses.md) covers address types, WIF and signed messages for implementers.

!!! danger "Check the prefix before sending real funds"
    Wallets reject an address encoded for another network because its prefix bytes do not match. Software that builds output scripts directly from hashes or keys skips that check. Decode every destination with the target network's parameters before broadcasting on mainnet, because a mainnet transaction cannot be reversed.

### Network identity

Source: `wire/protocol.go` and the `Name` field of `chaincfg/*params.go`. The magic number starts every P2P message.

| | mainnet | testnet3 | simnet | regnet |
|---|---|---|---|---|
| `chaincfg` name | `mainnet` | `testnet3` | `simnet` | `regnet` |
| Go constructor | `chaincfg.MainNetParams()` | `chaincfg.TestNet3Params()` | `chaincfg.SimNetParams()` | `chaincfg.RegNetParams()` |
| `wire` constant | `MainNet` | `TestNet3` | `SimNet` | `RegNet` |
| Network magic | `0xd9b400f9` | `0xb194aa75` | `0x12141c16` | `0xdab500fa` |

## HD coin types

Decred wallets derive keys along `m/44'/<COIN_TYPE>'/<ACCOUNT>'/<BRANCH>/<INDEX>`, with branch 0 for receiving addresses and branch 1 for change. Source: `SLIP0044CoinType` and `LegacyCoinType` in `chaincfg/*params.go`; the whitepaper's [wallet account structure](../../whitepaper/05-addresses.md#sec:addresses-bip44) describes the convention.

| Network | Current coin type (`SLIP0044CoinType`) | Legacy coin type (`LegacyCoinType`) |
|---|---|---|
| mainnet | 42 | 20 |
| testnet3 | 1 | 11 |
| simnet | 1 | 115 |
| regnet | 1 | 1 |

- **42 is Decred's entry in the SLIP-0044 registry**, and 1 is the registry's shared value for all test networks.
- **Early wallets used the legacy coin types.** dcrwallet stores keys for both, starts on the legacy one, and switches to the current one when no legacy account or address is in use. `dcrctl --wallet walletinfo` reports the coin type in use as `cointype`, and `disablecointypeupgrades` keeps a wallet on the legacy type.
- **Software that restores a Decred seed should scan both coin types**, or it misses funds from older wallets. [Keys, addresses and seeds](../protocol/keys-and-addresses.md) explains the switch and its edge cases.
- **DCRDEX identifies assets by SLIP-0044 number**, so DCR is asset ID 42 in Bison Wallet and the DCRDEX protocol (`dex/bip-id.go`).

## Legacy names and locations

These still turn up in old guides and old installations.

| Item | Status in 2.1.7 | Where to look instead |
|---|---|---|
| Legacy coin types 20, 11, 115 | Still recognized by dcrwallet for restores; new wallets switch to 42 or 1 | [HD coin types](#hd-coin-types) |
| `data/testnet` and `data/testnet2` in dcrd's home | Data from retired test networks. dcrd logs a warning that it can probably be removed | `data/testnet3` |
| `data/<NET>/utxodb/metadata` in dcrd's home | Transitional location of the UTXO database; dcrd moves it to `utxodb/` automatically | `data/<NET>/utxodb/` |
| `mainnet/wallet.db` or `testnet3/wallet.db` directly in Decrediton's folder | Layout of early Decrediton versions. Decrediton copies such a wallet to `wallets/<NET>/default-wallet/` on start | `wallets/<NET>/<WALLET>/` |
| `dexc`, `dexc.conf`, `dexc.log`, `dexcctl` | Names from before the app became Bison Wallet; still the current names on disk | [Bison Wallet](#bison-wallet) |

## Next steps

- [dcrd configuration](dcrd-config.md): every option that changes a port, path or listener on this page.
- [dcrwallet configuration](dcrwallet-config.md): the wallet's options, including certificates and client authentication.
- [Networks](../environment/index.md): how to select each network and how the networks differ.
- [Your first JSON-RPC call](../api/first-rpc-call.md): put the ports and `rpc.cert` to use from curl, Python or JavaScript.
- [Keys, addresses and seeds](../protocol/keys-and-addresses.md): the encodings behind the prefixes and coin types.

*[HD]: hierarchical deterministic
*[RPC]: remote procedure call
*[gRPC]: a remote procedure call framework over HTTP/2
*[TLS]: Transport Layer Security
*[P2P]: peer-to-peer
*[SPV]: simplified payment verification
*[UTXO]: unspent transaction output
*[P2PKH]: pay-to-pubkey-hash
*[P2SH]: pay-to-script-hash
*[P2PK]: pay-to-pubkey
*[WIF]: wallet import format
*[ECDSA]: Elliptic Curve Digital Signature Algorithm
*[SLIP]: SatoshiLabs Improvement Proposal
*[DEX]: decentralized exchange
*[REST]: representational state transfer
*[API]: application programming interface
