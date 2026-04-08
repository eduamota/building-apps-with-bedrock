# Bedrock Showcase UI

A simple Streamlit interface to demonstrate Amazon Bedrock capabilities.

## Features

### 💬 Chat with Model
- Direct conversation with Bedrock models
- Support for Nova Lite, Nova Pro, Claude Sonnet
- Chat history maintained in session

### 📚 Knowledge Base RAG
- Query equipment specifications
- View source citations
- Powered by S3 Vectors

### 🛡️ Guardrails Demo
- Test content safety filters
- See what gets blocked/allowed
- Example prompts provided

### 🎨 Image Generation
- Generate images with Nova Canvas
- Adjustable dimensions
- Instant preview

### 🎬 Video Generation
- Create videos with Nova Reel
- Configurable duration and FPS
- Download generated videos

## Setup

### 1. Install Dependencies

```bash
cd UI
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

```bash
aws configure
```

### 3. Run Notebooks (Optional)

For full functionality, run these notebooks first:
- `Bedrock Agents/5-knowledge_base_s3_vectors.ipynb` - For RAG demo
- `Bedrock Agents/7-bedrock_guardrails.ipynb` - For guardrails demo

### 4. Launch UI

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Select Demo** - Choose from sidebar
2. **Configure Settings** - Set AWS region if needed
3. **Interact** - Use the interface for each demo

## Demo Details

### Chat with Model
- Select model from dropdown
- Type message in chat input
- View conversation history

### Knowledge Base RAG
- Requires KB configuration from notebook 5
- Enter equipment-related questions
- View answers with source citations

### Guardrails Demo
- Requires guardrail configuration from notebook 7
- Test safe and unsafe prompts
- See real-time blocking

### Image Generation
- Enter text description
- Choose dimensions
- Generate and view image

### Video Generation
- Enter video description
- Set duration and FPS
- Generate and download video

## Architecture

```
Streamlit UI → boto3 → Amazon Bedrock
                    ↓
            - Models (Nova, Claude)
            - Knowledge Base
            - Guardrails
            - Image/Video Generation
```

## Troubleshooting

### "Knowledge Base not configured"
Run `Bedrock Agents/5-knowledge_base_s3_vectors.ipynb` first

### "Guardrails not configured"
Run `Bedrock Agents/7-bedrock_guardrails.ipynb` first

### Model access errors
Enable model access in Bedrock console:
- Amazon Nova models
- Anthropic Claude models

### Region errors
Ensure selected region supports all features:
- Nova Canvas: us-east-1, us-west-2
- Nova Reel: us-west-2
- Knowledge Bases: Most regions

## Customization

### Add New Demos

```python
elif demo_mode == "🆕 New Demo":
    st.markdown("Description")
    # Your demo code
```

### Change Models

Edit the model list in the selectbox:
```python
model = st.selectbox(
    "Select Model",
    ["your-model-id"]
)
```

### Styling

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF9900"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## Production Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add AWS credentials as secrets

### Docker
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### AWS App Runner
Deploy directly from GitHub with automatic builds

## Security Notes

- Never commit AWS credentials
- Use IAM roles in production
- Enable guardrails for user-facing apps
- Monitor costs with CloudWatch
- Set up budget alerts

## Next Steps

1. Add authentication (Cognito, Auth0)
2. Implement session persistence
3. Add usage analytics
4. Create admin dashboard
5. Deploy to production

## Support

For issues or questions:
- Check notebook outputs for configuration
- Verify AWS credentials
- Review CloudWatch logs
- Test with AWS CLI first
