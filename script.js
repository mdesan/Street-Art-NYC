function loadGoogleMapsAPI() {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${CONFIG.GMapsAPIKey}&callback=initMap`;
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
}


window.addEventListener('load', loadGoogleMapsAPI);


let map;
let groupedCoords = {}
let allMarkers = []; 
let markerCluster; 

async function initMap() {
    const nycBounds = {
      north: 41.4,     
      south: 40.1,     
      west: -74.7,     
      east: -73.3,     
    };
  
    const nycCenter = { lat: 40.7128, lng: -74.0060 };
  
    map = new google.maps.Map(document.getElementById("map"), {
      zoom: 11,
      center: nycCenter,
      restriction: {
        latLngBounds: nycBounds,
        strictBounds: true,
      },
      minZoom: 8,
      maxZoom: 18,
    });

    await setMarkers();
  }

  //this fills the groupedCoords dictionary
  async function groupCoords(){

      const response = await fetch("artworks.json");
      const coordinates = await response.json();

      coordinates.forEach(artwork => {

        const key = `${artwork.latitude},${artwork.longitude}`;
        
        if(!groupedCoords[key]){
            groupedCoords[key]=[]
        }
        groupedCoords[key].push(artwork)
      });

  }


  async function setMarkers(){

    const markers = [];

    await groupCoords();


      const infoWindow = new google.maps.InfoWindow(); 

    for (const key in groupedCoords) {
      const artworksAtLocation = groupedCoords[key];
      const [lat, lng] = key.split(',').map(Number);

  // Create 1 marker for this location
      const marker = new google.maps.Marker({
      position: { lat, lng },
     map: map,
       icon: {
        url: "images/blackMarker.png",
         scaledSize: new google.maps.Size(30, 30)
    }
  });

  // if 1 artwork, show 1 title/image. if multiple, show them all in a list
    const content = artworksAtLocation.length === 1
     ? `
       <div style="text-align:center; max-width:200px;">

      <img src="${artworksAtLocation[0].img_url}" 
        style="width:100%; border-radius:8px;cursor: pointer;" 
        onclick='showSidePanelFromHTML("${encodeURIComponent(JSON.stringify(artworksAtLocation[0]))}")'/>

            

          <div><strong>${artworksAtLocation[0].title}</strong><br><em>${artworksAtLocation[0].artist}</em></div>
        </div>
      `
      : `
        <div style="max-width:200px;">
          ${artworksAtLocation.map(art => `
            <div style="margin-bottom:12px;">

        <img src="${art.img_url}" 
           style="width:100%; border-radius:8px;cursor: pointer;" 
          onclick='showSidePanelFromHTML("${encodeURIComponent(JSON.stringify(art))}")'/>


              <div><strong>${art.title}</strong><br><em>${art.artist}</em></div>
            </div>
          `).join('')}
        </div>
      `;

    marker.addListener("mouseover", () => {
      infoWindow.setContent(content);
      infoWindow.open(map, marker);
    });

    marker.addListener("mouseout", () => {
      infoWindow.close();
    });

    markers.push(marker);

    const markerEntry = {
      marker: marker,
      artworks: artworksAtLocation // could be one or more artworks
    };

  allMarkers.push(markerEntry);
  }
  markerCluster = new markerClusterer.MarkerClusterer({
    map: map,
   markers: markers
  });
     
    } 

    document.getElementById("search-box").addEventListener("input", function () {
      const query = this.value.toLowerCase();
      filterMarkers(query);
    });


    function showSidePanel(art){

      document.getElementById("panel-img").src = art.img_url;
      document.getElementById("panel-title").textContent = art.title;
      document.getElementById("panel-artist").textContent = art.artist;
      document.getElementById("panel-address").textContent = art.address;
      document.getElementById("info-panel").style.display = "block";

    }

    document.getElementById("close-panel").addEventListener("click", () => {
      document.getElementById("info-panel").style.display = "none";
    });


  function showSidePanelFromHTML(encodedArt) {
    const art = JSON.parse(decodeURIComponent(encodedArt));
    showSidePanel(art);
  }
    function filterMarkers(query) {
      // First, hide all markers
      allMarkers.forEach(entry => {
        entry.marker.setMap(null);
      });

      
      if (markerCluster) {
        markerCluster.clearMarkers();
      }

      const filtered = allMarkers.filter(entry => {
        return entry.artworks.some(art =>
          art.title.toLowerCase().includes(query) ||
          art.artist.toLowerCase().includes(query)
        );
      });

      const filteredMarkers = filtered.map(entry => {
        entry.marker.setMap(map);
        return entry.marker;
      });

      // Add only filtered markers to cluster
      markerCluster = new markerClusterer.MarkerClusterer({
        map: map,
        markers: filteredMarkers
      });
    }

