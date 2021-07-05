function add_attendance(id) {
  if (!navigator.geolocation){
   console.log("Geolocation is not supported by your browser");
    return;
  }

  function handleErrors(response) {
    if (!response.ok) {
      document.getElementById('attend-fail').classList.remove('hide');

      throw Error(response.statusText);
    }
    return response;
 }

  function success(position) {
    var latitude  = position.coords.latitude;
    var longitude = position.coords.longitude;
    var acc = position.coords.accuracy;

    var att_info = {
        latitude : latitude,
        longitude : longitude,
        subject_timetable_id : id
    };


    console.log(latitude,longitude,acc,id);
    console.log(att_info);

    const csrf_token = document.cookie.match(/csrftoken=([\w-]+)/)[1];

    fetch(`/add_attendance/` , {
        method : 'POST',
        credentials : 'same-origin',
        headers : {'X-CSRFToken': csrf_token,
                   'Accept' : 'application/json'},
        body : JSON.stringify(att_info)
    })
    .then(handleErrors)
    .then(response => {
      console.log("ok")
      var button = document.getElementById(`${id}`);
      button.classList.add("disabled");
      button.innerText = "Attended.";
      document.getElementById('attend-success').classList.remove('hide');
    } )
    .catch(error => {
      console.log(error);
      
    });

  
  }
  function error() {
    console.log("Unable to retrieve your location");
  }
  navigator.geolocation.getCurrentPosition(success, error, {enableHighAccuracy:true});
}