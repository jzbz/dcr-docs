---
description: Back up the right secrets, restore a Decred wallet from its seed, recover funds and VSP tickets that look missing, and move between wallet apps safely.
---

# Back up and restore your wallet

This page shows what to back up, how to restore a wallet from its seed in Decrediton, Bison Wallet or `dcrwallet`, how to find funds and tickets that look missing afterwards, and how to move between wallet apps.

!!! info "Applies to"
    Decrediton 2.1.7, Bison Wallet 1.0.6 and dcrwallet 2.1.7. Checked November 2026.

## Before you start

- Pen and paper, or a metal backup plate, for the seed.
- For a restore: the seed, the wallet app installed and verified (see [Verify your download](../security/verify-downloads.md)), and time to sync. A light wallet (SPV) restores far faster than a full node, which first downloads the whole blockchain.
- To restore tickets bought through a voting service provider (VSP), the name of that VSP.
- If you use Lightning in Decrediton, your latest channel backup file.

## What to back up

For each app, one written secret restores almost everything:

| What | Which app | What it restores |
|---|---|---|
| **Seed**: 33 words, or the same seed as 64 hexadecimal characters | Decrediton, `dcrwallet` | Every key, account, address, coin and ticket of the wallet |
| **App seed**: 15 words (older versions: 128 hexadecimal characters) | Bison Wallet | The built-in wallets for every asset, including DCR, and most DCRDEX accounts |
| **Exported account file** (`.json`) | Bison Wallet, once you trade | A DCRDEX account and its fidelity bonds, including older accounts the app seed cannot restore |
| **DEX Account Seed** | Decrediton's **DEX** tab | DCRDEX accounts and native wallets for other assets; not connected external wallets or accounts from older versions. Its DCR is in a Decrediton account, covered by the seed |
| **Channel backup file** (static channel backup, SCB) | Lightning in Decrediton or `dcrlnd` | The funds in open channels, together with the seed |
| **Device recovery phrase** | Trezor or Ledger | Everything on the device; see [Use a hardware wallet](hardware-wallets.md) |

Passphrases are not part of the seed: a restore needs only the seed, and you choose a new passphrase during it.

The wallet file, `wallet.db`, is not a backup: a copy opens only with the passphrase current when you made it, and it usually sits on the disk that fails. It does hold what the seed cannot rebuild: account names, keys imported with `importprivkey`, accounts imported from an extended public key, and per-account passphrases. If you rely on these, also copy the file while the wallet is stopped; [How a Decred wallet works](how-wallets-work.md) shows where it is.

## Write it down and store it safely

The seed is 32 random bytes, so nobody can guess it. It can only be stolen or lost; store it against both:

- **Write it by hand**, on paper or stamped into metal, in order, each word numbered. Note which app it belongs to.
- **Keep it offline.** Never photograph it or store it in a file, cloud drive, email, chat or a password manager that syncs. Ignore Decrediton's **Copy seed words to clipboard**: other programs can read the clipboard.
- **Keep two copies in separate places**, safe from fire, water and visitors.
- **Plan for others.** Decide who should be able to find it if something happens to you.

!!! danger "Anyone who sees your seed owns your funds"
    Type a seed only into the restore screen of an official Decred wallet. No support person, website, "wallet validation" tool or exchange ever needs it. If you think someone has seen it, create a new wallet now and send everything to it.

### Test the backup

A seed you have never restored from is a hope, not a backup. Test it before you move in a large amount:

1. Send a small amount to the new wallet.
2. Restore the seed from your paper as a second wallet: in Decrediton, under a different **Wallet Name**; with `dcrwallet`, in a separate data directory (`--appdata`) while your main wallet is stopped.
3. Check that the restored wallet shows the same balance.
4. Remove the test wallet (see [Remove a wallet from a computer](#remove-a-wallet-from-a-computer)).

For Bison Wallet, read your app seed back through **Settings** > **View Application Seed** and compare it word by word with the paper.

## Restore from your seed

=== "Decrediton"

    1. On the wallet selection screen, click **Restore Existing Wallet**.
    2. Enter a **Wallet Name** (any name). Leave **Advanced Options** alone unless [Funds look missing?](#funds-look-missing) sends you there.
    3. Click **Continue**.
    4. Type the 33 words, one per box. For a hexadecimal seed, switch the toggle from **words** to **hex**.
    5. Enter a new **Private passphrase** and repeat it, then click **Create Wallet**.

    Decrediton scans the blockchain for your accounts, addresses and transactions. Depending on what it finds, it may then show:

    - **Set Mixed Account**, if some accounts hold mixed coins: choose which account was mixed and which unmixed, since account names are not on the blockchain. See [Mix your DCR](../privacy/mix-your-dcr.md).
    - **Process Managed Tickets** and **Process Unmanaged Tickets**, if you have live tickets. See [Tickets after a restore](#tickets-after-a-restore).

    Restored accounts appear as `account-1`, `account-2` and so on. To rename them, see [Manage accounts and passphrases](accounts-and-passphrases.md).

=== "Bison Wallet"

    A Bison Wallet app seed can only be entered when Bison Wallet starts with no existing data.

    1. Start Bison Wallet. On **New Password**, enter a new app password in **Password** and **Password Again**.
    2. Click **Restoration Seed** and type your app seed in the box that opens.
    3. Click **Submit**.
    4. In **Quick Configuration**, select the same wallets and DCRDEX server you used before, then click **Submit**. The built-in wallets are rebuilt from the app seed and start syncing.
    5. If you exported your DCRDEX account, open **Settings**, click **Import Account**, choose the `.json` file with **load from file**, and click **Authorize Import**.

    The [trading guide](../dex/trading-guide.md) covers bonds and accounts.

=== "Command line"

    Stop `dcrwallet` and move any old `mainnet/wallet.db` out of its data directory. Then run:

    ```bash
    dcrwallet --create
    ```

    Answer the prompts. At "Do you have an existing wallet seed you want to use?", type `yes`, then the 33 words; line breaks are fine, capitals do not matter, and an empty line ends the input. Answer `no` to the birthday question unless you are certain of the date: a birthday that is too late makes the wallet skip older transactions. The output prints your seed in hexadecimal, so clear the terminal afterwards.

    Start the wallet as usual, for example `dcrwallet --spv` for light mode. On this first run it prints `*** ATTENTION ***` and asks for the private passphrase, which it needs to find your accounts. It then stays unlocked; lock it afterwards with `dcrctl --wallet walletlock`.

    On testnet, add `--testnet` to both commands; the wallet file is then `testnet3/wallet.db`.

## Funds look missing?

First let the wallet finish syncing; a balance can climb for a while as old blocks are scanned. If something is still missing, the usual causes are these:

| Cause | Fix |
|---|---|
| More than 20 unused addresses in a row (the default address gap limit) | Discover address usage with a larger gap limit (below) |
| More than 10 unused accounts in a row (the default account gap limit in `dcrwallet`) | Raise `accountgaplimit`, then discover usage with accounts (below) |
| A command-line restore was given a birthday later than your first transaction | Discover usage from the genesis block, then rescan (below) |
| The wallet predates Decred v1.1.2 (December 2017), so its coins use the legacy coin type, but the restore found none and switched to the current one | Restore again with a larger gap limit and **Disable coin type upgrades** (Decrediton **Advanced Options**), or with `disablecointypeupgrades=1` and a larger `gaplimit` (such as `gaplimit=100`) in `dcrwallet.conf` before `dcrwallet --create` |
| The funds were in another app's wallet, such as Bison Wallet or a multi-coin wallet | Restore that app's own seed in that app |

Both gap limits are wallet defaults, not network rules: unused addresses and accounts leave no trace on the blockchain, so the wallet stops looking after that many.

=== "Decrediton"

    1. Click the gear icon (**Settings**) at the bottom of the sidebar.
    2. On the **General** tab, under **Address Usage**, click **Discover Address Usage**.
    3. Enter a **Gap Limit**, for example 100, and click **Discover Address Usage**.

    Decrediton then rescans on its own. Gap limits above 100 make this very slow. To rescan without discovery, use the rescan button at the bottom of the sidebar.

=== "Bison Wallet"

    1. On the Wallets page, select Decred and click **Settings**. In the form that opens, raise **Address Gap Limit** and click **Submit**. The running wallet keeps its old limit; the new one is used when the wallet is next created.
    2. Under **Other Actions**, click **Recover**. Bison Wallet moves the Decred wallet's data to a backup folder and rebuilds the wallet from your app seed with the new gap limit. It refuses while you have active orders, and the wallet is unusable until it has synced again.

    **Rescan**, under the same **Other Actions**, only rescans with the gap limit the wallet already uses.

=== "Command line"

    Unlock the wallet if it is locked (`promptsecret` reads the passphrase without echoing it), discover addresses and accounts from the genesis block with a larger gap limit, and rescan:

    ```bash
    promptsecret | dcrctl --wallet walletpassphrase - 0
    dcrctl --wallet discoverusage 298e5cc3d985bfe7f81dc135f360abe089edd4396b86d2de66b0cef42b21d980 true 100
    dcrctl --wallet rescanwallet 0
    ```

    The long hexadecimal value is the mainnet genesis block; on testnet, use the output of `dcrctl --wallet getblockhash 0`. `true` adds account discovery, which uses the `accountgaplimit` set in `dcrwallet.conf`. When the rescan finishes, restart `dcrwallet` so it watches the newly found addresses.

## Tickets after a restore

Tickets survive a restore: the wallet finds them on the blockchain, and a VSP keeps voting every ticket whose fee it received. A restore loses only the wallet's record of each ticket's VSP and fee status. Without it, the wallet cannot show fee status, send changed vote choices to the VSP, or pay a fee that was never paid.

Relinking rebuilds that record. Link each ticket only to the VSP you bought it through: linking it to another VSP can make the wallet pay that VSP a second fee.

=== "Decrediton"

    After a restore with live or immature tickets, Decrediton can show two screens while the wallet opens:

    - **Process Managed Tickets**: asks the VSP of each already linked ticket whether it knows the ticket and has its fee. Click **Continue** and enter your private passphrase.
    - **Process Unmanaged Tickets**: links tickets that have no VSP record to the VSP you select. Select the VSP you bought them through, click **Continue** and enter your passphrase. If you used several VSPs, or do not know which, click **Skip** and [ask for help](../reference/index.md) first.

    Then check the **Fee Status** column in **Staking** > **Ticket Status**. A ticket whose fee the VSP already had can show **Error** at first: close and reopen the wallet, and click **Continue** on **Process Managed Tickets** to read its status from the VSP. **Sync Failed VSP Tickets**, on the same tab, retries failed fee payments.

=== "Command line"

    The wallet signs every request to a VSP with a private key, so it must stay unlocked throughout. Put the VSP your tickets used in `dcrwallet.conf`, then restart `dcrwallet` with `--promptpass` and enter your private passphrase. The VSP's public key is in the footer of its website.

    ```ini
    [VSP Options]
    vsp.url=https://<VSP HOST>
    vsp.pubkey=<VSP PUBKEY>
    vsp.sync=1
    ```

    List your live and immature tickets, then link each one:

    ```bash
    dcrctl --wallet gettickets true
    dcrctl --wallet processunmanagedticket <TICKET HASH>
    ```

    `<TICKET HASH>` is one hash from the `gettickets` list. If the ticket's fee was never paid, the command pays it, provided the VSP's fee is no higher than `vsp.maxfee` (default 0.2 DCR). If the VSP already has the fee, the command returns an error saying so, but the ticket is now linked.

    When you have processed every ticket, restart `dcrwallet` with `--promptpass` again and enter your private passphrase. With `vsp.sync=1` and the wallet unlocked, each start asks the VSP for the status of linked tickets whose fee is not yet confirmed, and records it.

Bison Wallet 1.0.6 has no relinking screen. Its VSP keeps voting your tickets as long as it received their fees.

If you vote solo, your voting wallet must be restored, unlocked and running before your tickets are chosen; see [Vote without a VSP](../staking/solo-voting.md).

## Moving between wallet apps

Seeds come in different formats, and each restores only in software that understands it.

| Moving from | To | Use the seed? |
|---|---|---|
| Decrediton | `dcrwallet`, or the reverse | Yes: the same 33-word seed restores in both |
| Decrediton or `dcrwallet` | Bison Wallet, or the reverse | No: send the DCR to an address in the new wallet |
| Bison Wallet | Bison Wallet on another computer | Yes: the app seed, plus the exported account file |
| Any Decred wallet | A third-party wallet listed on [decred.org/wallets](https://decred.org/wallets/) | Only if that wallet's own documentation says it accepts Decred's 33-word seed; otherwise send the coins |

Many multi-coin wallets use BIP-39 phrases of 12 to 24 words, a different format that does not restore in Decrediton or `dcrwallet`, nor the reverse. Do not run conversion tools on a seed.

Even a wallet that accepts the 33 words can miss funds:

- **Legacy coin type.** Wallets created before Decred v1.1.2 used coin type 20 instead of 42; a wallet that scans only coin type 42 does not see those funds. See the whitepaper's [wallet account structure](../../whitepaper/05-addresses.md#sec:addresses-bip44).
- **Key derivation.** Decred's derivation differs slightly from standard BIP-32, so for a small fraction of seeds a strictly standard implementation derives different keys. See the whitepaper's [hierarchical deterministic keys](../../whitepaper/05-addresses.md#sec:addresses-hd).

When in doubt, send the coins instead of the seed: a small test amount first, then the rest. Live tickets cannot be sent; keep the old wallet until they have voted, then move what returns.

## Restoring Lightning funds

The seed alone does not restore funds in open Lightning channels; you also need the channel backup file. In Decrediton it is under **Lightning Transactions** > **Advanced** > **Backup**. A standalone `dcrlnd` node has its own 24-word seed and a `channel.backup` file. [Back up and protect Lightning funds](../lightning/backups-and-watchtowers.md) has the procedure.

!!! danger "Never restore an old channel database"
    Restoring an outdated copy of a channel database can cost you the channel's funds. Recover channels only from the seed plus the channel backup file.

## Remove a wallet from a computer

Before you remove a wallet, confirm that you have its seed (test it as above), that no DCRDEX trades are active, and that Lightning channels are closed.

=== "Decrediton"

    On the wallet selection screen, click **Edit Wallets**, then **Remove Wallet** on the wallet, and confirm. This permanently deletes the wallet's folder, including its Lightning and DEX data; the blockchain data and Decrediton's settings stay.

=== "Bison Wallet"

    Bison Wallet has no remove button. Quit it and delete its data folder: `~/.dexc` on Linux, `~/Library/Application Support/Dexc` on macOS, `%LOCALAPPDATA%\Dexc` on Windows. This removes every built-in wallet and every DCRDEX account on this computer.

=== "Command line"

    Stop `dcrwallet` and delete `mainnet/wallet.db` from its data folder: `~/.dcrwallet` on Linux, `~/Library/Application Support/Dcrwallet` on macOS, `%LOCALAPPDATA%\Dcrwallet` on Windows.

Deleted files can often be recovered. The private keys inside are encrypted with your private passphrase, but the transaction history (amounts and the addresses it paid) can be read from the file. A public passphrase hides only the account keys that reveal your other addresses. Wipe the whole disk before you sell or give away a computer.

## Lost seed or forgotten passphrase

What you can still do depends on what you still have:

- **Forgotten private or public passphrase:** restore from the seed with a new passphrase. In Decrediton, restore under a new name, then remove the old wallet.
- **Forgotten Bison Wallet app password:** on the **Unlock** screen, click **Forgot Password?** and set a new one with the app seed.
- **Seed lost, wallet still opens:** act now, before the disk fails. Decrediton and `dcrwallet` do not store the seed and cannot show it again. Create a new wallet, test its seed, and send your funds to it, as in [Moving between wallet apps](#moving-between-wallet-apps). Bison Wallet, by contrast, can show its app seed again (**View Application Seed**).
- **Seed and wallet both lost:** the funds are gone. Nobody, including Decred's developers, can recover a seed or bypass a passphrase; anyone offering to, for a fee, is a scammer.

## Check that it worked

- Once syncing has finished, the restored wallet shows the balance, accounts and history you expect.
- Each live VSP ticket shows **Paid** or **Confirmed**, not **Error**, in the **Fee Status** column of Decrediton's **Staking** > **Ticket Status**. On the command line, `dcrctl --wallet ticketinfo` lists a `vsphost` for each linked ticket, and after a restart with `--promptpass` the `dcrwallet` log shows no VSP errors naming the ticket.
- After a backup test, the test wallet showed the same balance and has been removed.

## Troubleshooting

### Decrediton says a word is not valid

"Error: word on position N is not valid" means the word in that box belongs to the other half of the word list, usually because a word before it is missing or entered twice. Check the order against your paper. "Error: seed is not valid" appears once all 33 boxes are filled and the checksum does not match: a word is wrong or two words are swapped.

### The hex seed is rejected or warns about its length

A Decred hex seed is 64 characters. Decrediton accepts 32 to 128 characters but warns that a seed of a different length "comes from a non-supported software". That usually means it is not a Decred seed.

### dcrwallet says the wallet database file already exists

`dcrwallet --create` never overwrites a wallet. Move the old `wallet.db` somewhere safe and run it again.

## Next steps

- [Keep your DCR safe](../security/index.md): the scams that target seeds, and how to avoid them.
- [Stake with Decrediton or Bison Wallet](../staking/stake.md): buy tickets once your backup is tested.
- [Use a hardware wallet](hardware-wallets.md): keep keys on a device instead of the computer.
- [Cold storage with an offline wallet](../security/cold-storage.md): for larger amounts.
- [Wallet troubleshooting](troubleshooting.md): fixes for other wallet problems.

*[VSP]: voting service provider
*[SPV]: simplified payment verification
*[DEX]: decentralized exchange
*[SCB]: static channel backup
*[BIP]: Bitcoin Improvement Proposal
