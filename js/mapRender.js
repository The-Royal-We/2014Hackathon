require([
        "esri/urlUtils", "esri/map", "esri/dijit/Directions", 
        "dojo/parser", 
        "dijit/layout/BorderContainer", "dijit/layout/ContentPane", "dojo/domReady!"
      ], function(
        urlUtils, Map, Directions,
        parser
      ) {
        parser.parse();
        //all requests to route.arcgis.com will proxy to the proxyUrl defined in this object.
        urlUtils.addProxyRule({
          urlPrefix: "route.arcgis.com",  
          proxyUrl: "/sproxy"
        });
        urlUtils.addProxyRule({
          urlPrefix: "traffic.arcgis.com",  
          proxyUrl: "/sproxy"
        });

        var map = new Map("map", {
          basemap: "streets",
          center:[-98.56,39.82],
          zoom: 4
        });

        var directions = new Directions({
          map: map
        },"dir");
        directions.startup();
      });