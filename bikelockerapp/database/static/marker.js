'use strict';

let locations = [
 {
   "Place": "Auburn Park & Ride ",
   "City": "Auburn",
   "Address": "101 15th St NE, Auburn, WA 98002",
   "latitude": 47.321,
   "longitude": -122.227
 },
 {
   "Place": "Aurora Village Transit Center",
   "City": "Shoreline",
   "Address": "1524 N 200th St, Shoreline, WA 98133",
   "latitude": 47.776,
   "longitude": -122.342
 },
 {
   "Place": "Bear Creek Park & Ride",
   "City": "Redmond",
   "Address": "7760 178th Pl NERedmond, WA 98052",
   "latitude": 47.673,
   "longitude": -122.101
 },
 {
   "Place": "Brickyard Road",
   "City": "Bothell",
   "Address": "15530 Juanita Woodinville Way NE, Bothell, WA 98011",
   "latitude": 47.74,
   "longitude": -122.189
 },
 {
   "Place": "Burien Transit Center",
   "City": "Burien",
   "Address": "14900 4th Ave SW, Burien, WA 98166",
   "latitude": 47.47,
   "longitude": -122.337
 },
 {
   "Place": "Eastgate Park & Ride",
   "City": "Bellevue",
   "Address": "14200 SE Eastgate Way, Bellevue, WA 98007", 
   "latitude": 47.58,
   "longitude": -122.152
 },
 {
   "Place": "Federal Way",
   "City": "Federal Way",
   "Address": "32320 23rd Ave S, Federal Way, WA 98003",
   "latitude": 47.315,
   "longitude": -122.303
 },
 {
   "Place": "Green Lake Park & Ride",
   "City": "North Seattle",
   "Address": "6601 8th Ave NE, Seattle, WA 98115",
   "latitude": 47.676,
   "longitude": -122.32
 },
 {
   "Place": "Houghton Park & Ride",
   "City": "Kirkland",
   "Address": "7024 116th Ave NE, Kirkland, WA 98033",
   "latitude": 47.668,
   "longitude": -122.185
 },
 {
   "Place": "Issaquah Park & Ride",
   "City": "Issaquah",
   "Address": "1645 Newport Way NW, Issaquah, WA 98027",
   "latitude": 47.542,
   "longitude": -122.061
 },
 {
   "Place": "Issaquah Highlands",
   "City": "Issaquah",
   "Address": "1755 Highlands Dr NE, Issaquah, WA 98029",
   "latitude": 47.545,
   "longitude": -122.019
 },
 {
   "Place": "Kenmore Park & Ride",
   "City": "Kenmore",
   "Address": "7304 NE 175th St, Kenmore, WA 98028",
   "latitude": 47.757,
   "longitude": -122.243
 },
 {
   "Place": "Kent/James St Park & Ride",
   "City": "Kent",
   "Address": "902 W James St, Kent, WA 98032", 
   "latitude": 47.386,
   "longitude": -122.243
 },
 {
   "Place": "Kingsgate Park & Ride",
   "City": "Kirkland",
   "Address": "13001 116th Way NE, Kirkland, WA 98034", 
   "latitude": 47.717,
   "longitude": -122.187
 },
 {
   "Place": "Newport Hills Park & Ride",
   "City": "Bellevue ",
   "Address": "5115 113th Pl SE, Bellevue, WA 98006",
   "latitude": 47.546,
   "longitude": -122.189
 },
 {
   "Place": "Northgate Transit Ceneter East Park & Ride",
   "City": "North Seattle",
   "Address": "3rd Ave NE & NE 103rd St, Seattle, WA 98125",
   "latitude": 47.701,
   "longitude": -122.325
 },
 {
   "Place": "Redmond Transit Center",
   "City": "Redmond",
   "Address": "16160 NE 83rd St, Redmond, WA 98052",
   "latitude": 47.677,
   "longitude": -122.124
 },
 {
   "Place": "Renton Highlands",
   "City": "Renton",
   "Address": "1700 Edmonds Ave NE Renton, WA 98056",
   "latitude": 47.507,
   "longitude": -122.184
 },
 {
   "Place": "South Bellevue Park & Ride ",
   "City": "Bellevue ",
   "Address": "2766 112th Ave SE, Bellevue, WA 98004",
   "latitude": 47.586,
   "longitude": -122.191
 },
 {
   "Place": "South Kirkland Park & Ride",
   "City": "Kirkland",
   "Address": "9800 NE 37th Ct, Kirkland, WA 98033",
   "latitude": 47.644,
   "longitude": -122.199
 },
 {
   "Place": "South Sammamish Park & Ride",
   "City": "Sammamish",
   "Address": "3015 228th Ave SE, Sammamish, WA 98075", 
   "latitude": 47.582,
   "longitude": -122.038
 },
 {
   "Place": "Tukwila Park & Ride",
   "City": "Tukwila",
   "Address": "13445 Interurban Ave S, Tukwila, WA 98168",
   "latitude": 47.482,
   "longitude": -122.269
 },
 {
   "Place": "Valley Center Park & Ride",
   "City": "Vashon island",
   "Address": "20221 Vashon Hwy SW, Vashon, WA 98070",
   "latitude": 47.423,
   "longitude": -122.461
 },
 {
   "Place": "Woodinville Park & Ride",
   "City": "Woodinville",
   "Address": "17800 140th Ave NE, Woodinville, WA 98072",
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
marker.bindPopup(data.Place + '</br>' + data.Address);
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

