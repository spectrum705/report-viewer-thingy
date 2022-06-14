


function makeChart(tags,marks, title, elementId) {

    // marks= [20, 30, 50,120], elementId='myChart', labels=['A', 'B', 'C', 'D'], title='Test Chart'
        // const tags= ['A', 'B', 'C', 'D'];
        const data = {
        labels: tags,
        datasets: [{
          label: title,//'Test Chart',
          data: marks,//[20, 30, 50,120],
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
          ],
          borderWidth: 1
        }]
        };


        const config = {
            type: 'bar',
            data: data,
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            },
            };

        const  myChart = new Chart(
                document.getElementById(elementId),//'myChart',),
                config
              );
            
              

}
fetch('/get_chart_data')
.then(function (response) {
    return response.json();
}).then(function (data) {
    console.log('GET response:');
    // console.log(data.chart_1); 
    // makeChart(tags=["maths","english","science","french"],marks=[20, 30, 50,90], title='Test 1', elementId='myChart');
    // console.log(">>tags",data.chart_1.tags);
    // console.log(">>marks",data.chart_1.marks);
    // console.log(">>title",data.chart_1.title);
    // console.log(">>elementId",data.chart_1.elementId);
    makeChart(tags=data.chart_1.tags,marks=data.chart_1.marks, title=data.chart_1.title, elementId=data.chart_1.elementId);
    makeChart(tags=data.chart_2.tags,marks=data.chart_2.marks, title=data.chart_2.title, elementId=data.chart_2.elementId);
    makeChart(tags=data.chart_3.tags,marks=data.chart_3.marks, title=data.chart_3.title, elementId=data.chart_3.elementId);
    makeChart(tags=data.chart_4.tags,marks=data.chart_4.marks, title=data.chart_4.title, elementId=data.chart_4.elementId);

    // makeChart(tags=data.chart_1.tags,marks=data.chart_1.marks, title=data.chart_1.title, elementId=data.chart_1.elementId);
  });
  // test ={{ data | tojson }};
// console.log(">>>>",test);
// makeChart

// makeChart(tags=["maths","english","science","french"],marks=[10, 20 , 30 , 50], title='Test 2', elementId='myChart2');

// makeChart(tags=["maths","english","science","french"],marks=[10, 20 , 30 , 50], title='Test 3', elementId='myChart3');

// makeChart(tags=["maths","english","science","french"],marks=[10, 20 , 30 , 50], title='Test 4', elementId='myChart4');

// const labels = [
//     'English',
//     'Maths',
//     'Science',
//     'Hindi',
//   ];
