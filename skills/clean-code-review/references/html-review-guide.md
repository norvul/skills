# HTML Review Guide

Apply this pass to `.html` files, server-rendered templates, CMS fragments, and markup-heavy UI files.

## Structural Correctness

- Check valid nesting and document structure.
- Check duplicate IDs and broken anchor or label targets.
- Check form structure, button types, label-control associations, heading order, and landmark usage.
- Check table, list, and interactive-element semantics.
- Check `doctype`, `lang`, page title, and core metadata when the file owns document structure.

## Accessibility And Semantics

- Prefer native semantic elements over `div` or `span` substitutions.
- Check keyboard usability, focus order, focus visibility, and custom-control accessibility.
- Check alt text, landmark clarity, link text clarity, and placeholder-as-label misuse.
- Check ARIA usage carefully; bad ARIA is a defect, not a nice-to-have.

## Safety And Templating

- Check server-rendered or templated HTML for unsafe interpolation and escaping assumptions.
- Flag inline event handlers unless they are intentionally required by the stack.
- Check iframe usage, external-link safety, and dangerous raw HTML injection boundaries.

## Maintainability

- Remove wrapper-div spam, duplicated fragments, and noisy conditional markup.
- Keep document structure easy to scan and easy to modify.
- Prefer a small number of clear structural patterns over many inconsistent variants.

## SEO Basics

- Check title, description, headings, canonical structure, and crawl-relevant basics when the page is indexable.
- Do not over-index on SEO for pages or fragments that are clearly not indexable surfaces.
