import React from 'react';

const ResultsList = ({ results, onSelectFood }) => {
  return (
    <div className="results-list">
      <h2>Search Results</h2>
      {results.length === 0 ? (
        <p>No results found</p>
      ) : (
        <ul>
          {results.map((food) => (
            <li key={food.id} onClick={() => onSelectFood(food)} className="food-item">
              <div className="food-item-content">
                <h3>{food.title}</h3>
              </div>
              {food.image && (
                <img src={food.image} alt={food.title} className="food-image" />
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ResultsList;