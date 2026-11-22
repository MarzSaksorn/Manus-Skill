---
name: react-language-switch
description: Add or improve bilingual and multilingual language switching in existing React web apps. Use when implementing translated UI, a language selector, persisted locale preferences, or document-language and accessibility updates.
---

# React Language Switch

Add a complete language-switching system to an existing React app while preserving its behavior and visual system. Prefer the app's existing localization library and conventions. For a small app with a small fixed language set, a typed message dictionary and a small hook can avoid unnecessary dependencies.

## Workflow

1. **Inspect before editing.** Find the app entry point, shared shell, route structure, localization tools, visible copy, form states, and persisted preferences. Separate interface copy from user-generated/domain data and product names. Preserve route, data, and form contracts.
2. **Choose the smallest architecture.** Reuse an existing i18n library if present. Otherwise, use a typed dictionary keyed by stable source-language messages or semantic keys and one translation function or hook. Keep locale definitions in one module. Avoid scattered language conditionals and unnecessary packages.
3. **Establish locale state.** Define supported locales and a default. Load a stored preference safely, fall back for missing or unsupported values, and persist changes under a stable key. Do not access `localStorage` during server rendering. Keep one source of truth so all screens rerender together.
4. **Update document semantics.** Set `<html lang>` to the active BCP 47 tag (for example, `en` or `th`) whenever the locale changes. Use an effect or the framework's metadata mechanism, not a render-time side effect.
5. **Translate the whole interface.** Cover navigation, headings, actions, filters, form labels and placeholders, help and privacy copy, loading/empty/error states, validation messages, confirmations, success toasts, accessible names, and authentication or modal flows. Include a selector on primary entry screens so users can choose before signing in. Keep proper names, item titles, user-generated content, IDs, and domain values unchanged unless requirements call for content localization.
6. **Handle dynamic copy and locale formats.** Use interpolation or locale-aware formatters instead of concatenating translated fragments. Localize app-generated dates, numbers, and currencies with `Intl.*`. Keep stable option IDs and translate only visible labels; don't make stored values depend on translated text.
7. **Add an accessible selector.** Use native buttons or a native select with visible language names, preferably each name in its own language. Expose selection with `aria-pressed`, `aria-selected`, or native control state. Give icon-only controls an accessible name, preserve visible focus, and support keyboard interaction. Place the selector consistently.
8. **Respect typography and layout.** Check that fonts cover the target script or provide a deliberate fallback. Review text expansion at narrow widths. Preserve design tokens, responsive behavior, and reduced-motion conventions.
9. **Verify behavior.** Run the repository's build and relevant tests. Check default locale, switching both ways, persistence after reload, unsupported stored values, document `lang`, translation-key coverage, forms, filters, dialogs, and success/error messages. Preserve existing user edits. Report browser or production checks that you didn't run.

## Small-app reference pattern

Use the application's existing state conventions. A minimal provider or external-store hook can expose `language`, `setLanguage`, and `t`. Keep the stored preference key stable and guard browser APIs for SSR:

```ts
export type Language = 'en' | 'th';

const messages: Record<Language, Record<string, string>> = {
  en: { 'Search reports': 'Search reports' },
  th: { 'Search reports': 'ค้นหารายงาน' },
};

export function translate(language: Language, key: string) {
  return messages[language][key] ?? messages.en[key] ?? key;
}
```

Persist locale changes and synchronize the document language from an effect. Fall back to the default locale when storage contains an unknown value. For interpolation, use a formatter or typed helper rather than assembling sentences from translated fragments.

A compact selector can use native buttons:

```tsx
<div role="group" aria-label="Language">
  <button type="button" aria-pressed={language === 'en'} onClick={() => setLanguage('en')}>EN</button>
  <button type="button" aria-pressed={language === 'th'} onClick={() => setLanguage('th')}>ไทย</button>
</div>
```

Keep language names understandable independently of the current locale. Add visible focus styling that matches the existing UI.

## Common failure modes

- Translating only the main screen while leaving sign-in, errors, dialogs, or toast feedback in the default language.
- Applying broad text replacements that alter brand names, data values, or JSX attributes.
- Concatenating translated fragments into unnatural word order.
- Translating category/location labels and also changing IDs used for filtering or persistence.
- Reading `localStorage` without an SSR guard or changing `document.documentElement.lang` during render.
- Adding a selector that doesn't persist, update all screens, or expose selected state accessibly.
- Declaring a target language without checking font coverage for its script.
- Assuming a passing build proves translation coverage; inspect visible states and translation-key coverage separately.

## FoundIt implementation notes

The FoundIt implementation used a central TypeScript dictionary and shared translation function, persisted `en`/`th` in local storage, updated the document language, placed the selector in sign-in and app shells, and added Noto Sans Thai alongside the existing fonts. It translated interface labels while retaining report values and IDs. Reuse these decisions only when they fit the target app; prefer its established localization architecture when one exists.
