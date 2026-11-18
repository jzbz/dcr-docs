---
description: Download, verify and set up Bison Wallet 1.0.6, create its Decred light wallet, back up the app seed, and send and receive DCR.
---

# Install and set up Bison Wallet

This guide takes you from download to a working Bison Wallet with a Decred wallet inside it, ready to receive and send DCR and, later, to stake, mix and trade on DCRDEX.

!!! info "Applies to"
    Bison Wallet 1.0.6, as shipped with the Decred 2.1.7 release. Checked November 2026.

## What Bison Wallet is

Bison Wallet is two things in one app:

- **A multi-asset wallet.** Its built-in ("native") Decred wallet is a light wallet (SPV, simplified payment verification) that checks the chain without downloading every block. It sends and receives, buys tickets through a voting service provider (VSP), mixes coins with StakeShuffle and sets vote preferences.
- **The client for DCRDEX**, the Decred exchange network, where trades settle by atomic swaps between the traders' own wallets. [DCRDEX: Trading without custody](../dex/index.md) explains the model.

Bison Wallet runs as a program on your computer and shows its interface in your web browser. Closing the browser tab does not stop it; the program must keep running while it mixes coins or settles trades.

Version 1.0.6 cannot vote without a VSP, vote on Politeia proposals, or use Lightning; [Decrediton](decrediton.md) can.

## Before you start

- A computer running Windows, macOS, Linux, FreeBSD or OpenBSD, and a web browser.
- Pen and paper for the 15-word app seed.
- About 30 minutes, plus the first sync. You need no DCR to set up.
- An OpenPGP tool such as GnuPG to check the download.

## Step 1: Download Bison Wallet

Download from the [Decred v2.1.7 release on GitHub](https://github.com/decred/decred-binaries/releases/tag/v2.1.7). Bison Wallet has its own version number, so its files are named `v1.0.6`.

| System | File |
|---|---|
| Windows, 64-bit Intel or AMD | `bisonwallet-windows-amd64-v1.0.6.zip` |
| Windows on ARM | `bisonwallet-windows-arm64-v1.0.6.zip` |
| macOS, Apple silicon | `bisonwallet-darwin-arm64-v1.0.6.tar.gz` |
| macOS, Intel | `bisonwallet-darwin-amd64-v1.0.6.tar.gz` |
| Linux, 64-bit Intel or AMD | `bisonwallet-linux-amd64-v1.0.6.tar.gz` |
| Linux, 64-bit ARM | `bisonwallet-linux-arm64-v1.0.6.tar.gz` |

Builds for other systems (32-bit, RISC-V, FreeBSD, OpenBSD) are on the same page. Also download `bisonwallet-v1.0.6-manifest.txt` and `bisonwallet-v1.0.6-manifest.txt.asc` for step 2. Each archive holds `bisonw`, the wallet, and `bwctl`, a scripting tool you can ignore.

Alternatively, **dcrinstall** from the [decred-release v2.1.7 release](https://github.com/decred/decred-release/releases/tag/v2.1.7) installs `bisonw` and `bwctl` into `~/decred` (`%USERPROFILE%\decred` on Windows) with the [command-line suite](command-line.md) and checks the signature and hashes for you. The desktop installers in the [Bison Wallet download guide](https://github.com/decred/dcrdex/wiki/Download-and-Install) were still at 1.0.5 when this page was checked. To compile it yourself, see [Build from source](../../dev/environment/build-from-source.md).

!!! warning "Download only from GitHub"
    Fake wallet apps are a common way to steal coins. Use the release linked above, never a link from a chat message, an advertisement or a search result. The Bison Wallet entry on the [official wallet list](https://decred.org/wallets/) links to the dcrdex source tag, which has no download files; the 1.0.6 files are on the decred-binaries release.

## Step 2: Verify the download

Verification proves the file was signed by the Decred release key and not altered on the way to you:

1. **Check the manifest signature.** `bisonwallet-v1.0.6-manifest.txt.asc` must be a good signature from `Decred Release <release@decred.org>`, made with the signing subkey `F516 ADB7 A069 852C 7C28 A02D 6D89 7EDF 518A 031D`.
2. **Check the archive's hash.** Compute the SHA-256 hash of your archive and find the identical value in the manifest, next to the file name:

    ```text title="A line from bisonwallet-v1.0.6-manifest.txt"
    b71d3dea19573b1f4793a5dafa14fee8a499e66624089995ef233a1e0d712efe  bisonwallet-linux-amd64-v1.0.6.tar.gz
    ```

[Verify your download](../security/verify-downloads.md) gives the commands for each operating system. If either check fails, delete the files and do not run them.

## Step 3: Start Bison Wallet

=== "Windows"

    1. Right-click the `.zip` file and choose **Extract All**. The archive holds two identical copies of `bisonw.exe`; if Windows asks whether to replace the file, either choice is fine.
    2. Open the extracted folder and double-click `bisonw`.
    3. No console window appears. Bison Wallet adds an icon to the system tray (notification area) and opens your browser at `http://127.0.0.1:5758` when it is ready. To stop it, choose **Quit** from the tray icon's menu.

=== "macOS"

    1. Double-click the `.tar.gz` file in Finder to extract it.
    2. In **Terminal**, start the wallet from the extracted folder (use `darwin-amd64` on an Intel Mac):

        ```bash
        cd ~/Downloads/bisonwallet-darwin-arm64-v1.0.6
        ./bisonw
        ```

    3. When startup finishes, Terminal shows the address to open:

        ```text title="Expected output (last line)"
        ****  OPEN IN YOUR BROWSER TO LOGIN AND TRADE  --->  http://127.0.0.1:5758  ****
        ```

    Closing Terminal stops Bison Wallet; so does ++ctrl+c++.

=== "Linux"

    1. Extract the archive and start the wallet (change `amd64` to your architecture if needed):

        ```bash
        tar -xzf bisonwallet-linux-amd64-v1.0.6.tar.gz
        cd bisonwallet-linux-amd64-v1.0.6
        ./bisonw
        ```

    2. When startup finishes, the terminal's last line says to open `http://127.0.0.1:5758` in your browser. Closing the terminal stops Bison Wallet; so does ++ctrl+c++.

Stopping Bison Wallet with active orders can make swaps fail and hurt your account's standing. ++ctrl+c++ warns and asks first in that case; the Windows tray's **Quit** does not.

!!! note "Testnet"
    Start with `bisonw --testnet` to use testnet coins. The interface is then at `http://127.0.0.2:5758` (note the `.2`), and testnet data is kept apart from mainnet.

## Step 4: Set your app password

Bison Wallet has two secrets of its own. Neither is a Decred wallet seed or passphrase, and a seed from Decrediton or `dcrwallet` cannot be entered into it.

- The **app password** unlocks Bison Wallet on this computer and authorizes sending, trading and posting bonds.
- The **app seed** is 15 words. The keys of every native wallet and of your DCRDEX accounts are derived from it, so it restores them on any computer. An external `dcrwallet` keeps its own seed.

On first launch the browser shows the **New Password** form:

1. Type a strong password in **Password** and again in **Password Again**.
2. Click **Submit**. Bison Wallet creates a new app seed.

To restore an existing Bison Wallet instead, click **Restoration Seed** before **Submit** and enter your 15-word app seed (the 128-character hexadecimal seeds of older versions also work).

## Step 5: Create the Decred wallet

The **Quick Configuration** form comes next.

1. Keep **Decred** checked. Uncheck other assets you do not want yet; you can add wallets later.
2. Keep `dex.decred.org:7232` checked if you plan to trade. This view-only connection lets you watch the markets; it creates no account and posts no bond.
3. Click **Submit**.

If a wallet or server fails, click **Continue** and retry later: wallets from the **Wallet** view, servers from **Settings** > **Add a DCRDEX Server**. To create the Decred wallet later, open **Wallet**, select **Decred**, click **Create a Decred Wallet**, stay on the **Native** tab and click **Create!**.

### Using an existing dcrwallet instead

The **External** tab of that dialog connects to a `dcrwallet` 2.1 that you already run. Enter its **RPC Username**, **RPC Password**, **RPC Address** (default `127.0.0.1:9110`), **TLS Certificate** (default: `rpc.cert` in the `dcrwallet` data folder) and private passphrase (**Wallet Password**), then click **Add**. Keep that `dcrwallet` running, and do not lock, unlock or spend from it directly while trades are active.

The privacy switch works only with the native wallet; an external `dcrwallet` mixes through its own settings. The **Staking** panel does appear, but its VSP must be set with `vsp.url` in `dcrwallet`'s own configuration, and staking may be unavailable when that `dcrwallet` runs in light mode (**Staking unavailable for RPC wallets using SPV**).

## Step 6: Back up the app seed

After creating a new app seed (not after a restore), Bison Wallet shows **Backup App Seed**.

1. Make sure nobody can see your screen, and click **Backup Now**.
2. Write the 15 words on paper, in order, and check them twice.
3. Click **Done**. The **Wallet** view opens.

If you clicked **Skip this step for now**, open the menu at the top right later and choose **Settings** > **View Application Seed**, enter your app password and click **Show Me**.

!!! danger "Your app seed is your money"
    Anyone who has the 15 words can take every coin in your native wallets, from any computer. Type them only into Bison Wallet's own **Restoration Seed** box, never into a website, chat, support form or "wallet validation" tool. If you lose both the seed and this computer's wallet files, nobody can recover the funds.

## Step 7: Let the wallet sync

In **Wallet** > **Decred**, watch the details panel. **Block Sync** rises to 100%, **Balance Discovery** finds past transactions (it matters after a restore), and **Status** shows **Ready** when the wallet is usable. Keep Bison Wallet running until the first sync finishes.

## Step 8: Receive and send DCR

Both start from **Wallet** > **Decred**; [Send and receive DCR](send-and-receive.md) explains addresses, fees and confirmations.

To receive, click **Receive** and copy the address or show its QR code. **New Address** gives a fresh one, which is better for privacy. The payment appears in **Decred Transaction History** and in your balance as soon as the wallet sees it, before it is mined (a block is mined about every 5 minutes).

To send:

1. Click **Send**, paste the address into **Address** and enter the **Amount**. **Max Estimated Send** shows the most you can send; check **Subtract fees from amount sent.** to take the fee out of the amount.
2. Click **Send** and review **Confirm Transfer**, including the **Estimated Fee**.
3. Enter your app password under **Password** and click **Confirm**.

!!! warning "Sent transactions cannot be reversed"
    Check the whole address before you confirm, and send only to a Decred mainnet address. These start with `D`: usually `Ds`, or `Dc` for script addresses. Testnet addresses start with `T`. Nobody can undo a mistake.

## Turn on privacy and staking

Both are optional and live in the Decred wallet view; their how-tos cover the details.

- **Privacy.** Flip the switch next to **Privacy off**; it changes to **Privacy active**. The wallet starts using its `mixed` and `dextrading` accounts and mixes your funds with StakeShuffle, Decred's peer-to-peer mixing protocol, while Bison Wallet runs and the wallet stays unlocked. Wallets mix only with peers that use the same mixing pairing version, so Bison Wallet 1.0.6 does not mix with Decrediton or `dcrwallet` 2.1.5 and later, only with other wallets on the older version. Turning privacy off moves all mixed funds back to the default account. See [Mix your DCR](../privacy/mix-your-dcr.md).
- **Staking.** In the **Staking** panel, click **Select a Voting Service Provider**, choose a VSP or enter a custom VSP URL, then click **Purchase Tickets**. **Set Votes** sets your choices on consensus agendas and treasury spends. A ticket locks its DCR until it votes, on average 8,192 blocks (about 28 days) after it matures, and cannot be cancelled. See [Stake with Decrediton or Bison Wallet](../staking/stake.md).

## Where Bison Wallet keeps its data

Everything lives in one data folder, named after the app's earlier name, `dexc`: `~/.dexc` on Linux, FreeBSD and OpenBSD, `~/Library/Application Support/Dexc` on macOS, and `%LOCALAPPDATA%\Dexc` on Windows. The `--appdata` option chooses a different folder.

| Inside it | What it is |
|---|---|
| `dexc.conf` | Optional settings file. |
| `mainnet/dexc.db` | The app database: settings, orders, swap records and your account keys (the keys are encrypted with your app password). |
| `mainnet/backup/dexc.db` | A copy of the database, refreshed every time Bison Wallet shuts down. |
| `mainnet/assetdb/dcr/` | The native Decred wallet; other assets have their own folders. |
| `mainnet/logs/dexc.log` | The log file. |

Testnet uses `testnet/` instead of `mainnet/`. The database tracks swaps in progress, so never delete the folder while trades are active.

Back up the app seed above all. Once you trade, also export your DCRDEX accounts, because some older accounts cannot be restored from the seed (see the [trading guide](../dex/trading-guide.md)). An external `dcrwallet` needs its own seed backed up.

## Upgrading

!!! warning "Finish or cancel your trades before upgrading"
    Replace Bison Wallet only when no orders or swaps are active. Bison Wallet 1.1 (tagged, not yet released when this page was checked) cannot trade on 1.0.x servers, and 1.0.x clients cannot trade on 1.1 servers; see [Upgrading and mandatory releases](../run/upgrades.md) for the procedure.

## Check that it worked

- **Wallet** > **Decred** shows **Status** **Ready** and **Block Sync** at 100%.
- A small test payment to your **Receive** address appears in **Decred Transaction History** and in your balance.
- Your app seed is on paper, and the **Version** line at the bottom of the menu starts with 1.0.6.

## Troubleshooting

### The browser page does not load

Use `http://127.0.0.1:5758`, not `https`. On Windows, choose **Launch browser** from the tray icon. On macOS and Linux, check that the terminal running `bisonw` is still open and shows no error. Bison Wallet cannot start if another program already uses port 5758.

### Windows warns that it protected your PC

`bisonw.exe` is not signed with a Windows code-signing certificate, so Microsoft Defender SmartScreen may show "Windows protected your PC". Only once you have verified the download (step 2), click **More info** and then **Run anyway**.

### macOS refuses to open bisonw

The archives are not signed with an Apple developer certificate, so macOS may block the program. Only once you have verified the download (step 2), allow it in macOS's privacy and security settings.

### Forgotten app password

On the unlock screen, click **Forgot Password?**, enter a **New Password** twice and your app seed in **Restoration Seed**, then click **Submit**. Without the app seed, the password cannot be reset.

### Balance missing after a restore

Wait for **Balance Discovery** to finish. If funds are still missing, choose **Rescan** under **Settings** in the Decred wallet panel, but not while trades are active.

### The Decred wallet will not lock

Mixing needs the wallet unlocked, so Bison Wallet refuses to lock it ("cannot lock wallet while mixing") while privacy is active. Turn privacy off first.

## Next steps

- [Your first trade on DCRDEX](../dex/first-trade.md): post a bond and place a small order.
- [Stake with Decrediton or Bison Wallet](../staking/stake.md): buy tickets and set your votes.
- [Mix your DCR](../privacy/mix-your-dcr.md): keep mixed coins private when you spend them.
- [Wallets for other assets in Bison Wallet](../dex/asset-wallets.md): add the other asset of a trading pair.
- [Back up and restore your wallet](back-up-and-restore.md): test your backup.

The whitepaper's [atomic swaps and DCRDEX section](../../whitepaper/19-ecosystem.md#sec:ecosystem-dex) describes the swap contract and bonds in detail.

*[SPV]: simplified payment verification
*[VSP]: voting service provider
*[RPC]: remote procedure call
*[TLS]: Transport Layer Security
