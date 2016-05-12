//Initialize
var map, heatmap;
var pointArray = new google.maps.MVCArray(); 


function heatMapInitialize() {
  // the map's options
  var mapOptions = {
    zoom: 9,
    center: new google.maps.LatLng(42.008490958,-87.667883978),
    mapTypeId: google.maps.MapTypeId.HYBRID
  };

  // the map and where to place it
map = new google.maps.Map(document.getElementById('map'), mapOptions);
    
  // what data for the heatmap and how to display it


heatmap = new google.maps.visualization.HeatmapLayer({
    data: pointArray,
    radius: 15,
    opacity: 0.2,
  });
  // placing the heatmap on the map
  heatmap.setMap(null);
  heatmap.setMap(map);
}

//category="burglary";
function temp(crimeType) { 

$.get("/api/getData/"+crimeType,function(data, status){
    var array = data.toString().split("\n");
    pointArray = [];
    for (i in array){
        var nums = array[i].split(",");
        var location = new google.maps.LatLng(parseFloat(nums[0]),parseFloat(nums[1]));
        pointArray.push(location);
    }
    google.maps.event.addDomListener(window, 'load', heatMapInitialize());
});

};


function getCrimeInfo(date){
$.get("/api/getCrimeInfo/"+date,function(data, status){
  
      console.log(data);
  });

}
          


    





