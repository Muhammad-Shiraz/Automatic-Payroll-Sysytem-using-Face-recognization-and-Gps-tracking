const attendanceCtx = document.getElementById('attendanceChart').getContext('2d');
const attendanceChart = new Chart(attendanceCtx, {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'On Time',
        data: [200, 220, 230, 210, 250, 240, 230, 220, 215, 225, 230, 235],
        backgroundColor: 'rgba(46, 204, 113, 0.8)', // Green color
      },
      {
        label: 'Late In',
        data: [50, 40, 35, 45, 30, 40, 35, 45, 50, 40, 35, 30],
        backgroundColor: 'rgba(241, 196, 15, 0.8)', // Yellow color
      },
      {
        label: 'Absent',
        data: [15, 20, 25, 30, 20, 25, 30, 25, 20, 25, 30, 20],
        backgroundColor: 'rgba(231, 76, 60, 0.8)', // Red color
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          font: {
            size: 12,
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 50,
        },
      },
    },
  },
});