import Map from "@/components/Map/Map";
import { FeatureCollection, Geometry } from "geojson"; 
import data from "@/assets/LGA_2024_AUST.json";

export default function Home() {
  const geoData = data as FeatureCollection<Geometry>;
  
  return (
    <div className="mx-auto max-w-4xl py-16 px-4">
      <div className="flex flex-col">
        <span>
          What should I put here guys?
        </span>
        <Map data={geoData}/>
      </div>
    </div>
  );
}
