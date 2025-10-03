import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SearchBar from './components/SearchBar';
import ResultsList from './components/ResultsList';
import NutritionSummary from './components/NutritionSummary';
import ChartComponent from './components/ChartComponent';
import './App.css';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedFood, setSelectedFood] = useState(null);
  const [dailyLog, setDailyLog] = useState([]);

  // Auto-load demo data to show chart initially
  useEffect(() => {
    const demoData = [
      {
        title: 'Dosa',
        nutrition: { calories: 168, protein: 4, carbs: 33, fat: 3 }
      },
      {
        title: 'Idli',
        nutrition: { calories: 58, protein: 2, carbs: 12, fat: 1 }
      },
      {
        title: 'Poha',
        nutrition: { calories: 180, protein: 3, carbs: 35, fat: 4 }
      }
    ];
    setDailyLog(demoData);
  }, []);

  const handleSearch = async () => {
    try {
      const response = await axios.get(`/api/search?query=${searchTerm}`);
      setSearchResults(response.data.searchResults || []);
    } catch (error) {
      console.error('Error searching for food:', error);
    }
  };

  const handleSelectFood = async (food) => {
    try {
      const response = await axios.get(`/api/nutrition?id=${food.id}`);
      const foodWithNutrition = { ...food, nutrition: response.data.nutrition };
      setSelectedFood(foodWithNutrition);
      
      // Automatically add to chart when food is selected
      setDailyLog(prevLog => [...prevLog, foodWithNutrition]);
      
      // Also log to backend
      await axios.post('/api/log-food', foodWithNutrition);
    } catch (error) {
      console.error('Error getting nutrition info:', error);
    }
  };

  const handleLogFood = async (food) => {
    try {
      await axios.post('/api/log-food', food);
      setDailyLog([...dailyLog, food]);
    } catch (error) {
      console.error('Error logging food:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="fruit-corner top-left">🥝</div>
        <div className="fruit-corner top-right">🍌</div>
        <div className="fruit-corner bottom-left">🍓</div>
        <div className="fruit-corner bottom-right">🥑</div>
        <h1>Calorie & Nutrition Tracker</h1>
        <p className="subtitle">Track Your Daily Nutrition Journey</p>
      </header>
      <main>
        <div className="content-layout">
          <div className="left-section">
            <div className="search-section">
              <SearchBar
                searchTerm={searchTerm}
                onSearchTermChange={setSearchTerm}
                onSearch={handleSearch}
              />
              <ResultsList results={searchResults} onSelectFood={handleSelectFood} />
            </div>
            <div className="nutrition-section">
              <NutritionSummary food={selectedFood} onLogFood={handleLogFood} />
            </div>
          </div>
          <div className="right-section">
            <div className="charts-section">
              <ChartComponent dailyLog={dailyLog} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
