'use strict';

let locations = [
 {
   "Place": "Auburn ",
   "City": "Auburn",
   "latitude": 47.321,
   "longitude": -122.227
 },
 {
   "Place": "Aurora Village",
   "City": "Shoreline",
   "latitude": 47.776,
   "longitude": -122.342
 },
 {
   "Place": "Bear Creek",
   "City": "Redmond",
   "latitude": 47.673,
   "longitude": -122.101
 },
 {
   "Place": "Brickyard Road",
   "City": "Bothell",
   "latitude": 47.74,
   "longitude": -122.189
 },
 {
   "Place": "Burien Transit Center",
   "City": "Burien",
   "latitude": 47.47,
   "longitude": -122.337
 },
 {
   "Place": "Eastgate Park & Ride",
   "City": "Bellevue",
   "latitude": 47.58,
   "longitude": -122.152
 },
 {
   "Place": "Federal Way",
   "City": "Federal Way",
   "latitude": 47.315,
   "longitude": -122.303
 },
 {
   "Place": "Green Lake Park & Ride",
   "City": "North Seattle",
   "latitude": 47.676,
   "longitude": -122.32
 },
 {
   "Place": "Houghton",
   "City": "Kirkland",
   "latitude": 47.668,
   "longitude": -122.185
 },
 {
   "Place": "Issaquah Transit Center ",
   "City": "Issaquah",
   "latitude": 47.542,
   "longitude": -122.061
 },
 {
   "Place": "Issaquah Highlands",
   "City": "Issaquah",
   "latitude": 47.545,
   "longitude": -122.019
 },
 {
   "Place": "Kenmore",
   "City": "Kenmore",
   "latitude": 47.757,
   "longitude": -122.243
 },
 {
   "Place": "Kent",
   "City": "Kent",
   "latitude": 47.386,
   "longitude": -122.243
 },
 {
   "Place": "Kingsgate",
   "City": "Kirkland",
   "latitude": 47.717,
   "longitude": -122.187
 },
 {
   "Place": "Newport Hills",
   "City": "Bellevue ",
   "latitude": 47.546,
   "longitude": -122.189
 },
 {
   "Place": "Northgate",
   "City": "North Seattle",
   "latitude": 47.701,
   "longitude": -122.325
 },
 {
   "Place": "Redmond Transit Center",
   "City": "Redmond",
   "latitude": 47.677,
   "longitude": -122.124
 },
 {
   "Place": "Renton Highlands",
   "City": "Renton",
   "latitude": 47.507,
   "longitude": -122.184
 },
 {
   "Place": "South Bellevue Park & Ride ",
   "City": "Bellevue ",
   "latitude": 47.586,
   "longitude": -122.191
 },
 {
   "Place": "South Kirkland Park & Ride",
   "City": "Kirkland",
   "latitude": 47.644,
   "longitude": -122.199
 },
 {
   "Place": "South Sammamish Park & Ride",
   "City": "Sammamish",
   "latitude": 47.582,
   "longitude": -122.038
 },
 {
   "Place": "Tukwila Park & Ride",
   "City": "Tukwila",
   "latitude": 47.482,
   "longitude": -122.269
 },
 {
   "Place": "Valley Center Park & Ride",
   "City": "Vashon island",
   "latitude": 47.423,
   "longitude": -122.461
 },
 {
   "Place": "Woodinville Park & Ride",
   "City": "Woodinville",
   "latitude": 47.757,
   "longitude": -122.153
 }
]

// Sets the map view 
var mymap = L.map('mapid').setView([47.606, -122.332], 9);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoieWVvbWoiLCJhIjoiY2pzMWVrY3V2MDR1ZDN5bzA5NDU3dTV3diJ9.FE52Fe9BEDs8T6O5VgMynQ'
}).addTo(mymap);


// Displays the markers on the map 
function displayMarker(data) {
var marker =  L.marker([data.latitude, data.longitude]).addTo(mymap);
marker.bindPopup(data.Place);
}


// Grabs the data from the submit from filter and 
// then displays the markers 
function filterMarkers() {
 
  var e = document.getElementById('cities');
  var strUser = e.options[e.selectedIndex].value;
  console.log(strUser);

  var filtered = locations.filter(a=> a.City==strUser);
  console.log(filtered);

 filtered.filter(displayMarker);

}

