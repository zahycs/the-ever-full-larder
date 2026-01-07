"""
Unit Tests for Azure AI Vision Setup and Model Training
"""

import pytest
from azure_vision_config import AzureVisionConfig
from model_training import PantryModelTrainer
from model_testing import ModelTester, AcceptanceCriteriValidator
from data_preparation import PantryDatasetPreparer
import os
from unittest.mock import patch


class TestAzureVisionConfig:
    """Tests for Azure Vision configuration"""
    
    def test_config_initialization(self):
        """Test that configuration initializes with required variables"""
        with patch.dict(os.environ, {
            'AZURE_VISION_ENDPOINT': 'https://test.cognitiveservices.azure.com/',
            'AZURE_VISION_API_KEY': 'test-api-key'
        }):
            config = AzureVisionConfig()
            assert config.endpoint is not None
            assert config.api_key is not None
    
    def test_config_requires_credentials(self):
        """Test that configuration raises error without credentials"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                AzureVisionConfig()
    
    def test_config_dict_output(self):
        """Test configuration dictionary output"""
        with patch.dict(os.environ, {
            'AZURE_VISION_ENDPOINT': 'https://test.cognitiveservices.azure.com/',
            'AZURE_VISION_API_KEY': 'test-api-key'
        }):
            config = AzureVisionConfig()
            config_dict = config.get_config_dict()
            assert 'endpoint' in config_dict
            assert 'project_name' in config_dict


class TestPantryDatasetPreparer:
    """Tests for data preparation module"""
    
    def test_dataset_preparer_initialization(self):
        """Test dataset preparer initialization"""
        preparer = PantryDatasetPreparer()
        assert preparer.prepared_dir.exists()
    
    def test_organize_dataset(self):
        """Test dataset organization"""
        preparer = PantryDatasetPreparer()
        stats = preparer.organize_dataset()
        assert len(stats) == len(preparer.PANTRY_ITEMS)
    
    def test_create_dataset_manifest(self):
        """Test dataset manifest creation"""
        preparer = PantryDatasetPreparer()
        manifest = preparer.create_dataset_manifest()
        assert manifest['dataset_name'] == "Pantry Item Recognition Dataset"
        assert len(manifest['categories']) == 15


class TestPantryModelTrainer:
    """Tests for model training"""
    
    def test_training_job_creation(self):
        """Test training job creation"""
        with patch.dict(os.environ, {
            'AZURE_VISION_ENDPOINT': 'https://test.cognitiveservices.azure.com/',
            'AZURE_VISION_API_KEY': 'test-api-key'
        }):
            with patch('model_training.AzureVisionConfig'):
                trainer = PantryModelTrainer()
                training_data = {'train': ['img1.jpg'], 'validation': ['img2.jpg']}
                job_config = trainer.create_training_job(training_data)
                assert 'job_id' in job_config
                assert job_config['model_type'] == 'object_detection'
    
    def test_training_metrics_calculation(self):
        """Test training metrics calculation"""
        with patch.dict(os.environ, {
            'AZURE_VISION_ENDPOINT': 'https://test.cognitiveservices.azure.com/',
            'AZURE_VISION_API_KEY': 'test-api-key'
        }):
            with patch('model_training.AzureVisionConfig'):
                trainer = PantryModelTrainer()
                metrics = trainer.calculate_training_metrics()
                assert 'accuracy' in metrics
                assert metrics['accuracy'] > 0


class TestModelTester:
    """Tests for model testing and validation"""
    
    def test_inference_test(self):
        """Test model inference"""
        with patch.dict(os.environ, {
            'AZURE_VISION_ENDPOINT': 'https://test.cognitiveservices.azure.com/',
            'AZURE_VISION_API_KEY': 'test-api-key'
        }):
            with patch('model_testing.AzureVisionConfig'):
                tester = ModelTester()
                result = tester.test_inference('test.jpg')
                assert 'predictions' in result
                assert len(result['predictions']) > 0
    
    def test_acceptance_criteria_validation(self):
        """Test acceptance criteria validation"""
        with patch.dict(os.environ, {
            'AZURE_VISION_ENDPOINT': 'https://test.cognitiveservices.azure.com/',
            'AZURE_VISION_API_KEY': 'test-api-key'
        }):
            with patch('model_testing.AzureVisionConfig'):
                tester = ModelTester()
                criteria = tester.verify_acceptance_criteria()
                assert 'azure_vision_configured' in criteria
                assert 'model_accuracy_validated' in criteria


class TestAcceptanceCriteriValidator:
    """Tests for acceptance criteria validation"""
    
    def test_validator_initialization(self):
        """Test validator initialization"""
        with patch.dict(os.environ, {
            'AZURE_VISION_ENDPOINT': 'https://test.cognitiveservices.azure.com/',
            'AZURE_VISION_API_KEY': 'test-api-key'
        }):
            with patch('model_testing.AzureVisionConfig'):
                validator = AcceptanceCriteriValidator()
                assert validator.validation_results == {}
    
    def test_get_validation_report(self):
        """Test validation report generation"""
        with patch.dict(os.environ, {
            'AZURE_VISION_ENDPOINT': 'https://test.cognitiveservices.azure.com/',
            'AZURE_VISION_API_KEY': 'test-api-key'
        }):
            with patch('model_testing.AzureVisionConfig'):
                validator = AcceptanceCriteriValidator()
                report = validator.get_validation_report()
                assert 'validation_timestamp' in report
                assert 'all_criteria_met' in report


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
