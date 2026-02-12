from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from game.models import CharacterClass, Character, Item


class GameAPITestCase(TestCase):
    def setUp(self):
        """Setup test data"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create character class
        self.warrior_class = CharacterClass.objects.create(
            name='Guerreiro',
            description='Classe de teste',
            base_health=100,
            base_mana=50,
            base_attack=10,
            base_defense=8,
            base_speed=5
        )
        
        # Create test item
        self.sword = Item.objects.create(
            name='Espada de Teste',
            description='Uma espada para testes',
            item_type='weapon',
            value=100,
            attack_bonus=5
        )
    
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/v1/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
    
    def test_user_login(self):
        """Test user login"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/v1/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
    
    def test_character_creation(self):
        """Test character creation"""
        # Login first
        self.client.force_authenticate(user=self.user)
        
        data = {
            'name': 'Aragorn',
            'character_class': self.warrior_class.id
        }
        response = self.client.post('/api/v1/game/characters/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_character_list_permission(self):
        """Test that characters are filtered by owner"""
        # Create character for test user
        character = Character.objects.create(
            owner=self.user,
            name='Test Character',
            character_class=self.warrior_class
        )
        
        # Login and check character list
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/game/characters/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Character')
    
    def test_character_classes_public(self):
        """Test that character classes are publicly accessible"""
        response = self.client.get('/api/v1/game/character-classes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_items_public(self):
        """Test that items are publicly accessible"""
        response = self.client.get('/api/v1/game/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GameModelTestCase(TestCase):
    def setUp(self):
        """Setup test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.character_class = CharacterClass.objects.create(
            name='Mago',
            description='Classe mágica',
            base_health=80,
            base_mana=100,
            base_attack=8,
            base_defense=5,
            base_speed=12
        )
    
    def test_character_stats_calculation(self):
        """Test character stat calculations"""
        character = Character.objects.create(
            owner=self.user,
            name='Gandalf',
            character_class=self.character_class,
            level=5
        )
        
        # Test calculated stats
        expected_health = 80 + (5 * 10)  # base + level * 10
        expected_mana = 100 + (5 * 5)   # base + level * 5
        expected_attack = 8 + (5 * 2)   # base + level * 2
        
        self.assertEqual(character.max_health, expected_health)
        self.assertEqual(character.max_mana, expected_mana)
        self.assertEqual(character.attack, expected_attack)
    
    def test_character_string_representation(self):
        """Test character __str__ method"""
        character = Character.objects.create(
            owner=self.user,
            name='Legolas',
            character_class=self.character_class,
            level=3
        )
        
        expected_str = 'Legolas (Mago) - Level 3'
        self.assertEqual(str(character), expected_str)