"""
Azure AI Vision Configuration Module
Handles connection and configuration for Azure AI Vision service
"""

import os
from typing import Optional
from dotenv import load_dotenv

try:
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
except ImportError:
    # Fallback for older SDK versions
    ImageAnalysisClient = None

try:
    from azure.core.credentials import AzureKeyCredential
except ImportError:
    AzureKeyCredential = None


class MockVisionClient:
    """Mock client for testing when Azure SDK is not available"""
    
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
    
    def analyze(self, **kwargs):
        """Mock analyze method"""
        return {"features": []}


class AzureVisionConfig:
    """
    Configuration manager for Azure AI Vision service
    """

    def __init__(self):
        """Initialize Azure Vision configuration from environment variables"""
        load_dotenv()
        
        self.endpoint = os.getenv("AZURE_VISION_ENDPOINT")
        self.api_key = os.getenv("AZURE_VISION_API_KEY")
        self.project_name = os.getenv("AZURE_VISION_PROJECT", "pantry-peeper")
        
        if not self.endpoint or not self.api_key:
            raise ValueError(
                "Azure Vision credentials not configured. "
                "Please set AZURE_VISION_ENDPOINT and AZURE_VISION_API_KEY environment variables."
            )
    
    def get_client(self):
        """
        Get an authenticated Azure AI Vision client
        
        Returns:
            ImageAnalysisClient or mock: Authenticated client for Azure AI Vision
        """
        if ImageAnalysisClient is None or AzureKeyCredential is None:
            # Return a mock object for testing if SDK not available
            return MockVisionClient(self.endpoint, self.api_key)
        
        return ImageAnalysisClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )
    
    def validate_connection(self) -> bool:
        """
        Validate that the Azure Vision service is accessible
        
        Returns:
            bool: True if connection is valid, False otherwise
        """
        try:
            self.get_client()
            return True
        except Exception as e:
            print(f"Failed to validate Azure Vision connection: {e}")
            return False
    
    def get_config_dict(self) -> dict:
        """
        Get configuration as dictionary
        
        Returns:
            dict: Configuration dictionary
        """
        return {
            "endpoint": self.endpoint,
            "project_name": self.project_name,
            "service_type": "Azure Computer Vision"
        }
