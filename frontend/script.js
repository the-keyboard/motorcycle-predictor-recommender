const serverUrl = 'http://localhost:8000';

async function getResults() {
  const preferences = {
    displacement_cc: parseFloat(document.getElementById('displacement').value),
    power_bhp: parseFloat(document.getElementById('power').value),
    weight_kg: parseFloat(document.getElementById('weight').value),
    mileage: parseFloat(document.getElementById('mileage').value),
    top_speed: parseFloat(document.getElementById('topSpeed').value),
    star_rating: parseFloat(document.getElementById('rating').value),
  };

  for (let key in preferences) {
    if (isNaN(preferences[key])) {
      alert(`Please enter a valid number for ${key.replace('_', ' ')}`);
      return;
    }
  }

  try {
    document.getElementById('recommendationResult').innerHTML = '<p>Loading recommendations...</p>';
    document.getElementById('pricePredictionResult').innerHTML   = '<p>Loading price prediction...</p>';

    const recommendResponse = await fetch(`${serverUrl}/recommend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(preferences),
    });
    const recommendations = await recommendResponse.json();

    const priceResponse = await fetch(`${serverUrl}/predict-price`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(preferences),
    });
    const priceData = await priceResponse.json();

    localStorage.setItem('userInputs', JSON.stringify(preferences));
    localStorage.setItem('recommendedBikes', JSON.stringify(recommendations));
    localStorage.setItem('predictedPrice', JSON.stringify(priceData.predicted_price));

    window.location.href = 'output.html';
  } catch (error) {
    alert('Error: ' + error.message);
    console.error(error);
  }
}

function displayRecommendations(data) {
  const resultDiv = document.getElementById('recommendationResult');
  if (!data || data.length === 0) {
    resultDiv.innerHTML = '<p>No recommendations found.</p>';
    return;
  }

  let table = '<h3>Top 10 Recommended Bikes:</h3>';
  table += '<table><thead><tr><th>Bike Name</th><th>Score</th></tr></thead><tbody>';
  data.forEach((bike, index) => {
    table += `<tr onclick="showBikeDetails(${index})"><td>${bike.bike_name}</td><td>${bike.score.toFixed(2)}</td></tr>`;
  });
  table += '</tbody></table>';
  resultDiv.innerHTML = table;
}

function displayPricePrediction(price) {
  const resultDiv = document.getElementById('pricePredictionResult');
  resultDiv.innerHTML = `<h3>Predicted Price:</h3><p><strong>₹ ${price.toFixed(2)}</strong></p>`;
}

function showBikeDetails(index) {
  const bike = window.recommendedBikes[index];
  const container = document.getElementById('bikeDetailsContainer');
  container.innerHTML = `
    <ul>
      <li><strong>Brand:</strong> ${bike.brand}</li>
      <li><strong>Bike Name:</strong> ${bike.bike_name}</li>
      <li><strong>Displacement:</strong> ${bike.displacement_cc} cc</li>
      <li><strong>Power:</strong> ${bike.power_bhp} BHP</li>
      <li><strong>Weight:</strong> ${bike.weight_kg} kg</li>
      <li><strong>Mileage:</strong> ${bike.mileage} km/l</li>
      <li><strong>Top Speed:</strong> ${bike.top_speed} km/h</li>
      <li><strong>Star Rating:</strong> ${bike.star_rating}</li>
      <li><strong>Price:</strong> ₹ ${bike.price.toLocaleString()}</li>
    </ul>`;
  document.getElementById('bikeModal').style.display = 'flex';
}

function closeModal() {
  document.getElementById('bikeModal').style.display = 'none';
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeModal();
  }
});
