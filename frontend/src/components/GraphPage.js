import React from 'react';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  ArcElement,
  Tooltip,
  Legend
);

const GraphPage = ({ dailyLog }) => {
  // Prepare data for line chart (calories over time)
  const calorieData = {
    labels: dailyLog.map((_, index) => `Meal ${index + 1}`),
    datasets: [{
      label: 'Calories per Meal',
      data: dailyLog.map(food => food.nutrition?.calories || 0),
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1,
      fill: false,
    }]
  };

  // Prepare data for macro distribution (doughnut chart)
  const macroData = {
    labels: ['Protein', 'Carbs', 'Fat'],
    datasets: [{
      data: [
        dailyLog.reduce((sum, food) => sum + (food.nutrition?.protein || 0), 0),
        dailyLog.reduce((sum, food) => sum + (food.nutrition?.carbs || 0), 0),
        dailyLog.reduce((sum, food) => sum + (food.nutrition?.fat || 0), 0),
      ],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
    }]
  };

  // Prepare data for nutrient comparison (bar chart)
  const nutrientData = {
    labels: dailyLog.map(food => food.title || 'Unknown Food'),
    datasets: [
      {
        label: 'Protein (g)',
        data: dailyLog.map(food => food.nutrition?.protein || 0),
        backgroundColor: 'rgb(255, 99, 132)',
      },
      {
        label: 'Carbs (g)',
        data: dailyLog.map(food => food.nutrition?.carbs || 0),
        backgroundColor: 'rgb(54, 162, 235)',
      },
      {
        label: 'Fat (g)',
        data: dailyLog.map(food => food.nutrition?.fat || 0),
        backgroundColor: 'rgb(255, 205, 86)',
      },
    ]
  };

  // Options for charts
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Nutrition Analysis',
      },
    },
  };

  return (
    <div className="graph-page">
      <h2>Nutrition Analysis</h2>
      
      <div className="graph-container">
        <div className="graph-item">
          <h3>Calorie Intake Over Time</h3>
          <div className="chart-wrapper">
            <Line data={calorieData} options={options} />
          </div>
        </div>

        <div className="graph-item">
          <h3>Macronutrient Distribution</h3>
          <div className="chart-wrapper">
            <Doughnut data={macroData} options={options} />
          </div>
        </div>

        <div className="graph-item">
          <h3>Nutrient Comparison by Food</h3>
          <div className="chart-wrapper">
            <Bar data={nutrientData} options={options} />
          </div>
        </div>
      </div>

      <div className="summary-stats">
        <div className="stat-item">
          <h4>Total Calories</h4>
          <p>{dailyLog.reduce((sum, food) => sum + (food.nutrition?.calories || 0), 0).toFixed(1)} kcal</p>
        </div>
        <div className="stat-item">
          <h4>Total Protein</h4>
          <p>{dailyLog.reduce((sum, food) => sum + (food.nutrition?.protein || 0), 0).toFixed(1)}g</p>
        </div>
        <div className="stat-item">
          <h4>Total Carbs</h4>
          <p>{dailyLog.reduce((sum, food) => sum + (food.nutrition?.carbs || 0), 0).toFixed(1)}g</p>
        </div>
        <div className="stat-item">
          <h4>Total Fat</h4>
          <p>{dailyLog.reduce((sum, food) => sum + (food.nutrition?.fat || 0), 0).toFixed(1)}g</p>
        </div>
      </div>
    </div>
  );
};

export default GraphPage;