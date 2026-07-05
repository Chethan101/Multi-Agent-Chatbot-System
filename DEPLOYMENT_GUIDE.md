# Vercel Deployment Guide

## Prerequisites
- Vercel Account (https://vercel.com)
- GitHub Account with this repository
- OpenAI API Key
- Tavily API Key

## Deployment Steps

### 1. Push to GitHub
```bash
git push origin vercel-deployment
```

### 2. Connect to Vercel
1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Select the `vercel-deployment` branch
4. Configure environment variables in Vercel dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API Key
   - `TAVILY_API_KEY`: Your Tavily API Key

### 3. Deploy
Vercel will automatically deploy when you push to the branch.

## API Endpoints

### Health Check
```
GET /api/health
```
Response: `{"status": "ok"}`

### Chat Endpoint
```
POST /api/chat
```

**Request Body:**
```json
{
  "input": "Your question here",
  "openai_api_key": "your-openai-key"
}
```

**Response:**
```json
{
  "response": "Answer from the chatbot"
}
```

## Local Testing

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-api.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys
```

### Run Locally
```bash
python api/index.py
```

The API will run on `http://localhost:5000`

### Test with curl
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What is Python?",
    "openai_api_key": "your-key-here"
  }'
```

## Troubleshooting

1. **Module not found errors**: Ensure all dependencies are in `requirements-api.txt`
2. **API Key errors**: Check environment variables in Vercel dashboard
3. **Timeout errors**: The API may take time on first request; increase timeout settings
4. **500 errors**: Check Vercel logs for detailed error messages

## Frontend Integration

To connect a frontend (React, Next.js, etc.):

```javascript
const response = await fetch('https://your-vercel-url.vercel.app/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    input: userInput,
    openai_api_key: userOpenAIKey
  })
});

const data = await response.json();
console.log(data.response);
```
