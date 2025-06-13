# Fathom API Investigation Notes

## API Response Structure Investigation
Date: 2024-03-27

### Host Information Structure
The API response from `/calls/previous` endpoint contains detailed host information in the following structure:

```json
"host": {
    "id": 783668,
    "avatar_url": "https://lh3.googleusercontent.com/a/...",
    "email": "contact@joaolandeiro.com",
    "first_name": "João",
    "last_name": "Landeiro",
    "teamUserViewUrl": null
}
```

### Current Implementation vs API Data
- **Current Implementation**: Only uses `host.get('first_name', '')` in `_parse_meeting_data_from_api`
- **Available Data**: Full name information (first_name + last_name) and email
- **Location**: This data is available in the API response from the `/calls/previous` endpoint

### Additional API Findings

#### Contact Information
```json
"contact": {
    "name": "Dave Gray"
}
```
- Contains participant name information
- Could be used to enhance participant tracking

#### Company Information
```json
"company": {
    "domain": "hiredthought.com",
    "name": "Hired Thought",
    "icon_url": "https://static.fathom.video/...",
    "teamCompanyViewUrl": null
}
```
- Contains company domain and name
- Includes company icon URL
- Could be used for organization tracking

#### Recording Details
```json
"recording": {
    "created_at": "2025-06-11T19:59:02.998561Z",
    "started_at": "2025-06-11T20:00:09.043768Z",
    "duration_seconds": 3122.364333
}
```
- Precise timestamps for creation and start
- Exact duration in seconds
- More accurate than current duration_minutes field

#### Meeting Metadata
- `hostTalkTime`: Percentage of meeting time host was speaking
- `is_impromptu`: Boolean indicating if meeting was scheduled
- `highlight_count`: Number of highlights in the meeting
- `permalink`: Direct URL to the meeting
- `universalShareable`: Contains share URL and access settings

### Recommended Changes
1. Modify `_parse_meeting_data_from_api` to capture full host name
2. Consider storing host email for reference
3. Update metadata structure to include complete host information
4. Add company information to metadata
5. Use precise recording timestamps instead of rounded minutes
6. Include host talk time percentage
7. Add meeting type (impromptu vs scheduled)

### API Response Context
- Endpoint: `/calls/previous`
- Response Type: JSON
- Contains array of meeting items
- Each meeting item includes host information
- Host information is consistent across all meeting entries

### Verification Method
This information was obtained using the `diagnostics.py` script which:
1. Intercepts API responses
2. Logs response data to `diagnostics.log`
3. Saves raw JSON responses to timestamped files

### Next Steps
1. Update host name extraction logic
2. Consider adding host email to metadata
3. Update documentation to reflect new host information structure
4. Test changes with existing meeting data
5. Implement company information tracking
6. Update duration handling to use precise timestamps
7. Add new metadata fields (host talk time, meeting type) 