from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Abstract base class defining the core agent interface."""
    
    def __init__(
        self,
        name: str,
        instructions: str,
        model_client: 'BaseChatCompletionClient',
        tools: Optional[List] = None,
        memory: Optional['BaseMemory'] = None,
        context: Optional['AgentContext'] = None,
        middleware: Optional[List] = None,
        max_iterations: int = 10
        ):
        self.name = name
        self.instructions = instructions
        self.model_client = model_client
        
        # Process Process optional components with defaults
        self.tools = self._process_tools(tools or [])
        self.memory = memory
        self.context = context or AgentContext()
        self.middleware_chain = MiddlewareChain(
            middleware or []
        )
        
        @abstractmethod
        async def run(
            self,
            task: Union[str, UserMessage, List[Message]],
        ) -> 'AgemtResponse':
            """Execute agent and return final respons"""
            pass
        
        @abstractmethod
        def run_stream(
            self,
            task: Union[str, UserMessage, List[Message]]
        ) -> AsyncGenerator[Union[Message, 'AgentEvent'], None]:
            """Execute agent with streaming output."""
            pass