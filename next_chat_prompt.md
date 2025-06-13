# Next Chat Prompt

I am working on a project to modify how participant information is handled in a Fathom API scraping system. The current implementation needs to be updated to handle a new participant structure, but this must be done with extreme caution.

## Current Context
- We have a working system that scrapes meeting data from Fathom API
- The system currently handles participants as a simple list of names
- We need to update it to handle a more detailed participant structure
- The existing code must NOT be broken under any circumstances

## New Participant Structure
```json
{
  "participants": [
    {
      "participant_id": "",
      "name": "Full Name",
      "is_host": true
    },
    {
      "participant_id": "",
      "name": "Guest Name",
      "is_host": false
    }
  ]
}
```

## Critical Rules
1. NEVER delete or modify existing files without explicit permission
2. ALWAYS create new files with a `_v2` suffix instead of modifying existing ones
3. NEVER remove old code - only add new code alongside it
4. ALWAYS create backups before making any changes
5. ASK FOR PERMISSION before proceeding to each phase

## Implementation Plan
We are following a phased approach:

### Phase 1: Testing Infrastructure
- Create `test_participants_v2.py` with test cases
- Run tests against existing code
- Document results in `test_results_v1.md`

### Phase 2: New Structure Implementation
- Create `scrape_v2.py` with new parsing method
- Keep original method untouched
- Add extensive logging
- Document validation results

### Phase 3: Export Integration
- Create `export_v2.py` with new frontmatter generation
- Keep original method untouched
- Add compatibility layer
- Document test results

### Phase 4: Validation
- Run full pipeline on sample meetings
- Document results and comparisons
- Verify no breakage

### Phase 5: Clean Up
- Only after explicit approval
- Create final versions
- Update documentation
- Remove temporary files

## Important Reminders
1. NEVER delete or modify existing files
2. ALWAYS create new files with `_v2` suffix
3. ALWAYS ask for permission before proceeding
4. ALWAYS document every change
5. ALWAYS create backups
6. NEVER remove old code
7. NEVER proceed without explicit permission

## Current State
- We have analyzed the API response structure
- We have documented the current implementation
- We have created a detailed implementation plan
- We are ready to begin Phase 1

## Next Steps
1. Confirm you understand the context and rules
2. Begin with Phase 1 after getting explicit permission
3. Document each step thoroughly
4. Ask for permission before proceeding to each phase

Please confirm you understand these instructions and rules before proceeding with any implementation steps. 