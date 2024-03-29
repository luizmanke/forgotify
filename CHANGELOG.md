## Unreleased

### Fix

- Add scrape tracks build to CD (#86)

## v0.2.1-rc1 (2023-04-23)

### Fix

- Add CD dependencies (#84)

## v0.2.0-rc1 (2023-04-23)

### Feat

- Create scrape tracks project (#82)
- Create scrape artists function (#75)
- Create cron job for the scrape trigger function (#71)
- Publish trigger messages to topic (#70)
- Create scrape-artist topic (#69)
- Deploy scrape trigger (#65)
- Create scrape trigger project (#64)
- Remove database batch update and pipelines (#63)
- Create media-tools get playlists method (#53)

### Fix

- Functions flow (#81)
- Search result with NoneType items (#51)

### Refactor

- Scrape tracks files (#83)
- Create queue tool (#80)
- Change infra project structure (#79)
- Replace SNS with SQS (#77)
- Create storage tool (#76)
- Scrape trigger (#73)

## v0.1.0-rc1 (2022-12-18)

### Feat

- Add media-tools backoff (#45)
- Search and save tracks (#37)
- Create system test (#35)
- Create continuous deployment (#34)
- Create batch database update pipeline (#26)
- Create medias database (#18)
- Create artists update (#8)
- Create media tools (#2)
- Create database tools (#3)

### Fix

- CD tag pattern (#47)

### Refactor

- Split batch-database-update functions (#44)
- Update media tools provider (#32)

### Perf

- Reduce database storage memory (#43)
