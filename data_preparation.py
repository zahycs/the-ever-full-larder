"""
Data Preparation Module for Pantry Item Recognition
Handles dataset preparation, preprocessing, and organization for model training
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
import cv2


class PantryDatasetPreparer:
    """
    Prepares and preprocesses pantry item images for Azure AI Vision training
    """
    
    PANTRY_ITEMS = [
        "flour", "sugar", "salt", "rice", "pasta", "beans", 
        "canned_vegetables", "canned_fruits", "oil", "butter",
        "milk", "cheese", "eggs", "bread", "cereal"
    ]
    
    def __init__(self, data_dir: str = "./pantry_data", img_size: Tuple[int, int] = (224, 224)):
        """
        Initialize data preparer
        
        Args:
            data_dir: Directory where pantry item images are stored
            img_size: Target image size for preprocessing
        """
        self.data_dir = Path(data_dir)
        self.img_size = img_size
        self.prepared_dir = self.data_dir / "prepared"
        self.prepared_dir.mkdir(parents=True, exist_ok=True)
    
    def organize_dataset(self) -> Dict[str, int]:
        """
        Organize raw images into category directories
        
        Returns:
            dict: Count of images per category
        """
        stats = {}
        
        for category in self.PANTRY_ITEMS:
            cat_dir = self.prepared_dir / category
            cat_dir.mkdir(exist_ok=True)
            stats[category] = 0
        
        return stats
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess a single image for training
        
        Args:
            image_path: Path to the image file
            
        Returns:
            np.ndarray: Preprocessed image
        """
        img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")
        
        # Resize to target size
        img = cv2.resize(img, self.img_size)
        
        # Normalize pixel values to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Apply mild color augmentation (optional)
        # Slight brightness/contrast adjustment
        img = cv2.convertScaleAbs(img, alpha=1.05, beta=0)
        
        return img
    
    def prepare_training_data(self, train_ratio: float = 0.8) -> Dict[str, List[str]]:
        """
        Prepare training and validation datasets
        
        Args:
            train_ratio: Ratio of training data (0.8 = 80% train, 20% validation)
            
        Returns:
            dict: Training and validation file lists
        """
        train_files = []
        val_files = []
        
        # Create sample dataset structure
        for category in self.PANTRY_ITEMS:
            cat_dir = self.prepared_dir / category
            cat_dir.mkdir(exist_ok=True)
            
            # Simulate dataset files (in real scenario, these would be actual images)
            num_images = 50  # Default number of training images per category
            
            for i in range(num_images):
                filename = f"{category}_{i:04d}.jpg"
                filepath = cat_dir / filename
                
                # Create placeholder (in production, real images would be copied)
                if not filepath.exists():
                    # Create dummy image
                    dummy_img = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
                    cv2.imwrite(str(filepath), dummy_img)
                
                # Split into train/val
                if i < int(num_images * train_ratio):
                    train_files.append(str(filepath))
                else:
                    val_files.append(str(filepath))
        
        return {
            "train": train_files,
            "validation": val_files
        }
    
    def create_dataset_manifest(self, output_file: str = "dataset_manifest.json") -> Dict:
        """
        Create a manifest file describing the dataset
        
        Args:
            output_file: Path to save manifest
            
        Returns:
            dict: Dataset manifest
        """
        manifest = {
            "dataset_name": "Pantry Item Recognition Dataset",
            "version": "1.0",
            "categories": self.PANTRY_ITEMS,
            "total_categories": len(self.PANTRY_ITEMS),
            "image_size": self.img_size,
            "preprocessing": {
                "resize": True,
                "normalization": "0-1 range",
                "augmentation": True
            },
            "split_ratio": {
                "training": 0.8,
                "validation": 0.2
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return manifest
