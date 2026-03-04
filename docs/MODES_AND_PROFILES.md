# Modes and Profiles

## Corpus modes

### `support_kb`
Best for operational and support documentation.
Typical structure:
- concise pages
- headings and bullet steps
- policy/procedure language

Desired retrieval behavior:
- high precision on concrete steps and exact sections
- strong use of heading metadata

### `academic_pdf`
Best for research papers and long technical documents.
Typical structure:
- long narrative sections
- dense argument chains
- page and section context matters

Desired retrieval behavior:
- keep enough context to preserve argument continuity
- retain section/page references for citation quality

## Chunking profiles

### `fine`
- Smaller chunks
- Higher precision, lower context continuity
- Useful for pinpoint support instructions

### `balanced`
- Moderate chunk size
- Compromise between precision and context
- Default candidate for mixed workloads

### `coarse`
- Larger chunks
- Better context continuity, lower pinpoint precision
- Useful for long-form academic reasoning

## Why chunking differs by corpus type
Corpus shape changes what "good evidence" looks like:
- Support docs usually reward precise, local snippets
- Academic texts often require broader neighboring context to avoid misinterpretation

Therefore, profile choice should be interpreted through mode defaults, not as one-size-fits-all settings.
