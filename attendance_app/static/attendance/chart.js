document.addEventListener('DOMContentLoaded',() => {
    const csrf_token = document.cookie.match(/csrftoken=([\w-]+)/)[1];

    function handleErrors(response) {
        if (!response.ok) {
    
          throw Error(response.statusText);
        }
        return response;
     }

    async function fetchdata(){
        let url = '/percent/';
        try{
            let res = await fetch(url);
            return await res.json();
        }catch(error){
            console.log(error);
        }
    }

    async function renderdata(){
        let json_data = await fetchdata();
        console.log(json_data)
        var keys = Object.keys(json_data);
        console.log(keys );
        var values = Object.values(json_data);
        console.log(values);

        //start
        var ctx = document.getElementById("myChart");
        var myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: keys,
                datasets: [{
                label: "Total Attended Percentage",
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
              ],
              borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
         
            title: {
                display: true,
                text: 'Total percentage of attended classes per subject'
              },
            legend: { display: false },
            responsive: false,
            scales: {
                xAxes: [{
                    ticks: {
                        min: 0,
                        max: 100
                        },
                   gridLines: {
                      display: false
                   }
                }],
                yAxes: [{
                   gridLines: {
                      display: false
                   }
                }]
           }            
        
          }
        });
        //end
    }


    renderdata();
    //i start here
/*
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ["2015-01", "2015-02", "2015-03", "2015-04", "2015-05", "2015-06", "2015-07", "2015-08", "2015-09", "2015-10", "2015-11", "2015-12"],
        datasets: [{
          label: '# of Tomatoes',
          data: [12, 19, 3, 5, 2, 3, 20, 3, 5, 6, 2, 1],
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: false,
        scales: {
          xAxes: [{
            ticks: {
              maxRotation: 90,
              minRotation: 80
            },
              gridLines: {
              offsetGridLines: true // à rajouter
            }
          },
          {
            position: "top",
            ticks: {
              maxRotation: 90,
              minRotation: 80
            },
            gridLines: {
              offsetGridLines: true // et matcher pareil ici
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    });
    //i end here
    */
})