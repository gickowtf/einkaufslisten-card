<img src="docs/icon.png" width="96" align="right" alt="Icon">

# 🛒 Shopping list for Home Assistant

🇩🇪 **Deutsch?** → [README auf Deutsch](README.md)

**The family shopping list right in your dashboard.** Several stores, categories, recipes and live sync on every phone. Every item shows who added it. Bought things get checked off and stay in the list as “bought before”, so next time they are back on with a single tap.

> 🌍 The card was written in German and speaks English whenever your Home Assistant is not set to German (or when you set `language: en`). The integration's setup dialogs, services and – on a fresh English install – the default stores, categories and recipe groups are English too. Your own entries (items, notes, recipes) are never translated. Some rarely seen texts may still show up in German – please open an issue if you spot one.

![Preview](docs/screenshot.png)

---

## ✨ What can it do?

| Feature | How it works |
|---|---|
| 🏪 **Several stores** | Each store gets its own tab at the top. Add, rename, color and sort them in ⚙️. |
| 🗂️ **Categories** | Fruit & vegetables, bakery, frozen and so on. Open **and** done items are grouped by category. |
| 👨‍👩‍👧‍👦 **For the whole family** | Everyone who can log in to Home Assistant can join – no admin rights needed. |
| ⭕ **Check off with the circle** | Only the circle checks an item off, so no accidental taps. |
| ♻️ **Nothing gets lost** | Checked items move to “Done – bought before”. Tap the circle again and it's back on the list. |
| 🏷️ **For whom & who** | “Cheese (for Grandma)” – and in small print who added it. |
| 🚫 **No duplicates** | Each item is on the list once. A second one needs a different note, “for whom” or store. |
| 🍽️ **Recipes** | Save a recipe with all ingredients. **Add to list**, tick what you need, done. With servings, oven settings, cook mode and sharing. |
| 🧹 **Automatic cleanup** | Once a week everything that has been on the list for 7+ days gets **checked off**. **Nothing is deleted.** |
| ⚡ **Live sync** | When someone adds something, it shows up on every phone right away. |
| 📸 **Photos** | Up to 6 photos per product (“exactly this brand!”). |
| 🔍 **Barcodes** | Scan in the Home Assistant app: at home to **add**, in the store to **check off**. |
| 📖 **Guesses the category** | “Milk” goes to dairy, “frozen pizza” to frozen – there's a built-in dictionary (German and English). |
| 🔁 **“Was out!”** | Store didn't have it? Tap **⇄**: keep it open for next time (everyone sees “⇄ was out”) or move it to another store. |
| 📍 **Nearest store** | When you are at a store (HA zone), the list jumps to its tab. |
| 🛒 **Shop mode** | Big rows, big circles, no input field – just check things off with one hand. |
| 🏷️ **Nicknames** | “Kleenex” means tissues: give a product nicknames and whoever types one lands on the right product. |
| 📥 **Import & backup** | Import recipes from a file, bring lists over from Bring!, Google Keep or the HA shopping list, download everything as a backup (.zip). |
| ⚖️ **Converts US measures** | Imported recipes: “1 cup flour” → “125 g flour”, “2 tbsp” → “2 EL” (tbsp), “350 °F” → “175 °C”. |

---

## 📦 Installation

### Step 1: Add it to HACS
1. Open **HACS**.
2. Top right **⋮ → Custom repositories**.
3. Repository `https://github.com/misterm2310/einkaufslisten-card`, type **Integration**, **Add**.
4. Search for **Einkaufsliste**, **Download**, then **restart Home Assistant**.

<details>
<summary>Without HACS (manually)</summary>

Copy the folder `custom_components/einkaufsliste` to `/config/custom_components/einkaufsliste` and restart Home Assistant.
</details>

### Step 2: Set up the integration
**Settings → Devices & services → Add integration → Einkaufsliste**, pick the cleanup day, time and minimum age, **Submit**. Done! 🎉

### Step 3: Card on the dashboard
Dashboard → **Edit → Add card → Einkaufsliste**. Or in YAML:

```yaml
type: custom:einkaufsliste-card
```

> 🙌 You don't have to add a resource by hand – the integration registers the card itself and keeps it up to date.
> Card looks odd after an update? Pull down to refresh in the app or clear the browser cache (Ctrl+F5).

---

## ✍️ Adding items

- Type a name, e.g. **milk**, then tap ✔. Up to 2 suggestions appear while typing; tapping one takes over quantity, note, for whom and store from last time.
- Quantities work directly: **3 milk**, **500 g flour**, **tomatoes 2 cans**. English units (tbsp, tsp, cans, bottles, jars, cloves, cups …) are understood.
- **Several at once:** `milk, 6 eggs, bread` → ✔ → 3 things on the list.
- The buttons below: 🔢 quantity · 📝 note · 👤 for whom · 📷 photo · 🧽 clear.
- Below that: **Which store?** (or “Anywhere”) and the **category**, usually preselected correctly.
- Typing a person's name shows what's on the list for them. Typos get a “Did you mean …?”.

## 👆 Using the list

- **Long-press** an item: edit, move, quantity, category, photo, barcode, info.
- Tap the quantity to change it with − / ＋.
- ⇄ = was out (see above).

## 🍽️ Recipes

- ⚙️ → **Recipes → New recipe**. Add ingredients exactly like on the list. **Paste recipe** accepts an ingredient list or a recipe link.
- Servings (people or trays), recipe groups, oven settings, instructions, up to 6 photos.
- The **chef's hat** at the top: **Add to list** → tick what you need → done. **Off the list (3)** takes them off again. **🔥 Cook** = step by step in large print. **Share** = as text, e.g. via WhatsApp.
- 🧂 **Staples** (salt, oil …) are not preselected.

## ⚙️ Settings (gear)

Tiles: **Stores · Categories · Recipes · Recipe groups · People · Products · All good? · Import & backup · History · Cleanup**.

- **Products:** all products the list knows – rename, category, default store, unit, nicknames, barcodes, photos, delete completely.
- **All good?** finds broken or incomplete entries (no category, no store, missing photos …), lists each one and fixes only what you tick.
- **Import & backup:**
  - **Recipes from file** (admins): `.txt/.md` (each recipe starts with `# Name`, then “Ingredients” and “Instructions”), `.csv` (columns `recipe;quantity;unit;ingredient;note;instructions`) or `.json`.
  - **From other apps:** pick any Home Assistant to-do list and bring its items over, or paste a list shared from Bring!, Google Keep & co. (one item per line; checked ones stay out).
  - **Backup** (admins): download everything as a .zip, or restore one (replaces everything after a confirmation).
- **History:** who did what, when and how – with filters.

## ⚙️ Card options

| Option | Default | What it does |
|---|---|---|
| `language` | `auto` | `auto` = like Home Assistant (German, otherwise English), `de`, `en` |
| `show_title` | `true` | `false` hides the cart icon (guide) at the top |
| `store` | `all` | `all` = all stores with tabs, or one store only |
| `show_added_by` | `true` | show who added an item |
| `added_by_style` | `name` | `name`, `first` or `initials` |
| `show_checked` | `true` | show the “Done” section |
| `show_dates` | `true` | show “since Tue” and the 🧹 date |
| `show_recipes` | `true` | show the chef's hat button |
| `compact` | `false` | smaller rows without extra info |
| `auto_store` | `true` | jump to the store you are at |
| `show_settings` | `true` | show the gear (e.g. off for a kids' tablet) |

## 🤖 For automations

Sensor `sensor.einkaufsliste_offene_artikel` (open items; attributes per store, items, checked, next cleanup).

| Action | What happens |
|---|---|
| `einkaufsliste.add_item` | puts an item on the list (`name`, optional `store`, `category`, `quantity`, `note`, `for_whom`, `added_by`) |
| `einkaufsliste.add_recipe` | puts all ingredients of a recipe on the list (`name`) |
| `einkaufsliste.check_item` | checks an item off (`name`, optional `store`) |
| `einkaufsliste.remove_item` | deletes an item (`name`, optional `store`) |
| `einkaufsliste.cleanup` | cleans up now; `force: true` checks off everything |

Events: `einkaufsliste_item_added`, `einkaufsliste_cleanup`.

## ❓ FAQ

**Where is the data stored?** Locally in Home Assistant (`/config/.storage/einkaufsliste.data`) – no cloud. Your HA backups include it; ⚙️ → Import & backup gives you an extra .zip.

**Why are my categories German?** The integration was set up while Home Assistant was in German. Just rename them in ⚙️ → Categories – the category guessing works by keywords in the category name (e.g. “Dairy”, “Frozen”, “Drinks”).

---

License: MIT · Product data: [Open Food Facts](https://world.openfoodfacts.org) (ODbL)
