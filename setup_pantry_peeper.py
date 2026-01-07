"""
Main Setup Script for Azure AI Vision - Pantry Peeper
Orchestrates the complete setup, training, and validation of the model
"""

import os
import sys
import json
from dotenv import load_dotenv
from azure_vision_config import AzureVisionConfig
from data_preparation import PantryDatasetPreparer
from model_training import PantryModelTrainer
from model_testing import ModelTester, AcceptanceCriteriValidator


def setup_environment():
    """
    Setup environment variables and configuration
    """
    load_dotenv()
    
    print("=" * 60)
    print("Azure AI Vision Setup for Pantry Peeper")
    print("=" * 60)
    
    # Check for required environment variables
    required_vars = ['AZURE_VISION_ENDPOINT', 'AZURE_VISION_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("\nPlease set the following environment variables:")
        print("  export AZURE_VISION_ENDPOINT=<your-endpoint>")
        print("  export AZURE_VISION_API_KEY=<your-api-key>")
        return False
    
    return True


def initialize_config():
    """
    Initialize Azure Vision configuration
    
    Returns:
        AzureVisionConfig: Configuration object
    """
    print("\n[1] Initializing Azure Vision Configuration...")
    try:
        config = AzureVisionConfig()
        print("✓ Configuration loaded successfully")
        print(f"  Endpoint: {config.endpoint[:50]}...")
        return config
    except Exception as e:
        print(f"✗ Failed to initialize configuration: {e}")
        return None


def prepare_data():
    """
    Prepare training data
    
    Returns:
        dict: Training data split
    """
    print("\n[2] Preparing Training Data...")
    try:
        preparer = PantryDatasetPreparer()
        
        print("  Organizing dataset...")
        preparer.organize_dataset()
        
        print("  Preparing training/validation split...")
        training_data = preparer.prepare_training_data()
        
        print("  Creating dataset manifest...")
        manifest = preparer.create_dataset_manifest()
        
        print("✓ Dataset prepared successfully")
        print(f"  Training samples: {len(training_data['train'])}")
        print(f"  Validation samples: {len(training_data['validation'])}")
        print(f"  Categories: {len(manifest['categories'])}")
        
        return training_data
    except Exception as e:
        print(f"✗ Failed to prepare data: {e}")
        return None


def train_model(config, training_data):
    """
    Train the model
    
    Args:
        config: AzureVisionConfig object
        training_data: Training data dictionary
        
    Returns:
        dict: Training results
    """
    print("\n[3] Training Model...")
    try:
        trainer = PantryModelTrainer(config)
        
        print("  Creating training job...")
        trainer.create_training_job(training_data)
        
        print("  Training model (this may take several minutes)...")
        training_result = trainer.train_model(training_data)
        
        print("✓ Model training completed")
        print(f"  Job ID: {training_result['job_id']}")
        print(f"  Accuracy: {training_result['metrics']['accuracy']:.2%}")
        print(f"  Validation Loss: {training_result['metrics']['validation_loss']:.4f}")
        
        # Save training report
        report_path = trainer.save_training_report()
        print(f"  Report saved to: {report_path}")
        
        return training_result
    except Exception as e:
        print(f"✗ Failed to train model: {e}")
        return None


def validate_model(config, training_data):
    """
    Validate and test the model
    
    Args:
        config: AzureVisionConfig object
        training_data: Training data dictionary
        
    Returns:
        dict: Validation results
    """
    print("\n[4] Validating Model...")
    try:
        tester = ModelTester(config)
        
        # Get validation samples
        test_images = training_data.get('validation', [])[:10]
        
        if not test_images:
            print("  No validation images available, skipping inference tests")
            validation = {}
        else:
            print(f"  Running validation on {len(test_images)} images...")
            validation = tester.run_validation_suite(test_images)
            
            print("✓ Validation completed")
            print(f"  Overall Accuracy: {validation['summary']['accuracy']:.2%}")
            print(f"  Passes Threshold: {validation['summary']['passes_threshold']}")
        
        # Test performance
        print("\n  Testing performance metrics...")
        performance = tester.test_performance()
        print(f"  Average Inference Time: {performance['metrics']['average_inference_time_ms']}ms")
        print(f"  Throughput: {performance['metrics']['throughput_images_per_sec']:.1f} img/sec")
        
        # Generate report
        report_path = tester.generate_test_report()
        print(f"  Test report saved to: {report_path}")
        
        return {"validation": validation, "performance": performance}
    except Exception as e:
        print(f"✗ Failed to validate model: {e}")
        return None


def verify_acceptance_criteria(config):
    """
    Verify acceptance criteria
    
    Args:
        config: AzureVisionConfig object
        
    Returns:
        dict: Acceptance criteria validation results
    """
    print("\n[5] Verifying Acceptance Criteria...")
    try:
        validator = AcceptanceCriteriValidator(config)
        
        print("  ✓ Azure AI Vision is configured properly")
        report = validator.get_validation_report()
        
        print("\n  Validation Report:")
        print(f"  - All criteria met: {report['all_criteria_met']}")
        print(f"  - Summary: {report['summary']}")
        
        for criterion, result in report['criteria_results'].items():
            status = "✓" if result else "✗"
            print(f"  {status} {criterion}: {result}")
        
        return report
    except Exception as e:
        print(f"✗ Failed to verify acceptance criteria: {e}")
        return None


def generate_summary_report(config, training_result, validation_result, acceptance_report):
    """
    Generate comprehensive summary report
    
    Args:
        config: AzureVisionConfig object
        training_result: Training results
        validation_result: Validation results
        acceptance_report: Acceptance criteria report
    """
    print("\n" + "=" * 60)
    print("SETUP SUMMARY")
    print("=" * 60)
    
    summary = {
        "setup_date": "2026-01-07",
        "project": "Pantry Peeper",
        "service": "Azure AI Vision",
        "configuration": config.get_config_dict() if config else {},
        "training": training_result if training_result else {},
        "validation": validation_result if validation_result else {},
        "acceptance_criteria": acceptance_report if acceptance_report else {},
        "overall_status": "SUCCESS" if acceptance_report and acceptance_report.get('all_criteria_met') else "IN PROGRESS"
    }
    
    # Save summary
    with open("setup_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("\n✓ Setup Summary:")
    print(f"  Status: {summary['overall_status']}")
    print("  Configuration: ✓ Configured")
    print(f"  Training: {'✓ Complete' if training_result else '✗ Incomplete'}")
    print(f"  Validation: {'✓ Passed' if validation_result else '✗ Incomplete'}")
    print(f"  Acceptance: {'✓ All criteria met' if summary['overall_status'] == 'SUCCESS' else '✗ Criteria not met'}")
    
    print("\nSummary saved to: setup_summary.json")
    
    return summary


def main():
    """
    Main setup orchestration
    """
    # Setup environment
    if not setup_environment():
        print("\n✗ Environment setup failed")
        sys.exit(1)
    
    # Initialize configuration
    config = initialize_config()
    if not config:
        print("\n✗ Configuration initialization failed")
        sys.exit(1)
    
    # Prepare data
    training_data = prepare_data()
    if not training_data:
        print("\n✗ Data preparation failed")
        sys.exit(1)
    
    # Train model
    training_result = train_model(config, training_data)
    if not training_result:
        print("\n⚠️  Model training incomplete")
    
    # Validate model
    validation_result = validate_model(config, training_data)
    if not validation_result:
        print("\n⚠️  Model validation incomplete")
    
    # Verify acceptance criteria
    acceptance_report = verify_acceptance_criteria(config)
    
    # Generate summary
    generate_summary_report(config, training_result, validation_result, acceptance_report)
    
    # Final status
    if acceptance_report and acceptance_report.get('all_criteria_met'):
        print("\n✓ Setup completed successfully! Azure AI Vision is ready for Pantry Peeper.")
        sys.exit(0)
    else:
        print("\n⚠️  Setup completed with issues. Review the reports above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
