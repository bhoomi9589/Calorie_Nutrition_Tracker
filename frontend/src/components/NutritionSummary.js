import React from 'react';


const NutritionSummary = ({ food, onPlotGraph }) => {
  if (!food) return null;

  return (
    <div className="nutrition-summary">
      <h2>Nutrition Information</h2>
      <div className="nutrition-details">
        <h3>{food.title}</h3>
        <div className="nutrition-values">
          <p>Calories: {food.nutrition?.calories || 0} kcal</p>
          <p>Protein: {food.nutrition?.protein || 0}g</p>
          <p>Carbohydrates: {food.nutrition?.carbs || 0}g</p>
          <p>Fat: {food.nutrition?.fat || 0}g</p>
        </div>
        <button onClick={onPlotGraph} className="plot-graph-btn" style={{marginTop: '10px'}}>Plot Graph</button>
      </div>
    </div>
  );
};

export default NutritionSummary;