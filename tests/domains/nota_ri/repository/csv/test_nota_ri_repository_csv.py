import unittest
from pathlib import Path
import sys
import os

# Add src to sys.path to ensure imports work if not already configured
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../src")))

from busca.domains.nota_ri.repository.csv.nota_ri_repository_csv import NotaRIRepositoryCSV
from busca.domains.nota_ri.core import NotaRi

class TestNotaRIRepositoryCSV(unittest.TestCase):
    
    def setUp(self):
        """
        Setup the repository with the real CSV file.
        """
        self.project_root = Path(__file__).parent.parent.parent.parent.parent.parent
        self.csv_path = self.project_root / "data" / "manutancao" / "RIs_T051.csv"
        
        # Fallback if path construction is slightly off due to context
        if not self.csv_path.exists():
            self.csv_path = Path("data/manutancao/RIs_T051.csv").absolute()
            
        self.repo = NotaRIRepositoryCSV(self.csv_path)

    def test_get_current_state(self):
        """
        Test reading the real CSV file and verifying its content.
        """
        if not self.csv_path.exists():
            self.fail(f"Test data file not found at {self.csv_path}")

        # Act
        items = self.repo.get_current_state()
        
        # Assert
        self.assertGreater(len(items), 0, "The repository should return a non-empty list of items")
        self.assertIsInstance(items[0], NotaRi, "Items should be instances of NotaRi")
        self.assertGreater(len(items), 100, "The CSV should contain a significant number of items")
        
        # Verify the first item functionality
        first_item = items[0]
        self.assertEqual(first_item.num_ri, "20043998")
        self.assertEqual(first_item.local_instalacao, "SUA.GLP.PIER01")

if __name__ == '__main__':
    unittest.main()
