# Implementation Plan: Safe Migration to New Participants Structure

## CRITICAL RULES FOR THE ASSISTANT

1. **NEVER DELETE OR MODIFY EXISTING FILES** without explicit permission
2. **ALWAYS CREATE NEW FILES** with a `_v2` suffix instead of modifying existing ones
3. **NEVER REMOVE OLD CODE** - only add new code alongside it
4. **ALWAYS CREATE BACKUPS** before making any changes
5. **ASK FOR PERMISSION** before proceeding to each phase

## Pre-Implementation Checks

1. **Create Backup Files**
   - Create `scrape_v2.py` as a copy of `scrape.py`
   - Create `export_v2.py` as a copy of `export.py`
   - Create `test_participants_v2.py` as a new file
   - Create `processed_urls_v2.json` as a copy of `processed_urls.json`

2. **Document Current State**
   - Create `current_state.md` documenting:
     - Current participant structure
     - All files that use participant data
     - Current test coverage

## Implementation Steps

### Phase 1: Testing Infrastructure
**DO NOT PROCEED WITHOUT PERMISSION**

1. Create `test_participants_v2.py` with test cases for:
   - Host only
   - Host + guest
   - Missing names
   - Edge cases (nulls, empty strings)

2. Run tests against existing code to establish baseline
   - Document all test results in `test_results_v1.md`

### Phase 2: New Structure Implementation
**DO NOT PROCEED WITHOUT PERMISSION**

1. In `scrape_v2.py`:
   - Add new `_parse_meeting_data_from_api_v2` method
   - Keep original method untouched
   - Add extensive logging
   - Add validation checks

2. Create `validation_results_v2.md` to document:
   - All validation checks
   - Expected vs actual results
   - Any warnings or errors

### Phase 3: Export Integration
**DO NOT PROCEED WITHOUT PERMISSION**

1. In `export_v2.py`:
   - Add new `generate_frontmatter_v2` method
   - Keep original method untouched
   - Add compatibility layer for old format

2. Create `export_test_results_v3.md` documenting:
   - Sample outputs
   - Format comparisons
   - Any compatibility issues

### Phase 4: Validation
**DO NOT PROCEED WITHOUT PERMISSION**

1. Run full pipeline on 1-3 meetings
2. Create `validation_results_v4.md` with:
   - Sample outputs
   - Comparison with original format
   - Any discrepancies

### Phase 5: Clean Up
**DO NOT PROCEED WITHOUT PERMISSION**

1. Only after explicit approval:
   - Create final versions of files
   - Update documentation
   - Remove temporary files

## Safety Measures

For EVERY change:
1. Create a new file instead of modifying existing ones
2. Document the change in a corresponding markdown file
3. Run tests and document results
4. Ask for permission before proceeding

## Emergency Procedures

If ANYTHING breaks:
1. STOP immediately
2. Document the issue in `error_log.md`
3. DO NOT attempt to fix without permission
4. Wait for explicit instructions

## Success Metrics

Must Have:
- All original files remain untouched
- All new code in separate files
- All changes documented
- All tests passing
- No breakage of existing functionality

## Documentation Updates

Create new files:
- `README_v2.md` for new structure
- `notes_v2.md` for migration details
- `test_docs_v2.md` for test documentation

## IMPORTANT REMINDERS

1. NEVER delete or modify existing files
2. ALWAYS create new files with `_v2` suffix
3. ALWAYS ask for permission before proceeding
4. ALWAYS document every change
5. ALWAYS create backups
6. NEVER remove old code
7. NEVER proceed without explicit permission

**DO NOT PROCEED TO ANY PHASE WITHOUT EXPLICIT PERMISSION**

# Validation Results for scrape_v3.py

**Test:** `test_scrape_v3_participants.py`  
**Date:** 2025-06-13

## Purpose
To confirm that the new participant structure (without `participant_id`) is correctly parsed and validated.

## Test Output
```json
[
  {
    "name": "João Landeiro",
    "is_host": true
  },
  {
    "name": "Dave Gray",
    "is_host": false
  }
]
```

## Result
- ✅ No `participant_id` present in any participant.
- ✅ Correct host/guest distinction.
- ✅ Names are correctly parsed.
- ✅ No errors or warnings during parsing.

## Notes
- The new structure is now the recommended format for downstream processing.
- See `scrape_v3.py` for implementation details and comments.

## Summary of Participant Structure Migration (v3)

- The `participant_id` field was removed from the participant structure in `scrape_v3.py`.
- This change was made to simplify the data model and because unique IDs will be generated elsewhere in the pipeline.
- All related parsing and validation logic was updated.
- The new structure has been tested and validated (see `validation_results_v3.md`).
- For any new features or bugfixes, use `scrape_v3.py` as the base.