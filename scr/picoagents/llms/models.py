from agents.agent import BaseChatCompletionClient

class OpenAIChatCompletionClinet(BaseChatCompletionClient):
    def __init__(self,
                 model: str = "gpt-4.1-mini",
                 api_key: Optional[str] = None):
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)
        
    async def create(
        self, 
        messages: List[Message],
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> ChatCompletionResult:
        # Step 1: Convert our types to provider's format
        api_messages = self.convert_messages_to_api_format(messages)
        
        # step 2: Make the provider-specific API call
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=api_messages,
            tools=tools
        )
        
        # step 3: Convert response back to our unified format
        return ChatCompletionResult(
            message=AssitantMessage(
                content=response.choice[0].message.content
            ),
            usage=Usage(
                tokens_input=response.usage.prompt_tokens,
                tokens_output=response.usage.completion_tokens
            ),
            model=response.model
        )