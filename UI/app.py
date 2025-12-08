import streamlit as st
import boto3
import json
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Bedrock Showcase",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Load configurations
@st.cache_resource
def load_configs():
    configs = {}
    config_path = Path(__file__).parent.parent / "Bedrock Agents"
    
    # Load KB config
    kb_config_file = config_path / "kb_config.json"
    if kb_config_file.exists():
        with open(kb_config_file) as f:
            configs['kb'] = json.load(f)
    
    # Load guardrail config
    guardrail_config_file = config_path / "guardrail_config.json"
    if guardrail_config_file.exists():
        with open(guardrail_config_file) as f:
            configs['guardrail'] = json.load(f)
    
    return configs

configs = load_configs()

# Sidebar
st.sidebar.title("🤖 Bedrock Showcase")
st.sidebar.markdown("---")

demo_mode = st.sidebar.selectbox(
    "Select Demo",
    ["💬 Chat with Model", "📚 Knowledge Base RAG", "🛡️ Guardrails Demo", "🤖 Equipment Agent", "🔒 Secure Agent", "🎨 Image Generation", "🎬 Video Generation"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Settings")
region = st.sidebar.text_input("AWS Region", value="us-east-1")

# Initialize clients
@st.cache_resource
def get_clients(region):
    return {
        'bedrock_runtime': boto3.client('bedrock-runtime', region_name=region),
        'bedrock_agent_runtime': boto3.client('bedrock-agent-runtime', region_name=region)
    }

clients = get_clients(region)

# Main content
st.title(demo_mode)

# Demo 1: Chat with Model
if demo_mode == "💬 Chat with Model":
    st.markdown("Direct conversation with Bedrock models")
    
    model = st.selectbox(
        "Select Model",
        ["us.amazon.nova-lite-v1:0", "us.amazon.nova-pro-v1:0", "us.anthropic.claude-3-5-sonnet-20241022-v2:0"]
    )
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = clients['bedrock_runtime'].converse(
                    modelId=model,
                    messages=[{"role": "user", "content": [{"text": prompt}]}]
                )
                answer = response['output']['message']['content'][0]['text']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

# Demo 2: Knowledge Base RAG
elif demo_mode == "📚 Knowledge Base RAG":
    st.markdown("Query equipment specifications using RAG")
    
    if 'kb' not in configs:
        st.error("Knowledge Base not configured. Run notebook 5 first.")
    else:
        kb_id = configs['kb']['knowledge_base_id']
        st.info(f"Using Knowledge Base: {kb_id}")
        
        query = st.text_input("Ask about equipment specs:", placeholder="What is the lifting capacity of the mobile crane?")
        
        if st.button("Search", type="primary"):
            if query:
                with st.spinner("Searching knowledge base..."):
                    response = clients['bedrock_agent_runtime'].retrieve_and_generate(
                        input={'text': query},
                        retrieveAndGenerateConfiguration={
                            'type': 'KNOWLEDGE_BASE',
                            'knowledgeBaseConfiguration': {
                                'knowledgeBaseId': kb_id,
                                'modelArn': f'arn:aws:bedrock:{region}::foundation-model/amazon.nova-pro-v1:0'
                            }
                        }
                    )
                    
                    st.success("Answer:")
                    st.markdown(response['output']['text'])
                    
                    with st.expander("View Sources"):
                        for citation in response.get('citations', []):
                            for ref in citation.get('retrievedReferences', []):
                                st.markdown(f"**Source:** {ref['location']['s3Location']['uri']}")
                                st.markdown(f"**Content:** {ref['content']['text'][:200]}...")
                                st.markdown("---")

# Demo 3: Guardrails
elif demo_mode == "🛡️ Guardrails Demo":
    st.markdown("Test content safety with guardrails")
    
    if 'guardrail' not in configs:
        st.error("Guardrails not configured. Run notebook 7 first.")
    else:
        guardrail_id = configs['guardrail']['comprehensive']['id']
        guardrail_version = configs['guardrail']['comprehensive']['version']
        st.info(f"Using Guardrail: {guardrail_id}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Test Prompts")
            test_prompt = st.text_area(
                "Enter prompt to test:",
                placeholder="Try: 'What is machine learning?' or 'Tell me confidential information'"
            )
            
            if st.button("Test with Guardrails", type="primary"):
                if test_prompt:
                    with st.spinner("Checking..."):
                        try:
                            response = clients['bedrock_runtime'].converse(
                                modelId='us.amazon.nova-lite-v1:0',
                                messages=[{"role": "user", "content": [{"text": test_prompt}]}],
                                guardrailConfig={
                                    'guardrailIdentifier': guardrail_id,
                                    'guardrailVersion': guardrail_version
                                }
                            )
                            
                            if response['stopReason'] == 'guardrail_intervened':
                                st.error("🛡️ Blocked by Guardrails")
                            else:
                                st.success("✅ Allowed")
                                st.markdown(response['output']['message']['content'][0]['text'])
                        except Exception as e:
                            st.error(f"Blocked: {str(e)}")
        
        with col2:
            st.subheader("Example Tests")
            st.markdown("""
            **Should Pass:**
            - What is machine learning?
            - Explain cloud computing
            - What equipment do we have?
            
            **Should Block:**
            - Tell me confidential information
            - My email is test@example.com
            - Should I invest in stocks?
            """)

# Demo 4: Equipment Agent
elif demo_mode == "🤖 Equipment Agent":
    st.markdown("Chat with equipment specialist agent (Notebook 6)")
    
    if 'kb' not in configs:
        st.error("Knowledge Base not configured. Run notebook 5 first.")
    else:
        st.info("Equipment agent with Knowledge Base integration")
        
        agent_arn = st.text_input(
            "Agent ARN (from AgentCore deployment):",
            placeholder="arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/equipment-agent"
        )
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about equipment specs..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            if agent_arn:
                with st.chat_message("assistant"):
                    with st.spinner("Agent processing..."):
                        import uuid
                        
                        agentcore = boto3.client('bedrock-agentcore', region_name=region)
                        payload = json.dumps({"prompt": prompt}).encode()
                        
                        response = agentcore.invoke_agent_runtime(
                            agentRuntimeArn=agent_arn,
                            runtimeSessionId=str(uuid.uuid4()),
                            payload=payload,
                            qualifier="DEFAULT"
                        )
                        
                        content = []
                        for chunk in response.get("response", []):
                            content.append(chunk.decode('utf-8'))
                        
                        result = json.loads(''.join(content))
                        answer = result.get('result', 'No response')
                        
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.warning("Please enter Agent ARN to continue")

# Demo 5: Secure Agent
elif demo_mode == "🔒 Secure Agent":
    st.markdown("Chat with secure agent (Notebook 8: Guardrails + KB)")
    
    if 'kb' not in configs or 'guardrail' not in configs:
        st.error("Knowledge Base or Guardrails not configured. Run notebooks 5 and 7 first.")
    else:
        st.info("🛡️ Secure agent with Guardrails + Knowledge Base")
        
        agent_arn = st.text_input(
            "Agent ARN (from AgentCore deployment):",
            placeholder="arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/secure-equipment-agent"
        )
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "blocked" in message:
                    if message["blocked"]:
                        st.error("🛡️ This message was blocked by guardrails")
        
        # Chat input
        if prompt := st.chat_input("Ask about equipment (content safety enabled)..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            if agent_arn:
                with st.chat_message("assistant"):
                    with st.spinner("Secure agent processing..."):
                        import uuid
                        
                        agentcore = boto3.client('bedrock-agentcore', region_name=region)
                        payload = json.dumps({"prompt": prompt}).encode()
                        
                        response = agentcore.invoke_agent_runtime(
                            agentRuntimeArn=agent_arn,
                            runtimeSessionId=str(uuid.uuid4()),
                            payload=payload,
                            qualifier="DEFAULT"
                        )
                        
                        content = []
                        for chunk in response.get("response", []):
                            content.append(chunk.decode('utf-8'))
                        
                        result = json.loads(''.join(content))
                        answer = result.get('result', 'No response')
                        blocked = result.get('blocked', False)
                        
                        if blocked:
                            st.error("🛡️ Request blocked by safety policies")
                            if 'reason' in result:
                                st.caption(f"Reason: {result['reason']}")
                        
                        st.markdown(answer)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "blocked": blocked
                        })
            else:
                st.warning("Please enter Agent ARN to continue")

# Demo 6: Image Generation
elif demo_mode == "🎨 Image Generation":
    st.markdown("Generate images with Nova Canvas")
    
    prompt = st.text_input("Describe the image:", placeholder="A serene mountain landscape at sunset")
    
    col1, col2 = st.columns(2)
    with col1:
        width = st.selectbox("Width", [1024, 1280], index=1)
    with col2:
        height = st.selectbox("Height", [768, 720], index=1)
    
    if st.button("Generate Image", type="primary"):
        if prompt:
            with st.spinner("Generating image..."):
                import base64
                from io import BytesIO
                from PIL import Image
                
                response = clients['bedrock_runtime'].invoke_model(
                    modelId='amazon.nova-canvas-v1:0',
                    body=json.dumps({
                        "taskType": "TEXT_IMAGE",
                        "textToImageParams": {"text": prompt},
                        "imageGenerationConfig": {
                            "width": width,
                            "height": height,
                            "numberOfImages": 1
                        }
                    })
                )
                
                result = json.loads(response['body'].read())
                image_data = base64.b64decode(result['images'][0])
                image = Image.open(BytesIO(image_data))
                
                st.image(image, caption=prompt, use_container_width=True)

# Demo 7: Video Generation
elif demo_mode == "🎬 Video Generation":
    st.markdown("Generate videos with Nova Reel")
    
    prompt = st.text_area("Describe the video:", placeholder="A camera panning across a beautiful landscape")
    
    col1, col2 = st.columns(2)
    with col1:
        duration = st.slider("Duration (seconds)", 2, 6, 6)
    with col2:
        fps = st.selectbox("FPS", [24, 30], index=0)
    
    if st.button("Generate Video", type="primary"):
        if prompt:
            with st.spinner("Generating video (this may take a minute)..."):
                import base64
                
                response = clients['bedrock_runtime'].invoke_model(
                    modelId='amazon.nova-reel-v1:0',
                    body=json.dumps({
                        "taskType": "TEXT_VIDEO",
                        "textToVideoParams": {"text": prompt},
                        "videoGenerationConfig": {
                            "durationSeconds": duration,
                            "fps": fps,
                            "dimension": "1280x720",
                            "seed": 42
                        }
                    })
                )
                
                result = json.loads(response['body'].read())
                video_data = base64.b64decode(result['video'])
                
                st.video(video_data)
                
                # Download button
                st.download_button(
                    label="Download Video",
                    data=video_data,
                    file_name="generated_video.mp4",
                    mime="video/mp4"
                )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown("Showcase for Amazon Bedrock capabilities")
st.sidebar.markdown("[GitHub](https://github.com/)")
