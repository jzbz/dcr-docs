---
description: Set how your tickets vote on consensus agendas, treasury spends and Politeia proposals, with or without a VSP, and check that each vote counted.
---

# Vote with your tickets

Each ticket gives you a say on consensus rule changes, treasury spends and Politeia proposals. This page shows how to cast each kind of vote in Decrediton, Bison Wallet or on the command line, with or without a voting service provider (VSP), and how to check that it counted.

!!! info "Applies to"
    Decrediton 2.1.7, Bison Wallet 1.0.6, dcrwallet 2.1.7 with dcrctl 2.1.7, and `politeiavoter` 1.5.0 from the Decred 2.1.7 command-line bundle. Checked November 2026.

## Before you start

- Tickets bought with this wallet (see [How staking works](../staking/index.md)):
    - for agendas and treasury spends, tickets that are unmined, immature or live; a ticket that has voted on chain cannot vote on chain again;
    - for Politeia, tickets that were live at the proposal's snapshot, whatever has happened to them since.
- Your **private passphrase** (Decrediton and dcrwallet). Bison Wallet only needs you to be logged in.
- A wallet that can sign: watching-only wallets cannot vote, and Trezor- or Ledger-backed wallets cannot stake ([Use a hardware wallet](../wallets/hardware-wallets.md)).
- With a VSP: the wallet open, unlocked and online when you change a choice, so it can send the change to the VSP. It need not stay online afterwards.
- For Politeia: the wallet that bought the tickets, open and unlocked once while each proposal's vote is running.

## How each kind of vote works

| | Consensus agendas | Treasury spends | Politeia proposals |
|---|---|---|---|
| Counted | On chain, in your ticket's vote | On chain, in your ticket's vote | Off chain, by the Politeia server |
| Cast by | The wallet that votes the ticket: the VSP's or your own | Same as agendas | The wallet that bought the ticket, never a VSP |
| Choice read | When the ticket is drawn to vote | When the ticket is drawn to vote | When you click **Cast Vote** |
| If you set nothing | Abstain | Abstain | No vote |
| Change it later? | Yes, until the ticket votes | Yes, until the ticket votes | No: a cast vote is final |

For agendas and treasury spends, clicking sets a standing instruction rather than casting a vote. When the lottery draws one of your tickets, the voting wallet writes the choices in force at that moment into the vote transaction. A missed ticket records nothing.

## With a VSP: Your choices travel to it

A VSP holds your tickets' voting rights, so its wallet builds the votes ([Voting service providers](../staking/vsps.md) explains the arrangement). Your wallet keeps it informed:

- **When the VSP fee is paid**, your wallet sends the choices it has at that moment.
- **Whenever you change a choice**, your wallet signs an update with the key of each ticket's commitment address (which the VSP does not have) and sends it to the VSP for every unspent ticket whose stored choice differs. That is why the wallet must be unlocked and online at that moment. The VSP accepts updates only for tickets whose fee it has received and that are unmined, immature or live.

When a ticket is drawn, the VSP votes it with the choices it holds, even if your wallet is closed. Where you can, set your choices before you buy tickets, so the fee payment already carries them.

## Vote on consensus agendas

An agenda is a proposed consensus rule change, named by an id such as `maxtreasuryspend`. It arrives with a new software release, and its vote runs in intervals of 8,064 blocks (about 4 weeks). [Consensus rule votes](consensus-upgrades.md) explains the thresholds and how to follow a vote.

As of November 2026 no agenda is being voted on: the newest, `maxtreasuryspend`, activated at block 1,052,416. All three wallets still list it, but a choice on a decided agenda has no effect. Check that a vote is live on [dcrdata's agendas page](https://dcrdata.decred.org/agendas) before you act.

=== "Decrediton"

    1. In the sidebar, click **Governance**, then the **Consensus Changes** tab. Each agenda card shows its **Agenda ID**, a status of **In Progress** or **Finished**, and your current **Preference**.
    2. Click the agenda's card.
    3. Under **Voting for:**, select **yes**, **no** or **abstain**.
    4. Click **Update Preference**. In **Confirm Your Vote**, enter your private passphrase and click **Continue**.

    The card shows your new **Preference**, and Decrediton sends it to your VSPs. On a **Finished** agenda the choices are greyed out. Decrediton reads the status from dcrdata, so with **Decred Block Explorer** turned off under **Settings** > **Privacy and Security** it can show a decided agenda as **In Progress**.

=== "Bison Wallet"

    1. Click **Wallet** in the top bar and select **Decred**.
    2. In the **Staking** panel, click **Set Votes**.
    3. Under **Agendas**, click **Abstain**, **No** or **Yes** next to the agenda.

    Each click is saved at once; there is no save button. An error appears in red at the bottom of the form if the wallet could not save it.

=== "Command line"

    List the agendas your wallet knows and your current choice for each:

    ```bash
    dcrctl --wallet getvotechoices
    ```

    ```json title="Expected output (mainnet, nothing set)"
    {
      "version": 11,
      "choices": [
        {
          "agendaid": "maxtreasuryspend",
          "agendadescription": "Change maximum treasury expenditure policy as defined in DCP0013",
          "choiceid": "abstain",
          "choicedescription": "abstain voting for change"
        }
      ]
    }
    ```

    Set a choice:

    ```bash
    dcrctl --wallet setvotechoice <AGENDA_ID> <CHOICE_ID>
    ```

    `<AGENDA_ID>` is an `agendaid` from the list and `<CHOICE_ID>` is `yes`, `no` or `abstain`. The command prints nothing when it succeeds. With a VSP, unlock the wallet first so the change can be sent (`promptsecret | dcrctl --wallet walletpassphrase - 300` unlocks it for 300 seconds without putting the passphrase on the command line).

## Vote on treasury spends

Money leaves the treasury only in a treasury spend (TSPEND), a transaction signed with one of two Politeia keys and approved by ticket votes over a window of 3,456 blocks (about 12 days). [The treasury](treasury.md) explains the approval rule. You can set two kinds of policy, each yes, no or abstain:

- **Per Politeia key**: a standing choice for every spend that key signs, including spends that do not exist yet. A yes here approves future spends you have not seen.
- **Per treasury spend**: a choice for one spend, identified by its transaction hash. A yes or no here overrides the key policy for that spend. Abstain removes the per-spend choice, so the key policy applies again; to abstain on one spend while a key policy is set, change the key policy instead.

Spends waiting for votes are listed on [dcrdata's treasury page](https://dcrdata.decred.org/treasury); each spend's page shows its vote tally.

=== "Decrediton"

    1. In the sidebar, click **Governance**, then the **Treasury Spending** tab.
    2. To set a policy for every spend a key signs: under **Politeia Keys**, find the card with that **Pi key:**, select **yes**, **no** or **abstain**, and click **Update Preference**.
    3. In **Confirm Your Vote**, enter your private passphrase and click **Continue**.
    4. To set a policy for one spend: under **Tspends** (shown only while your wallet knows of spends waiting for votes), find the card with that spend's **Tx hash:**, select a choice, click **Update Preference**, and confirm in the same way.

    Each confirmation saves that one choice and sends it to your VSPs.

=== "Bison Wallet"

    1. Open **Wallet** > **Decred**, and in the **Staking** panel click **Set Votes**.
    2. Under **Treasury Spends**, find the spend by its hash and click **No** or **Yes**.

    Bison Wallet 1.0.6 has no abstain button for treasury spends and cannot set key policies: its **Treasury Keys** list shows only keys that already have a policy, so it is empty in a new wallet. Bison Wallet 1.1.0 lists both keys; it is not released, and only release candidates (v1.1.0-rc2) are tagged.

=== "Command line"

    Per Politeia key (the two mainnet keys are shown):

    ```bash
    dcrctl --wallet settreasurypolicy 03f6e7041f1cf51ee10e0a01cd2b0385ce3cd9debaabb2296f7e9dee9329da946c <POLICY>
    dcrctl --wallet settreasurypolicy 0319a37405cb4d1691971847d7719cfce70857c0f6e97d7c9174a3998cf0ab86dd <POLICY>
    ```

    `<POLICY>` is `yes`, `no` or `abstain`; a yes approves future spends signed by that key. `treasurypolicy` lists the key policies you have set.

    Per spend:

    ```bash
    dcrctl --wallet tspendpolicy
    dcrctl --wallet settspendpolicy <TSPEND_HASH> <POLICY>
    ```

    `tspendpolicy` lists each spend your wallet knows with the `policy` that applies to it, including one that comes from its key; empty means abstain. `<TSPEND_HASH>` is a `hash` from that list or from dcrdata. Here `abstain` removes the per-spend choice. With a full node, `dcrctl gettreasuryspendvotes` shows the spends in the mempool with their tallies.

### Choices for single tickets

`dcrwallet` can also give one ticket its own choices, which take precedence over the wallet-wide choice for the same item. Neither graphical wallet offers this.

```bash
dcrctl --wallet setvotechoice <AGENDA_ID> <CHOICE_ID> <TICKET_HASH>
dcrctl --wallet settspendpolicy <TSPEND_HASH> <POLICY> <TICKET_HASH>
dcrctl --wallet settreasurypolicy <PI_KEY> <POLICY> <TICKET_HASH>
dcrctl --wallet getvotechoices <TICKET_HASH>
```

`<TICKET_HASH>` is a ticket from `dcrctl --wallet gettickets true`, `<PI_KEY>` is one of the two Politeia keys above, and `<POLICY>` is `yes`, `no` or `abstain`. `getvotechoices <TICKET_HASH>` shows the choices that apply to that ticket. With a VSP, only that ticket's VSP is updated, and a later wallet-wide change to the same item overwrites the single-ticket choice there; run the single-ticket commands again afterwards.

## Vote on Politeia proposals

Politeia proposals ask for treasury funding or set project policy; [Politeia proposals](politeia.md) explains the process. Each vote runs for a set number of blocks, usually 2,016 to 4,032 (about 7 to 14 days).

The Politeia server looks up each ticket's largest commitment address, the address that gets the ticket's funds back, and accepts a vote only if it is signed with that address's key. Only the wallet that bought the ticket holds that key. So:

- **A VSP never votes on proposals for you.** It holds only the voting key. If you do nothing, your tickets do not vote.
- **Only tickets live at the snapshot can vote.** The snapshot is the block Politeia lists as the vote's start block, 256 blocks before voting opens. A ticket turns live 256 blocks after it is mined, so it must be mined at least 256 blocks before that start block: about 512 blocks (about 43 hours) before voting opens. Tickets that vote on chain or expire after the snapshot can still vote.
- **Decrediton and `politeiavoter` vote all your eligible tickets the same way**, and a cast vote cannot be changed.

=== "Decrediton"

    1. In the sidebar, click **Governance**, then the **Proposals** tab. If you see "Politeia integration is disabled by privacy settings", click **Enable Politeia Integration** (or tick **Politeia** under **Settings** > **Privacy and Security**).
    2. Open the **Voting** tab and click a proposal. It shows **Tickets eligible for voting:** with your count.
    3. Under **My voting preference:**, select **Yes** or **No**.
    4. Click **Cast Vote**. **Confirm Your Vote** says how many tickets will vote; enter your private passphrase and click **Continue**.

    A **Voted** check mark appears and the choice is locked. "Voting is only available upon participation in Staking." means the wallet has no tickets; "You don't have tickets elligible for voting on this proposal" means none was live at the snapshot.

=== "Command line"

    `politeiavoter` ships in the command-line bundle and talks to `dcrwallet` over gRPC, which needs a client certificate. `dcrinstall` creates it when it first sets up the wallet; if you installed another way, set it up once:

    === "Windows"

        ```powershell
        cd $env:LOCALAPPDATA
        New-Item -ItemType Directory -Force Politeiavoter
        gencerts Politeiavoter\client.pem Politeiavoter\client-key.pem
        Get-Content Politeiavoter\client.pem | Add-Content Dcrwallet\clients.pem
        ```

    === "macOS"

        ```bash
        cd "$HOME/Library/Application Support"
        mkdir -p Politeiavoter
        gencerts Politeiavoter/client.pem Politeiavoter/client-key.pem
        cat Politeiavoter/client.pem >> Dcrwallet/clients.pem
        ```

    === "Linux"

        ```bash
        mkdir -p ~/.politeiavoter
        gencerts ~/.politeiavoter/client.pem ~/.politeiavoter/client-key.pem
        cat ~/.politeiavoter/client.pem >> ~/.dcrwallet/clients.pem
        ```

    Then restart `dcrwallet`; it starts its gRPC server only if `clients.pem` exists.

    List the proposals under vote, with your eligible tickets and the command for each choice:

    ```bash
    politeiavoter inventory
    ```

    Cast the vote:

    ```bash
    politeiavoter vote <TOKEN> yes
    ```

    `<TOKEN>` is the proposal token from `inventory`; the choice is `yes` or `no`. The tool asks for your private passphrase.

    ```text title="Expected output"
    Enter the private passphrase of your wallet:
    Votes succeeded: 9
    Votes failed   : 0
    ```

    On testnet, add `--testnet` to each command.

Bison Wallet 1.0.6 cannot vote on proposals. Politeia voting arrives in Bison Wallet 1.1.0, which is not released; only release candidates (v1.1.0-rc2) are tagged.

!!! warning "Your tickets can be linked to your IP address"
    Decrediton always sends all of a wallet's votes in one request, and `politeiavoter` does so by default, so the Politeia server operator can see which IP address controls those tickets ([Privacy beyond mixing](../privacy/privacy-practices.md)). `politeiavoter` can instead send them one at a time, at random moments, through a local Tor proxy:

    ```bash
    politeiavoter --proxy=127.0.0.1:9050 --trickle vote <TOKEN> yes
    ```

    `politeiavoter` must keep running, with Tor available, until the last vote is sent. Votes not yet sent when it stops are not cast; running the same command again sends only the tickets that have not voted. Without `--voteduration` it spreads the votes over the remaining time minus 12 hours (`--hoursprior`), and it refuses to start when that leaves less than 24 hours; then set a shorter duration such as `--voteduration=6h`. `--trickle` requires `--proxy`.

## Solo voters: Set choices on every voting wallet

Without a VSP, your voting wallets build the votes, so set agenda and treasury choices on each of them, the same way on all. Choices set only in a separate purchasing wallet have no effect, and if two voting wallets differ, a ticket votes with whichever wallet's vote is mined. Proposal votes still come from the wallet that holds the commitment keys, usually the purchasing wallet. [Vote without a VSP](../staking/solo-voting.md) covers the setup.

## Check that your vote counted

**Agendas and treasury spends.** Find the vote transaction, then read it on dcrdata.

=== "Decrediton"

    Open **Staking** > **Ticket History**, set the **Ticket Status** filter to **voted** and click a ticket. Follow **Spending Tx** to the vote. It shows **Last Block Valid**, **Vote Version**, **Vote Bits** and **Agenda Choices**, with a warning beside any choice that "doesn't align with what the wallet currently has set". For a VSP ticket, **Fetch VSP Ticket Status** on the ticket's page shows the treasury policies the VSP holds.

=== "Bison Wallet"

    In the **Staking** panel, **Votes cast** counts your voted tickets, and **Tickets** opens your **Ticket History**. Search for a voted ticket's hash on dcrdata and follow the link to the vote that spent it.

=== "Command line"

    ```bash
    dcrctl --wallet ticketinfo
    ```

    Each voted ticket has `"status": "voted"` and the hash of its vote transaction in `vote`. Search for that hash on dcrdata.

On dcrdata, the vote's **Vote Info** section shows **Last Block Valid**, the **Version** and **Bits**, an **Agenda Choices** table and a **Treasury Spend Choices** table; [Use the block explorer](../wallets/block-explorer.md) walks through these pages. Bit 0 approves the previous block, and each agenda has its own higher bits: on `maxtreasuryspend` (version 11), with the previous block approved, `0x0005` is a yes, `0x0003` a no and `0x0001` an abstain. The whitepaper's [vote bits and vote version](../../whitepaper/08-staking.md#sec:staking-votebits) and [treasury vote output](../../whitepaper/12-treasury.md#sec:treasury-vote-output) sections define the exact encoding. A vote on chain is final; if one shows a choice you did not intend, fix the setting for the tickets still to vote.

**Politeia proposals.** Decrediton shows the **Voted** check mark and updates the totals. [proposals.decred.org](https://proposals.decred.org) and [dcrdata's proposals page](https://dcrdata.decred.org/proposals) show each proposal's tally. From the command line, `politeiavoter tally <TOKEN>` shows the count, and after the vote ends `politeiavoter verify <TOKEN>` checks your local records against the server's.

## Troubleshooting

### Decrediton says a VSP "has not upgraded to the minimum version"

Your paid tickets at that VSP will still be voted, but your vote preferences will not be used. Ask the operator to upgrade, and buy future tickets through an up-to-date VSP from the [VSP list on decred.org](https://decred.org/vsp/). A VSP that does not know a new agenda also rejects choices for it.

### Decrediton did not update a VSP you entered by URL

Decrediton finds the VSPs to update through the VSP list on decred.org, so it sends no changes for tickets at a VSP missing from that list, such as one entered by URL or one that has closed. Those tickets vote with the choices sent when their fee was paid.

### `setvotechoice` returns an error after saving

The wallet saves the choice before contacting the VSP, so an error such as a locked wallet, or `VSP client for "<HOST>" not found`, means only the VSP update failed. Unlock the wallet, make sure `vsp.url` and `vsp.pubkey` in `dcrwallet.conf` name the VSP your tickets use ([Stake with dcrwallet](../staking/stake-with-dcrwallet.md)), and run the same command again.

### Bison Wallet saved the choice, but did the VSP get it?

Bison Wallet 1.0.6 does not report a failed VSP update on screen; it writes a warning such as `unable to set vote for vsp` to its log. Check the log after a change, and check votes on dcrdata as your tickets vote.

### No eligible tickets for a proposal

A ticket must have been mined at least 256 blocks before the vote's listed start block, the snapshot. A wallet restored from seed must finish its rescan and see its tickets first. Decrediton also needs the **Politeia** privacy setting turned on.

## Next steps

- [Consensus rule votes](consensus-upgrades.md): how an agenda passes, and how to follow one live.
- [The treasury](treasury.md): how treasury spends are approved and limited.
- [Politeia proposals](politeia.md): how proposals are submitted, discussed and voted on.
- [Stake with Decrediton or Bison Wallet](../staking/stake.md): buy more tickets, with your choices in place first.
- [Write a Politeia proposal](write-a-proposal.md): put your own idea to the ticket holders.

*[VSP]: voting service provider
*[VSPs]: voting service providers
*[TSPEND]: treasury spend
