# Job Management

This guide covers job management operations including listing, monitoring, and managing Dremio query jobs.

## Commands

### List Jobs

List recent jobs.

```bash
alt-dremio-cli job list [OPTIONS]
```

**Options:**
- `--max-results INTEGER` - Maximum number of results to return
- `--filter TEXT` - Filter expression (e.g., `state=COMPLETED`)
- `--sort TEXT` - Sort field (prefix with `-` for descending, e.g., `-submittedAt`)

**Examples:**

```bash
# List recent jobs
alt-dremio-cli job list

# List last 50 jobs
alt-dremio-cli job list --max-results 50

# List only completed jobs
alt-dremio-cli job list --filter "state=COMPLETED"

# List jobs sorted by submission time (newest first)
alt-dremio-cli job list --sort "-submittedAt"

# Combine filters and sorting
alt-dremio-cli job list --max-results 20 --filter "state=RUNNING" --sort "-submittedAt"
```

### Get Job Details

Retrieve detailed information about a specific job.

```bash
alt-dremio-cli job get <JOB_ID>
```

**Arguments:**
- `JOB_ID` - The job ID (UUID)

**Examples:**

```bash
# Get job details
alt-dremio-cli job get 16b2c9cd-a920-952b-b162-2280c9059d00

# Get job details in JSON
alt-dremio-cli --output json job get 16b2c9cd-a920-952b-b162-2280c9059d00

# Get job details with verbose output
alt-dremio-cli --verbose job get 16b2c9cd-a920-952b-b162-2280c9059d00
```

### Analyze Job

Analyze the performance of a job to identify bottlenecks.

```bash
alt-dremio-cli job analyze <JOB_ID>
```

**Output:**
- Job duration and state
- Data reduction ratio (input vs output records)
- Insights on performance metrics

### Get Job Results

Retrieve the results of a completed job.

```bash
alt-dremio-cli job results <JOB_ID> [OPTIONS]
```

**Arguments:**
- `JOB_ID` - The job ID (UUID)

**Options:**
- `--limit INTEGER` - Maximum number of rows to return
- `--offset INTEGER` - Offset for pagination

**Examples:**

```bash
# Get job results
alt-dremio-cli job results 16b2c9cd-a920-952b-b162-2280c9059d00

# Get first 100 rows
alt-dremio-cli job results 16b2c9cd-a920-952b-b162-2280c9059d00 --limit 100

# Get next 100 rows (pagination)
alt-dremio-cli job results 16b2c9cd-a920-952b-b162-2280c9059d00 --limit 100 --offset 100

# Export results to JSON
alt-dremio-cli --output json job results 16b2c9cd-a920-952b-b162-2280c9059d00 > results.json
```

### Cancel Job

Cancel a running job.

```bash
alt-dremio-cli job cancel <JOB_ID>
```

**Arguments:**
- `JOB_ID` - The job ID (UUID)

**Examples:**

```bash
# Cancel a running job
alt-dremio-cli job cancel 16b2c9cd-a920-952b-b162-2280c9059d00

# Cancel without confirmation prompt
alt-dremio-cli job cancel 16b2c9cd-a920-952b-b162-2280c9059d00 --yes
```

### Get Job Profile

Download job profile for performance analysis.

```bash
alt-dremio-cli job profile <JOB_ID> [OPTIONS]
```

**Arguments:**
- `JOB_ID` - The job ID (UUID)

**Options:**
- `--download PATH` - Download profile to file

**Examples:**

```bash
# View job profile
alt-dremio-cli job profile 16b2c9cd-a920-952b-b162-2280c9059d00

# Download profile to file
alt-dremio-cli job profile 16b2c9cd-a920-952b-b162-2280c9059d00 --download profile.zip
```

### Get Job Reflections

Get reflection information for a job.

```bash
alt-dremio-cli job reflections <JOB_ID>
```

**Arguments:**
- `JOB_ID` - The job ID (UUID)

**Examples:**

```bash
# Get reflection info
alt-dremio-cli job reflections 16b2c9cd-a920-952b-b162-2280c9059d00

# Get in JSON format
alt-dremio-cli --output json job reflections 16b2c9cd-a920-952b-b162-2280c9059d00
```

## Scenarios

### Monitoring Query Execution

```bash
# 1. Execute a query
alt-dremio-cli sql execute "SELECT * FROM large_table LIMIT 1000"
# Output: Job ID: abc-123-def-456

# 2. Check job status
alt-dremio-cli job get abc-123-def-456

# 3. Wait for completion, then get results
alt-dremio-cli job results abc-123-def-456
```

### Debugging Slow Queries

```bash
# 1. List recent jobs
alt-dremio-cli job list --max-results 10

# 2. Get details of slow job
alt-dremio-cli job get slow-job-id

# 3. Download profile for analysis
alt-dremio-cli job profile slow-job-id --download slow_query_profile.zip

# 4. Check if reflections were used
alt-dremio-cli job reflections slow-job-id
```

### Pagination Through Large Results

```bash
# Get results in batches of 1000
for i in {0..9}; do
  offset=$((i * 1000))
  alt-dremio-cli job results abc-123 --limit 1000 --offset $offset > results_part_$i.json
done
```

### Monitoring Running Jobs

```bash
# List all running jobs
alt-dremio-cli job list --filter "state=RUNNING"

# Check specific running job
alt-dremio-cli job get running-job-id

# Cancel if needed
alt-dremio-cli job cancel running-job-id
```

### Job History Analysis

```bash
# Export last 100 jobs
alt-dremio-cli --output json job list --max-results 100 > job_history.json

# Analyze with jq
cat job_history.json | jq '.jobs[] | {id: .id, state: .jobState, duration: .duration}'

# Find failed jobs
cat job_history.json | jq '.jobs[] | select(.jobState == "FAILED")'
```

## Job States

Jobs progress through these states:

1. **PLANNING** - Query is being planned
2. **RUNNING** - Query is executing
3. **COMPLETED** - Query finished successfully
4. **FAILED** - Query failed
5. **CANCELED** - Query was canceled

## Common Workflows

### 1. Execute and Monitor

```bash
# Execute query
RESULT=$(dremio sql execute "SELECT COUNT(*) FROM customers")
JOB_ID=$(echo $RESULT | grep -oP 'Job ID: \K[a-f0-9-]+')

# Monitor until complete
while true; do
  STATE=$(dremio --output json job get $JOB_ID | jq -r '.jobState')
  echo "Job state: $STATE"
  [[ "$STATE" == "COMPLETED" ]] && break
  sleep 2
done

# Get results
alt-dremio-cli job results $JOB_ID
```

### 2. Batch Job Management

```bash
# Get all running jobs
RUNNING_JOBS=$(dremio --output json job list --filter "state=RUNNING" | jq -r '.jobs[].id')

# Cancel all running jobs
for job_id in $RUNNING_JOBS; do
  alt-dremio-cli job cancel $job_id --yes
done
```

### 3. Performance Analysis

```bash
# Get job details
alt-dremio-cli --output json job get $JOB_ID > job_details.json

# Extract performance metrics
cat job_details.json | jq '{
  duration: .duration,
  rowCount: .rowCount,
  dataProcessed: .dataProcessed,
  reflectionsUsed: .reflectionsUsed
}'

# Download profile for deep analysis
alt-dremio-cli job profile $JOB_ID --download profile_$JOB_ID.zip
```

### 4. Result Export

```bash
# Export results to different formats
alt-dremio-cli --output json job results $JOB_ID > results.json
alt-dremio-cli --output yaml job results $JOB_ID > results.yaml
alt-dremio-cli --output table job results $JOB_ID > results.txt

# Convert JSON to CSV
alt-dremio-cli --output json job results $JOB_ID | jq -r '.rows[] | @csv' > results.csv
```

## Tips

1. **Save job IDs**: Store job IDs for later reference
   ```bash
   echo "abc-123-def-456" > last_job_id.txt
   JOB_ID=$(cat last_job_id.txt)
   ```

2. **Use filters effectively**: Narrow down job lists
   ```bash
   alt-dremio-cli job list --filter "state=FAILED" --max-results 10
   ```

3. **Automate monitoring**: Create scripts to watch jobs
   ```bash
   watch -n 5 'dremio job list --max-results 5'
   ```

4. **Export for analysis**: Use JSON output for processing
   ```bash
   alt-dremio-cli --output json job list > jobs.json
   ```

## Error Handling

### Job Not Found

```bash
$ alt-dremio-cli job get invalid-job-id
Error: Resource not found
```

**Solution**: Verify the job ID is correct.

### Results Not Available

```bash
$ alt-dremio-cli job results abc-123
Error: Cannot fetch results for job in PLANNING state
```

**Solution**: Wait for job to complete:
```bash
alt-dremio-cli job get abc-123  # Check state
```

### Permission Denied

```bash
$ alt-dremio-cli job get abc-123
Error: Access forbidden
```

**Solution**: Ensure you have permission to view the job.

## Platform Differences

### Cloud
- Job listing may have rate limits
- Some job profile features may differ

### Software
- Full job history available
- Complete profile download support
- Reflection information available

## Best Practices

1. **Monitor long-running queries**: Check job status periodically
2. **Cancel unnecessary jobs**: Free up resources
3. **Download profiles for analysis**: Investigate performance issues
4. **Use pagination for large results**: Avoid memory issues
5. **Filter job lists**: Focus on relevant jobs
6. **Export job history**: Track query patterns over time
