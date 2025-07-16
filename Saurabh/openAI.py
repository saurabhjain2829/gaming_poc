from pydantic.v1 import BaseSettings, Field
from langchain_openai import AzureChatOpenAI

 
class EnvironmentSettings(BaseSettings):
    AZURE_OPENAI_API_KEY:str = Field(..., description="Azure OpenAI key")
    AZURE_OPENAI_ENDPOINT:str= Field(..., description="Azure OpenAI endpoint")
    AZURE_OPENAI_API_VERSION:str= Field(..., description="Azure OpenAI API version")
    AZURE_OPENAI_DEPLOYMENT_NAME:str= Field(..., description="Azure OpenAI model name")
 
 
    class Config:
        env_file = ".env"
 
 
environment_settings = EnvironmentSettings()
 
llm: AzureChatOpenAI = AzureChatOpenAI(
    azure_endpoint=environment_settings.AZURE_OPENAI_ENDPOINT,
    azure_deployment=environment_settings.AZURE_OPENAI_DEPLOYMENT_NAME,
    api_version=environment_settings.AZURE_OPENAI_API_VERSION,
    api_key=environment_settings.AZURE_OPENAI_API_KEY,
    temperature=0.0
)

print(llm.invoke("2+2").content)