## ADDED Requirements

### Requirement: Language Configuration
- **WHEN** bot starts
- **THEN** MUST read `LANGUAGE` env var (default: `vi`)
- **AND** supported values: `vi`, `en`
- **AND** all user-facing output MUST use the configured language

### Requirement: UI String Translation
- **WHEN** bot sends any user-facing message (help, status, errors, analysis labels)
- **THEN** MUST use translated string via `t(key)` function
- **AND** `t()` MUST fallback to `vi` if key not found in current locale

### Requirement: Prompt Locale
- **WHEN** calling LLM with any prompt
- **THEN** MUST load prompt from `prompts/{LANGUAGE}/` folder
- **AND** MUST fallback to `prompts/vi/` if locale folder/file not found
- **AND** LLM MUST respond in the same language as the prompt

### Requirement: English Prompts
- **WHEN** `LANGUAGE=en`
- **THEN** all 7 prompts MUST be available in English under `prompts/en/`
- **AND** persona names MUST stay the same (Scout, Builder, Debater, Chief)
- **AND** output format MUST match Vietnamese version structure
