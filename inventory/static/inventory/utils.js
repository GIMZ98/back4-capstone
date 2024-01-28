async function loadCharts(){
  vehicle_revenue_chart();
  vehicle_profit_chart();
  vehicle_inventory_chart();
}

async function fetchData(chartType) {
  try {
    const response = await fetch(`/api/chartdata/${chartType}`);
    const data = await response.json();

    receivedArray = data['data'];

    let intArray = receivedArray.map(element => {
      // Convert to integer if the element is a string containing only digits
      return typeof element === 'string' && /^\d+$/.test(element) ? parseInt(element) : element;
    });
    
    console.log("recieved", intArray);

    return intArray;
    //return [10, 20, 30];

  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

async function vehicle_revenue_chart(){

  const data = {
    labels: [
      'Cars',
      'EVs',
      'Vans'
    ],
    datasets: [{
      label: 'Revenues Distribution',
      data: await fetchData('revenues'),
      backgroundColor: [
        'rgb(255, 165, 100)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };

  // Get the canvas element
  var ctx = document.getElementById('revenuesChart').getContext('2d');

  // Create the chart
  var myChart = new Chart(ctx, {
      type: 'doughnut',
      data: data,
  });
}

async function vehicle_profit_chart(){

  const data = {
    labels: [
      'Cars',
      'EVs',
      'Vans'
    ],
    datasets: [{
      label: 'Revenues Distribution',
      data: await fetchData('profits'),
      backgroundColor: [
        'rgb(255, 165, 100)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };

  // Get the canvas element
  var ctx2 = document.getElementById('profitsChart').getContext('2d');

  // Create the chart
  var myChart = new Chart(ctx2, {
      type: 'doughnut',
      data: data,
  });
}

// Creates inventory data chart
async function vehicle_inventory_chart(){

  const data = {
    labels: [
      'Cars',
      'EVs',
      'Vans'
    ],
    datasets: [{
      label: 'Revenues Distribution',
      data: await fetchData('unsold'),
      backgroundColor: [
        'rgb(255, 165, 100)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };

  // Get the canvas element
  var ctx2 = document.getElementById('unsoldChart').getContext('2d');

  // Create the chart
  var myChart = new Chart(ctx2, {
      type: 'doughnut',
      data: data,
  });
}