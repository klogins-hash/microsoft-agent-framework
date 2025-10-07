# Deployment Guide for Northflank

This guide explains how to deploy the Microsoft Agent Framework to Northflank with PostgreSQL integration and auto-deployment from GitHub.

## Prerequisites

1. **Northflank Account**: Sign up at [northflank.com](https://northflank.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Groq API Key**: Get your API key from [console.groq.com](https://console.groq.com)
4. **PostgreSQL Database**: Use existing "show me the monies" project database

## Step 1: Prepare Environment Variables

You'll need these environment variables in Northflank:

```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://username:password@host:port/database
PORT=8000
PYTHONPATH=/app/src
DEFAULT_GROQ_MODEL=llama3-70b-8192
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=4096
```

## Step 2: Connect to Existing PostgreSQL Database

1. In Northflank dashboard, go to your "show me the monies" project
2. Find your PostgreSQL service
3. Copy the connection string from the service details
4. Use this as your `DATABASE_URL` environment variable

## Step 3: Create Northflank Service

### Option A: Using Northflank Dashboard

1. **Create New Service**:
   - Go to your Northflank project
   - Click "Create Service" → "Deployment"
   - Choose "Git Repository"

2. **Connect GitHub Repository**:
   - Select your GitHub account
   - Choose the microsoft-agent-framework repository
   - Set branch to `main`

3. **Configure Build**:
   - Build Type: `Buildpack`
   - Buildpack: `Python`
   - Build Command: (leave default)
   - Run Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**:
   - Add all the environment variables listed above
   - Link `DATABASE_URL` to your existing PostgreSQL service

5. **Configure Ports**:
   - Internal Port: `8000`
   - Protocol: `HTTP`
   - Public: `Yes`

### Option B: Using northflank.json (Recommended)

The project includes a `northflank.json` file for automated deployment:

1. Push your code to GitHub
2. In Northflank, import the service using the JSON configuration
3. Update environment variables to match your setup

## Step 4: Set Up Auto-Deployment

### GitHub Actions (Included)

The project includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that:

1. Runs tests on every push
2. Deploys to Northflank on main branch pushes

**Setup GitHub Secrets**:
1. Go to your GitHub repository → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `NORTHFLANK_TOKEN`: Your Northflank API token
   - `NORTHFLANK_PROJECT_ID`: Your Northflank project ID

### Northflank Auto-Deploy

1. In your Northflank service settings
2. Go to "Git" tab
3. Enable "Auto deploy" for the main branch
4. Set "Deploy on push" to `Yes`

## Step 5: Database Migration

After deployment, run database migrations:

1. **Using Northflank Console**:
   - Go to your service → Runtime → Console
   - Run: `alembic upgrade head`

2. **Or via API** (after first deployment):
   ```bash
   curl -X POST https://your-app-url.northflank.app/health
   ```

## Step 6: Verify Deployment

1. **Check Health Endpoint**:
   ```bash
   curl https://your-app-url.northflank.app/health
   ```

2. **Test API**:
   ```bash
   curl https://your-app-url.northflank.app/templates
   ```

3. **Create Test Agent**:
   ```bash
   curl -X POST https://your-app-url.northflank.app/agents \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Test Agent",
       "template_name": "code_assistant"
     }'
   ```

## Environment Configuration

### Production Environment Variables

```env
# Required
GROQ_API_KEY=gsk_...
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Optional (with defaults)
DEFAULT_GROQ_MODEL=llama3-70b-8192
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=4096
PORT=8000
PYTHONPATH=/app/src

# Northflank specific
NF_REGION=us-east-1
NF_COMPUTE_SIZE=nf-compute-20
```

### Database Connection

The app automatically handles PostgreSQL connection:
- Converts `postgres://` URLs to `postgresql+asyncpg://`
- Uses connection pooling
- Handles reconnections

## Scaling and Monitoring

### Scaling
- Northflank auto-scales based on CPU/memory usage
- Configure in service settings → Scaling

### Monitoring
- View logs in Northflank dashboard
- Set up alerts for errors
- Monitor database connections

### Health Checks
- Health endpoint: `/health`
- Readiness check: `/`
- Database connectivity included in health checks

## Troubleshooting

### Common Issues

1. **Database Connection Failed**:
   - Check `DATABASE_URL` format
   - Verify PostgreSQL service is running
   - Check network connectivity

2. **Import Errors**:
   - Verify `PYTHONPATH=/app/src` is set
   - Check all dependencies in requirements.txt

3. **Groq API Errors**:
   - Verify `GROQ_API_KEY` is correct
   - Check API quota and limits

4. **Build Failures**:
   - Check Python version in runtime.txt
   - Verify all dependencies are compatible

### Logs and Debugging

```bash
# View application logs
northflank logs service microsoft-agent-framework

# Check build logs
northflank logs build microsoft-agent-framework

# Database logs
northflank logs service your-postgres-service
```

## API Endpoints

Once deployed, your API will be available at:

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /templates` - List agent templates
- `POST /agents` - Create new agent
- `GET /agents` - List all agents
- `POST /agents/{id}/chat` - Chat with agent
- `POST /agents/{id}/chat/stream` - Stream chat
- `GET /conversations/{id}` - Get conversation history

## Security Considerations

1. **Environment Variables**: Never commit secrets to Git
2. **Database Access**: Use connection pooling and prepared statements
3. **API Rate Limiting**: Consider adding rate limiting for production
4. **CORS**: Configure CORS settings for your domain
5. **Authentication**: Add authentication for production use

## Next Steps

1. Set up monitoring and alerting
2. Configure custom domain
3. Add authentication/authorization
4. Set up backup strategies
5. Configure CI/CD pipeline
6. Add comprehensive logging
