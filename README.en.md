<img src="docs/icon.png" width="96" align="right" alt="Icon">

# 🛒 Shopping list for Home Assistant

🇩🇪 **Deutsch?** → [README auf Deutsch](README.md)

**The family shopping list right in your dashboard.** Several stores, categories, recipes and live sync on every phone. Every item shows who added it. Bought things get checked off and stay as “bought before”, so next time they are back on with a single tap.

> 🌍 The card was written in German and speaks English whenever your Home Assistant is not set to German (or with `language: en`). On a fresh English install the default stores, categories and recipe groups are English too. Your own entries are never translated. Spot a German leftover? Please open an issue.

![Preview](docs/screenshot.png)

---

## ✨ What can it do?

| Feature | How it works |
|---|---|
| 🏪 **Several stores** | Each store gets its own tab. When your location says you're at a store, the list jumps there. |
| 🗂️ **Categories** | Fruit & vegetables, frozen … The list guesses the category itself (“yogurt” → dairy). |
| 👨‍👩‍👧‍👦 **For the whole family** | Everyone with an HA user can join, no admin rights needed. Live on every phone. |
| ♻️ **Nothing gets lost** | Checked items move down to “Done”. Tap the circle again = back on the list. |
| 🏷️ **For whom & who** | *Cheese (for Grandma)* – and in small print who added it. |
| ⚡ **Quick entry** | “3 milk”, “500 g flour” or “milk, 6 eggs, bread” at once. Suggestions bring back everything from last time. |
| 🍽️ **Recipes** | Ingredients onto the list with one tap, scaled for x people. Cook mode, photos, sharing and import (links and US measures too). |
| 🔍 **Barcodes** | Scan in the HA app or with the phone camera in the offline app: add at home, check off in the store. |
| 🔁 **“Was out!”** | ⇄ on the item: here again next time, or move it to another store. The list notices what's often missing. |
| 🛒 **Shop mode** | Big rows, checking off only – one hand on the cart. |
| 📱 **Offline app** | The complete card as a phone app that opens without a connection. Changes are sent later. |
| ⏲️ **Cooking times** | Cheat sheet by appliance: 🍲 stove, 🔥 oven, 💨 air fryer. |
| 🧹 **Cleanup** | Once a week old items get **checked off**, nothing is deleted. |
| 🔒 **PIN** | Settings (the gear) only with a PIN – the list stays open for everyone. |

Plus lots of small things: photos per product, nicknames (“Kleenex” = tissues), learned typos, store brands when scanning, duplicate finder, history, backup, a mascot 🛒😊 and more.

**🗣️ With Alexa:** “Alexa, add milk to my shopping list” – and the milk lands on *this* list (see [Alexa & other lists](#-alexa--other-lists)).

---

## 📦 Installation

1. Open **HACS** → top right **⋮ → Custom repositories**.
2. Add `https://github.com/misterm2310/einkaufslisten-card`, type **Integration**.
3. Search for **Einkaufsliste**, **Download**, **restart Home Assistant**.
4. **Settings → Devices & services → Add integration → Einkaufsliste**, pick the cleanup day and time, done. 🎉
5. Dashboard → **Edit → Add card → Einkaufsliste**.

```yaml
type: custom:einkaufsliste-card
```

> 🙌 No need to add a resource by hand – the integration does it.
> Card looks odd after an update? Pull down to refresh in the app or press Ctrl+F5 in the browser.

<details><summary>Without HACS (manually)</summary>

Copy `custom_components/einkaufsliste` to `/config/custom_components/einkaufsliste` and restart Home Assistant.
</details>

---

## 👆 How to use it

**Adding:** type a name, tap the green ✔. The buttons below: 🔢 quantity · 📝 note · 👤 for whom · 📷 photo · 🧽 clear. Store and category are usually picked correctly already. A store is missing? Pick **“➕ New store …”** in the list – just type the name, the rest later in ⚙️.

**In the list:**
- ⭕ **Circle** = check off. Under “Done” once more = back on the list.
- ⇄ = was out (stays open marked “was out”, or moves to another store).
- **Long-press** = menu: edit, move, quantity, category, photo, barcode, info.
- **Tap the quantity** = [−] 2x [＋].
- ✨ = new since you last looked; the red number on a tab shows how much is new there.
- The **shopping cart** at the top left opens a guide for the whole family – including the app link to copy.

**In the store:** the cart at the top right switches on **shop mode**. No connection? Keep checking off, the dot turns orange ⏳ and everything is sent later.

**Recipes:** create them in ⚙️ → Recipes (ingredients just like on the list, or paste an ingredient list or a recipe link). The **chef's hat** at the top: **Add to list** → tick what's missing → done. Also 👥 people or 🍕 trays scaling, **🔥 Cook** (step by step), **Share** (e.g. WhatsApp) and **⏲️ cooking times**. Checked recipe ingredients disappear completely.

---

## 🔍 Scanning barcodes

The ▥ button at the top knows where you are:
- 🏠 **At home:** scan a pack → name, brand and category are filled in → ✔. With **“📦 Scan several”** every pack goes straight onto the list. Unknown ones are added as “❓ Unknown” – rename once and the list knows the barcode.
- 🛒 **In the store** (store with a 📍 zone): every scanned pack is checked off on the list.

**Where does it work?**
- In the **Home Assistant app** (Android/iPhone) with its scanner – works over `http://` too.
- In the **offline app** with the phone camera. The first time, the phone asks whether the page may use the camera. Without a connection it only recognizes barcodes the list already knows; adding and checking off still work (sent later).
- No scanner in a desktop browser.

Product names come from **Open Food Facts**, **Open Beauty Facts** and **Open Products Facts** (Home Assistant needs internet for that). German store brands such as Milsani, ja! or Balea go straight to the right store; add your own per store in ⚙️ → Stores.

---

## 📱 Offline app

The **complete card** as its own app on your home screen – with recipes, cook mode, cooking times, settings and camera scanner. It opens **without a connection** with the last state.

1. Copy the address: in **⚙️ → App & look → Offline app** or in the **guide** (shopping cart at the top left) – so everyone without the gear can get it too.
2. Paste it into the phone's **browser** (Chrome or Safari, not the HA app).
3. Log in with your own Home Assistant user.
4. Browser menu → **“Add to Home screen”**.

**↩️ Back button:** goes back step by step inside the app (closes windows, one level up in the settings, ends shop mode). Only on the plain list does the app close.

**📱 Quick menu (Android):** long-press the app icon → ✍️ Add · 🛍️ Shop mode · 📷 Scan – the app opens right at that spot. (iPhones don't offer this for web apps.)

**Needs a connection:** looking up new barcodes, product info, recipe links, new photos, backup.

**🔄 Sending while the app is closed:** on **Android with Chrome** the app sends remembered changes even when it's closed – Android wakes it up briefly once there's a connection again (Android decides exactly when; with strict battery saving it can take a while). **iPhones** can't do this; there it's sent the next time you open the app. Each app has its own queue: what the offline app remembered is only sent by the offline app.

Good to know: it needs an **https** address (e.g. Nabu Casa). If two people change the same thing at once, the last change wins. iPhones sometimes clear a web app's offline storage after weeks without use – just open it once with a connection.

---

## ⚙️ Settings (gear)

| Tile | What's inside |
|---|---|
| 🏪 **Stores** | Every store as its own tile. Tap = name, color, icon, order, 📍 zones (several, e.g. for several branches) and 🏷️ store brands. Without an icon of its own the list uses the zone's icon (if it has one), otherwise 🛒. |
| 🗂️ **Categories** · 👥 **People** | Add, rename, color, icon (just type “dog”, no “mdi:”), sort. |
| 👨‍🍳 **Recipes** | Two tabs: **Recipes** (new, edit, delete) and **Recipe groups**. |
| 📦 **Products** | Everything the list knows: rename, category, store (“Available at”), nicknames, photos, barcodes, learned typos, delete completely. Plus “Newly scanned” to check. |
| 🧰 **Tools** | **All good?** (finds broken entries, fixes only what you tick) · **Import & backup** (recipes from a file, lists from other apps – once or 🔁 automatically –, backup as .zip; file import and backup for admins) · **History** (who did what and when, “📈 Often not available”) · **Cleanup** |
| 📱 **App & look** | **Offline app** (your address with a copy button) · **Mascot** 🛒😊 (the switch applies to everyone) · **Protection** (4–8 digit PIN for the gear; forgot it? Devices & services → Einkaufsliste → Configure → “Reset PIN”, admins – honestly: protection against accidental changes, not a safe) |

### 🧹 Cleanup, simply explained
On cleanup day everything that has been open for at least 7 days (adjustable) gets **checked off**. Example Sunday: added on Tuesday → only 5 days old on the first Sunday, stays → checked off on the second Sunday. Each item shows 🧹 with its date. Nothing is deleted. Day and time: **Devices & services → Einkaufsliste → Configure**.

### 📍 Nearest store first
Create a **zone** per store (Settings → Areas, labels & zones → Zones) and pick it in ⚙️ → Stores → tap the store → 📍. Several branches? Just pick several zones for the same store. Whoever shares their location via the companion app lands on the right tab in the store.

### 🗣️ Alexa & other lists
The shopping list can **empty another Home Assistant to-do list automatically**: everything that lands there moves over right away and is deleted there.

1. Set up the **“Alexa Devices”** integration in Home Assistant. The Alexa shopping list then shows up as a to-do list in HA.
2. In the card: **⚙️ → Tools → Import & backup → From other apps → 🔁 Bring over automatically**, pick the Alexa list (and a store if you like), **Turn on**.
3. From now on: “Alexa, add milk to my shopping list” → milk is on the list, with “🔁 Alexa” as the one who added it.

This works with any to-do list in HA (Google Tasks, Bring!, Todoist, the HA shopping list …). Honestly: “Hey Google, …” writes to Google Keep, which has no official Home Assistant connection – so it doesn't work that way with Google.

### 📧 Onto the list by email
1. Create a **separate email address** just for the shopping list and set up the **“IMAP”** integration in Home Assistant with it.
2. In the card: **⚙️ → Tools → Import & backup → 📧 Email**: pick the mailbox, a store if you like, what happens to the email afterwards (📬 leave · 👁️ mark as read · 🗑️ delete), enter the **allowed senders** (at least one), **Turn on**.
3. Send an email to that address – **one item per line** (“milk”, “6 eggs” …). Quotes, signatures and “Sent from my iPhone” are skipped, quantities are recognized. The history shows 📧.
4. **Send the store along:** a store in the **subject** (“Aldi”, “Shopping at Aldi”) puts everything there. Or use a **heading** in the email: `Aldi:` – the things below – then `DM:` … Unknown names go to the chosen store.

Honestly: senders can be faked – so use an address that isn't public. Depending on the mailbox it takes a few seconds to minutes until an email arrives. Only emails that actually put something on the list are marked as read or deleted – others stay. With Gmail, “delete” may mean “archive” depending on your settings.

---

## 🎛️ Card options

| Option | Default | What it does |
|---|---|---|
| `store` | `all` | `all` = all stores with tabs, or one store only |
| `show_title` | `true` | `false` hides the cart icon (guide) at the top |
| `show_added_by` | `true` | show who added an item |
| `added_by_style` | `name` | `name`, `first` or `initials` |
| `show_checked` | `true` | show the “Done” section |
| `show_dates` | `true` | show “since Tue” and the 🧹 date |
| `show_recipes` | `true` | show the chef's hat |
| `show_settings` | `true` | show the gear (e.g. off for a kids' tablet) |
| `compact` | `false` | smaller rows without extra info |
| `auto_store` | `true` | jump to the store you are at |
| `language` | `auto` | `auto` = like Home Assistant, `de` or `en` |

---

## 🤖 For automations

| Entity | What it shows |
|---|---|
| `sensor.einkaufsliste_offene_artikel` | all open items (attributes per store, items, checked, next cleanup) |
| `sensor.einkaufsliste_<store>` | one sensor **per store**: open items there, attribute `artikel` |
| `binary_sensor.einkaufsliste_etwas_zu_kaufen` (English HA: `…_something_to_buy`) | on as soon as anything is open |
| `sensor.einkaufsliste_zuletzt_eingetragen` (English HA: `…_last_added`) | last added item with `von` (who), `wann` (when), `geschaeft` (store) |

| Action | What happens |
|---|---|
| `einkaufsliste.add_item` | puts an item on the list (`name`, optional `store`, `category`, `quantity`, `note`, `for_whom`, `added_by`) |
| `einkaufsliste.add_recipe` | puts all ingredients of a recipe on the list (`name`) |
| `einkaufsliste.check_item` | checks an item off (`name`, optional `store`) |
| `einkaufsliste.remove_item` | deletes an item (`name`, optional `store`) |
| `einkaufsliste.cleanup` | cleans up now; `force: true` checks off everything |

Events: `einkaufsliste_item_added`, `einkaufsliste_cleanup`.

## ❓ FAQ

**Where is the data stored?** Locally in Home Assistant (`/config/.storage/einkaufsliste.data`, photos in `/config/einkaufsliste_fotos`). No cloud. Your HA backups include it; ⚙️ → Tools → Import & backup gives you an extra .zip.

**Why are my categories German?** The integration was set up while Home Assistant was in German. Just rename them in ⚙️ → Categories – the guessing works by keywords in the category name (e.g. “Dairy”, “Frozen”, “Drinks”).

---

License: MIT · Product data: [Open Food Facts](https://world.openfoodfacts.org) (ODbL) · Offline app icons: [Material Design Icons](https://pictogrammers.com) (Apache 2.0) · Offline app barcode reader: [ZXing-js](https://github.com/zxing-js/library) (Apache 2.0)
