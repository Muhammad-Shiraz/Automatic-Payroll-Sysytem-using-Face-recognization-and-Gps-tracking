

$(document).ready(function () {
  $("#dateRange").daterangepicker({
    startDate: "01/26/2024",
    endDate: "02/25/2024",
    locale: {
      format: "DD MMM YYYY", // Format like "26 Jan 2024"
    },
  });
});




// fetch('/payroll/api/payroll-chart/')
//   .then(response => response.json())
//   .then(data => {
//     const myChart = echarts.init(document.getElementById('lineChart'));

//     // Define chart options
//     const options = {
//       title: {
//         text: 'Total Daily Payroll Overview',
//         left: 'center',
//         textStyle: { color: '#333', fontSize: 18 }
//       },
//       tooltip: {
//         trigger: 'axis',
//         backgroundColor: 'rgba(50, 50, 50, 0.8)',
//         textStyle: { color: '#fff' }
//       },
//       legend: {
//         data: ['Payroll'],
//         bottom: 0,
//         textStyle: { color: '#666' }
//       },
//       xAxis: {
//         type: 'category',
//         boundaryGap: false,
//         data: data.labels, // Using dates from the API
//         axisLine: { lineStyle: { color: '#999' } }
//       },
//       yAxis: {
//         type: 'value',
//         axisLine: { lineStyle: { color: '#999' } },
//         splitLine: { lineStyle: { type: 'dashed' } }
//       },
//       series: [{
//         name: 'Payroll',
//         type: 'line',
//         smooth: true,
//         lineStyle: { color: '#5470C6', width: 3 },
//         itemStyle: { color: '#5470C6' },
//         areaStyle: { color: 'rgba(84, 112, 198, 0.2)' },
//         data: data.daily_salaries // Using daily salaries from the API
//       }]
//     };

//     myChart.setOption(options);

//     function updateChart(dataset, label) {
//       if (!data[dataset]) {
//         alert(`${label} data not available.`);
//         return;
//       }

//       myChart.setOption({
//         legend: {
//           data: [label]  // ✅ Update legend text
//         },
//         series: [{
//           name: label,    // ✅ Update series name
//           data: data[dataset]
//         }]
//       });
//     }


//     // Button listeners
//     document.getElementById('monthlyBtn').addEventListener('click', function () {
//       updateChart('monthly', 'Monthly Payroll');
//     });

//     document.getElementById('overtimeBtn').addEventListener('click', function () {
//       updateChart('overtime', 'Overtime');
//     });

//     document.getElementById('bonusesBtn').addEventListener('click', function () {
//       updateChart('bonuses', 'Bonuses & Incentives');
//     });
//   });


fetch('/payroll/api/payroll-chart/')
  .then(response => response.json())
  .then(data => {
    const myChart = echarts.init(document.getElementById('lineChart'));

    const options = {
      title: {
        text: 'Payroll Components Overview',
        left: 'center',
        textStyle: { color: '#333', fontSize: 18 }
      },
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(50, 50, 50, 0.8)',
        textStyle: { color: '#fff' },
        with: 10,
      },
      legend: {
        data: ['Daily', 'Overtime'],
        bottom: 0,
        textStyle: { color: '#666' },
        fontSize: 15,
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: data.labels,
        axisLine: { lineStyle: { color: '#999' } }
      },
      yAxis: {
        type: 'value',
        axisLine: { lineStyle: { color: '#999' } },
        splitLine: { lineStyle: { type: 'dashed' } }
      },
      series: [
        {
          name: 'Daily',
          type: 'line',
          smooth: true,
          data: data.daily_salaries,
          lineStyle: { color: '#5470C6' },
          areaStyle: { color: 'rgba(84, 112, 198, 0.2)' }
        },
        {
          name: 'Overtime',
          type: 'line',
          smooth: true,
          data: data.overtime_salaries,
          lineStyle: { color: '#EE6666' },
          areaStyle: { color: 'rgba(238, 102, 102, 0.2)' }
        }
      ]
    };

    myChart.setOption(options);
  });











// fetch('/payroll/api/payroll-chart/')
//   .then(response => response.json())
//   .then(data => {
//     const myChart = echarts.init(document.getElementById('lineChart'));

//     // Define chart options
//     const options = {
//       title: {
//         text: 'Total Daily Payroll Overview',
//         left: 'center',
//         textStyle: { color: '#333', fontSize: 18 }
//       },
//       tooltip: {
//         trigger: 'axis',
//         backgroundColor: 'rgba(50, 50, 50, 0.8)',
//         textStyle: { color: '#fff' }
//       },
//       legend: {
//         data: ['Payroll'],
//         bottom: 0,
//         textStyle: { color: '#666' }
//       },
//       xAxis: {
//         type: 'category',
//         boundaryGap: false,
//         data: data.labels, // Using dates from the API
//         axisLine: { lineStyle: { color: '#999' } }
//       },
//       yAxis: {
//         type: 'value',
//         axisLine: { lineStyle: { color: '#999' } },
//         splitLine: { lineStyle: { type: 'dashed' } }
//       },
//       series: [{
//         name: 'Payroll',
//         type: 'line',
//         smooth: true,
//         lineStyle: { color: '#5470C6', width: 3 },
//         itemStyle: { color: '#5470C6' },
//         areaStyle: { color: 'rgba(84, 112, 198, 0.2)' },
//         data: data.daily_salaries // Using daily salaries from the API
//       }]
//     };

//     myChart.setOption(options);

//     function updateChart(dataset, label) {
//       if (!data[dataset]) {
//         alert(`${label} data not available.`);
//         return;
//       }

//       myChart.setOption({
//         legend: {
//           data: [label]  // ✅ Update legend text
//         },
//         series: [{
//           name: label,    // ✅ Update series name
//           data: data[dataset]
//         }]
//       });
//     }


//     // Button listeners
//     document.getElementById('monthlyBtn').addEventListener('click', function () {
//       updateChart('monthly', 'Monthly Payroll');
//     });

//     document.getElementById('overtimeBtn').addEventListener('click', function () {
//       updateChart('overtime', 'Overtime');
//     });

//     document.getElementById('bonusesBtn').addEventListener('click', function () {
//       updateChart('bonuses', 'Bonuses & Incentives');
//     });
//   });


fetch('/payroll/api/payroll-donut-chart/')
  .then(response => response.json())
  .then(data => {
    // Initialize the ECharts instance
    const pieChart = echarts.init(document.getElementById('modernPieChart'));

    // Set the chart options
    const options = {
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)',
        backgroundColor: 'rgba(50, 50, 50, 0.8)',
        textStyle: {
          color: '#fff',
          fontSize: 12
        }
      },
      legend: {
        top: '5%',
        left: 'center',
        textStyle: {
          color: '#666',
          fontSize: 9
        },
        itemWidth: 9, // Smaller legend items
        itemHeight: 9, // Smaller legend items
      },
      series: [
        {
          name: 'Payroll Breakdown',
          type: 'pie',
          radius: ['40%', '70%'], // Donut style with smaller gap
          center: ['50%', '70%'], // Adjust to the bottom to create the half-donut effect
          startAngle: 180,  // Start from 180 degrees to create a half-donut
          endAngle: 360,    // End at 360 degrees (so it's half the full circle)
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            position: 'center',  // Keep labels centered inside the pie chart
            formatter: '{b}\n{d}%',  // Display name and percentage
            fontSize: 14,  // Slightly smaller font size
            fontWeight: 'bold',
            color: '#333'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 16,
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false  // Remove label lines to keep it clean
          },
          data: [
            {
              value: data.total_salary,
              name: 'Total Salary',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#4facfe' },
                  { offset: 1, color: '#00f2fe' }
                ])
              }
            },
            {
              value: data.total_bonus,
              name: 'Bonuses',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#f093fb' },
                  { offset: 1, color: '#f5576c' }
                ])
              }
            },
            {
              value: data.total_overtime_salary,
              name: 'Overtime Salary',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#43e97b' },
                  { offset: 1, color: '#38f9d7' }
                ])
              }
            },
          ]
        }
      ]
    };

    // Set the chart options
    pieChart.setOption(options);

    // Resize the chart on window resize
    window.addEventListener('resize', () => {
      pieChart.resize();
    });
  });








var myChart = echarts.init(document.getElementById('employee-chart'));

var option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
    },
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    axisLabel: { show: false },
    axisTick: { show: false },
    axisLine: { show: false },
  },
  yAxis: {
    type: 'value',
    axisLabel: { show: false },
    axisTick: { show: false },
    axisLine: { show: false },
    splitLine: { show: false },
  },
  grid: {
    left: 0,
    right: 0,
    top: 10,
    bottom: 0,
    containLabel: false,
  },
  series: [
    {
      name: 'Total Employees',
      type: 'line',
      smooth: true,
      symbol: 'none',  // 🚫 Remove the circle dots
      lineStyle: {
        width: 0  // Hide line
      },
      areaStyle: {
        opacity: 0.6,
        color: '#66bb6a'  // Optional: soft green area fill
      },
      data: [10, 20, 60, 40, 30, 40, 10]  // Replace with your actual data
    }
  ]
};

myChart.setOption(option);




// fetch('employees/employee/monthly-data/')  // Replace with your Django URL
//   .then(response => response.json())
//   .then(chartData => {
//     var myChart = echarts.init(document.getElementById('employee-chart'));

//     var option = {
//       tooltip: {
//         trigger: 'axis',
//         axisPointer: {
//           type: 'shadow',
//         },
//       },
//       xAxis: {
//         type: 'category',
//         boundaryGap: false,
//         data: chartData.labels,
//         axisLabel: { show: false },
//         axisTick: { show: false },
//         axisLine: { show: false },
//       },
//       yAxis: {
//         type: 'value',
//         axisLabel: { show: false },
//         axisTick: { show: false },
//         axisLine: { show: false },
//         splitLine: { show: false },
//       },
//       grid: {
//         left: 0,
//         right: 0,
//         top: 10,
//         bottom: 0,
//         containLabel: false,
//       },
//       series: [
//         {
//           name: 'Total Employees',
//           type: 'line',
//           smooth: true,
//           symbol: 'none',
//           lineStyle: {
//             width: 0
//           },
//           areaStyle: {
//             opacity: 0.6,
//             color: '#66bb6a'
//           },
//           data: chartData.data
//         }
//       ]
//     };

//     myChart.setOption(option);
//   });






// -------------------------------------------------------------


// var chart = echarts.init(document.getElementById('present-chart'));

// var option = {
//   tooltip: {
//     trigger: 'axis',
//     axisPointer: {
//       type: 'shadow',
//     },
//   },
//   xAxis: {
//     type: 'category',
//     boundaryGap: false,
//     data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
//     axisLabel: { show: false },
//     axisTick: { show: false },
//     axisLine: { show: false }
//   },
//   yAxis: {
//     type: 'value',
//     axisLabel: { show: false },
//     axisTick: { show: false },
//     axisLine: { show: false },
//     splitLine: { show: false }
//   },
//   grid: {
//     left: 0,
//     right: 0,
//     top: 0,
//     bottom: 0,
//     containLabel: false
//   },
//   series: [{
//     name: 'Present Employees',
//     type: 'line',
//     smooth: true,
//     symbol: 'none',
//     lineStyle: {
//       width: 0
//     },
//     areaStyle: {
//       opacity: 0.6,
//       color: '#42a5f5'
//     },
//     data: [40, 45, 50, 48, 42, 47, 48] // dummy data
//   }]
// };

// chart.setOption(option);


document.addEventListener("DOMContentLoaded", function () {
  var presentChart = echarts.init(document.getElementById('present-chart'));


  fetch('/attendance/present-chart-data/')
    .then(response => response.json())
    .then(data => {
      const labels = data.map(entry => entry.date);
      const values = data.map(entry => entry.present);

      presentChart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: labels,
          axisLabel: { show: false },
          axisTick: { show: false },
          axisLine: { show: false }
        },
        yAxis: {
          type: 'value',
          axisLabel: { show: false },
          axisTick: { show: false },
          axisLine: { show: false },
          splitLine: { show: false }
        },
        grid: {
          left: 0,
          right: 0,
          top: 0,
          bottom: 0,
          containLabel: false
        },
        series: [{
          name: 'Present',
          type: 'line',
          smooth: true,
          symbol: 'none',
          lineStyle: { width: 0 },
          areaStyle: {
            opacity: 0.6,
            color: '#42a5f5'
          },
          data: values
        }]
      });
    });
});




// document.addEventListener("DOMContentLoaded", function () {
//   var presentChart = echarts.init(document.getElementById('present-chart'));

//   fetch('attendance/present-chart-data/')
//     .then(response => response.json())
//     .then(data => {
//       const labels = data.map(entry => entry.date);
//       const values = data.map(entry => entry.present);

//       presentChart.setOption({
//         grid: {
//           left: 0,
//           right: 0,
//           top: 0,
//           bottom: 0
//         },
//         xAxis: {
//           type: 'category',
//           data: labels,
//           show: false
//         },
//         yAxis: {
//           type: 'value',
//           show: false
//         },
//         tooltip: {
//           trigger: 'axis',
//           formatter: function (params) {
//             const item = params[0];
//             return `Date: ${item.axisValue}<br>Present: ${item.data}`;
//           },
//           backgroundColor: '#fff',
//           borderColor: '#42a5f5',
//           borderWidth: 1,
//           textStyle: {
//             color: '#333'
//           }
//         },
//         series: [{
//           name: 'Present',
//           type: 'line',
//           smooth: true,
//           symbol: 'none',
//           lineStyle: {
//             color: '#42a5f5',
//             width: 2
//           },
//           areaStyle: {
//             color: 'rgba(66, 165, 245, 0.3)'
//           },
//           data: values
//         }]
//       });
//     });
// });








// ------------------------------------------------------------------------------------------

// window.onload = function () {
//   fetch('/payroll/daily-salaries-api/')
//     .then(response => response.json())
//     .then(data => {
//       const salaries = data.salaries;
//       const chartDom = document.getElementById('salary-chart');
//       const myChart = echarts.init(chartDom);

//       const option = {
//         grid: {
//           left: 0,
//           right: 0,
//           top: 0,
//           bottom: 0
//         },
//         xAxis: {
//           type: 'category',
//           show: false,
//           data: data.dates
//         },
//         yAxis: {
//           type: 'value',
//           show: false
//         },
//         tooltip: {
//           trigger: 'axis',
//           formatter: function (params) {
//             const item = params[0];
//             return `Date: ${item.axisValue}<br>Salary: Rs${item.data.toFixed(2)}`;
//           },
//           backgroundColor: '#fff',
//           borderColor: '#4CAF50',
//           borderWidth: 1,
//           textStyle: {
//             color: '#333'
//           }
//         },
//         series: [{
//           data: salaries,
//           type: 'line',
//           smooth: true,
//           symbol: 'none',
//           lineStyle: {
//             color: '#4CAF50',
//             width: 2
//           },
//           areaStyle: {
//             color: 'rgba(76, 175, 80, 0.3)'
//           }
//         }]
//       };

//       myChart.setOption(option);
//     });
// };






window.onload = function () {
  fetch('/payroll/daily-salaries-api/')
    .then(response => response.json())
    .then(data => {
      const salaries = data.salaries;
      const chartDom = document.getElementById('salary-chart');
      const myChart = echarts.init(chartDom);

      const option = {
        tooltip: {
          trigger: 'axis',
          formatter: function (params) {
            const item = params[0];
            return `Date: ${item.axisValue}<br>Salary: Rs${item.data.toFixed(2)}`;
          },
          backgroundColor: '#fff',
          borderColor: '#4cc2c7',
          borderWidth: 1,
          textStyle: {
            color: '#333'
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: data.dates,
          axisLabel: { show: false },
          axisTick: { show: false },
          axisLine: { show: false }
        },
        yAxis: {
          type: 'value',
          axisLabel: { show: false },
          axisTick: { show: false },
          axisLine: { show: false },
          splitLine: { show: false }
        },
        grid: {
          left: 0,
          right: 0,
          top: 0,
          bottom: 0,
          containLabel: false
        },
        series: [{
          name: 'Salary',
          type: 'line',
          smooth: true,
          symbol: 'none',
          lineStyle: { width: 0 },
          areaStyle: {
            opacity: 0.6,
            color: '#4cc2c7'
          },
          data: salaries
        }]
      };

      myChart.setOption(option);
    });
};



// =====================================================================================================================================
document.addEventListener('DOMContentLoaded', function () {
  const chartDom = document.getElementById('attendanceChart');
  if (!chartDom) {
    console.error('Div with id "attendanceChart" not found.');
    return;
  }

  const myChart = echarts.init(chartDom);

  fetch('/attendance/api/monthly-attendance-data/')
    .then(res => res.json())
    .then(data => {
      // Assuming your data has 'labels' and 'values' arrays
      const option = {

        tooltip: {},
        xAxis: {
          type: 'category',
          data: data.labels
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: data.values,
          type: 'bar',
          itemStyle: {
            color: 'rgba(75, 192, 192, 0.6)'
          }
        }]
      };

      myChart.setOption(option);
    })
    .catch(error => console.error('Error fetching chart data:', error));
});





// //////////////////////////////////////////////performance/////////////////////////////////////////////

