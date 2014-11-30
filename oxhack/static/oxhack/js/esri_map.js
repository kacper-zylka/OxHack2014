var map;
require([
    "esri/InfoTemplate",
    "esri/layers/FeatureLayer",
    "esri/map",
    "esri/renderers/HeatmapRenderer",
    "dojo/domReady!"
    ],
    function (InfoTemplate, FeatureLayer, Map, HeatmapRenderer){
    map = new Map("map", {
      center: [-1.257918, 51.759021],
      zoom: 14,
      basemap: "streets"
    });

    var infoContent = "${Colleges} has been visited ${Intensity} times.</p>";
    var infoTemplate = new InfoTemplate("College Details", infoContent);

    var serviceURL = "http://services.arcgis.com/8nDsFeogfUwUXjrP/arcgis/rest/services/colleges/FeatureServer/0";
    var heatmapFeatureLayerOptions = {
      mode: FeatureLayer.MODE_SNAPSHOT,
      infoTemplate: infoTemplate,
      outFields: [
        "Colleges",
        "Intensity"
  ]
    };
    var heatmapFeatureLayer = new FeatureLayer(serviceURL, heatmapFeatureLayerOptions);
    var heatmapRenderer = new HeatmapRenderer({
        field: "Intensity",
        blurRadius: 5,
        maxPixelIntensity: 20,
    });
    
    heatmapFeatureLayer.setRenderer(heatmapRenderer);
    map.addLayer(heatmapFeatureLayer);
  });