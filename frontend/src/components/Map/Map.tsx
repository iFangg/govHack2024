'use client';

import { useRef, useEffect } from "react";
import * as d3 from "d3";
import { FeatureCollection } from "geojson";
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';

interface MapProps {
  data: FeatureCollection;
}

// Learnt from and inspired by Rafael Segat here: https://rafaelsegat.com/posts/map-of-australia-react-hooks-d3-js
export default function Map({ data }: MapProps) {
  const svgRef = useRef<SVGSVGElement | null>(null);

  const width = 768;
  const height = 600;

  useEffect(() => {
    /*
     The geoJSON data gives longitude and latitude coordinates (of a 3D sphere)
     which we wish to project down to a 2D plane, i.e. the SVG box.
     We use Mercator for this to preserve angles and small shapes.
    */
    const projection = d3.geoMercator()
      .rotate([0, -14])
      .fitSize([width, height], data)
      .precision(100);
    const pathGenerator = d3.geoPath().projection(projection);

    /*
     Now draw each region boundary...
    */
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();
    svg.selectAll("path")         // for all (existing and to-exist) paths in the SVG...
      .data(data.features)        // bind to the corresponding entry/feature (region) in geoJSON...
      .enter()                    // and get missing entries.
      .append("path")             // add an empty path to the SVG for each missing entry...
      .attr("d", pathGenerator)   // fill by actually converting GeoJSON to SVG path.
      .attr("fill", "#cccccc")    // fill color for each feature
      .on("mouseover", function (e, d) { // tooltip stuff
        tooltip.style('visibility', 'visible')
          .text(d.properties ? d.properties.LGA_NAME24 : "Hidden spot?");
        d3.select(this).attr("fill", "#ffcc00");
      })
      .on("mousemove", function (e) {
        tooltip.style('top', (e.pageY - 5) + 'px')
          .style('left', (e.pageX + 20) + 'px');
      })
      .on("mouseout", function () {
        tooltip.style('visibility', 'hidden');
        d3.select(this).attr("fill", "#cccccc");
      });

    const tooltip = d3.select('body')
      .append('div')
      .style('position', 'absolute')
      .style('padding', '8px')
      .style('background', 'rgba(0, 0, 0, 0.7)')
      .style('color', '#fff')
      .style('border-radius', '4px')
      .style('visibility', 'hidden')
      .style('pointer-events', 'none')
      .text('Tooltip');

    /*
     Apply d3 in-built zoom
    */
    const zoom = d3.zoom<any, unknown>()
      .scaleExtent([1, 500])
      .on("zoom", handleZoom)
    function handleZoom(e: any) {
      d3.select('svg g')
		    .attr('transform', e.transform);
    }
    d3.select('svg').call(zoom)

  }, [data]);

  return (
    <div className="flex items-center justify-center overflow-hidden border p-2">
      <svg width={width} height={height}>
        <g ref={svgRef} />
      </svg>
    </div>
  );
}
