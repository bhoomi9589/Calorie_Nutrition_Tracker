import React from 'react';
import { Doughnut, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  ArcElement,
  Tooltip,
  Legend
);

const ChartComponent = ({ dailyLog }) => {
  // Calculate total macros
  const totalMacros = dailyLog.reduce(
    (acc, food) => {
      acc.protein += food.nutrition?.protein || 0;
      acc.carbs += food.nutrition?.carbs || 0;
      acc.fat += food.nutrition?.fat || 0;
      return acc;
    },
    { protein: 0, carbs: 0, fat: 0 }
  );

  const macroData = {
    labels: ['Protein', 'Carbohydrates', 'Fat'],
    datasets: [
      {
        data: [totalMacros.protein, totalMacros.carbs, totalMacros.fat],
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
        hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      },
    ],
  };

  // Calculate nutrition per meal
  const nutritionData = {
    labels: dailyLog.map(food => food.title),
    datasets: [
      {
        label: 'Calories',
        data: dailyLog.map(food => food.nutrition?.calories || 0),
        backgroundColor: '#FF6384',
        borderColor: '#FF6384',
        borderWidth: 1,
      },
      {
        label: 'Protein (g)',
        data: dailyLog.map(food => food.nutrition?.protein || 0),
        backgroundColor: '#36A2EB',
        borderColor: '#36A2EB',
        borderWidth: 1,
      },
      {
        label: 'Carbohydrates (g)',
        data: dailyLog.map(food => food.nutrition?.carbs || 0),
        backgroundColor: '#FFCE56',
        borderColor: '#FFCE56',
        borderWidth: 1,
      },
      {
        label: 'Fat (g)',
        data: dailyLog.map(food => food.nutrition?.fat || 0),
        backgroundColor: '#4BC0C0',
        borderColor: '#4BC0C0',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 12
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        },
        ticks: {
          color: '#333'
        }
      },
      x: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        },
        ticks: {
          color: '#333',
          maxRotation: 45,
          minRotation: 0
        }
      }
    }
  };

  return (
    <div className="charts">
      <div className="chart-container">
        <h3>Macronutrient Distribution</h3>
        <div className="chart-wrapper">
          <Doughnut data={macroData} options={chartOptions} />
        </div>
      </div>
      <div className="chart-container">
        <h3>Nutrition per Meal</h3>
        <div className="chart-wrapper">
          <Bar data={nutritionData} options={chartOptions} />
        </div>
      </div>
    </div>
  );
};

export default ChartComponent;