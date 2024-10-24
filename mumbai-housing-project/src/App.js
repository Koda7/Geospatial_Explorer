import { useState } from "react";
import './App.css';
import { MapContainer, useMap, GeoJSON, TileLayer } from 'react-leaflet';
import L from "leaflet";
import mumbai from "./data/suburbs.json";
import Grid from "@mui/material/Grid";
import Modal from "@mui/material/Modal";
import Select from "@mui/material/Select";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import close from "./close.svg";
import axios from "axios";

const rent_data = {
  "Vikhroli": [[5, 9], [35, 65], [70, 110]],
  "Vile Parle": [[25, 50], [50, 70], [80, 115]],
  "Andheri West": [[9, 16], [55, 85], [160, 190]],
  "Chandivali": [[10, 20], [40, 65], [80, 105]],
  "Ghatkopar West": [[8, 13], [30, 55], [60, 80]],
  "Vandre West": [[25, 40], [50, 70], [195, 230]],
  "Ghatkopar East": [[20, 40], [25, 50], [60, 85]],
  "Kurla (SC)": [[20, 35], [40, 60], [60, 85]],
  "Mankhurd Shivaji Nagar": [[5, 25], [30, 50], [60, 85]],
  "Kalina": [[20, 35], [50, 70], [85, 110]],
  "Vandre East": [[15, 25], [60, 90], [100, 140]],
  "Sion Koliwada": [[5, 20], [25, 50], [65, 95]],
  "Dharavi (SC)": [[5, 12], [20, 45], [50, 85]],
  "Chembur": [[4, 8], [35, 65], [70, 90]],
  "Borivali": [[10, 20], [25, 45], [50, 75]],
  "Magathane": [[8, 18], [20, 45], [50, 80]],
  "Dahisar": [[10, 20], [20, 30], [40, 100]],
  "Mulund": [[17, 30], [30, 50], [60, 85]],
  "Malad West": [[5, 13], [20, 35], [52, 75]],
  "Charkop": [[9, 15], [20, 38], [40, 62]],
  "Kandivali East": [[18, 25], [27, 38], [40, 65]],
  "Jogeshwari East": [[11, 16], [40, 55], [90, 120]],
  "Dindoshi": [[22, 34], [45, 65], [80, 125]],
  "Goregaon": [[12, 22], [30, 45], [55, 90]],
  "Andheri East": [[11, 16], [30, 42], [80, 130]],
  "Versova": [[20, 35], [50, 70], [80, 110]],
  "Bhandup West": [[5, 8], [32, 45], [40, 85]],
  "Wadala": [[30, 55], [60, 90], [100, 145]],
  "Anushakti Nagar": [[15, 35], [40, 65], [75, 100]],
  "Mahim": [[30, 50], [50, 70], [85, 135]],
  "Shivadi": [[25, 40], [40, 60], [70, 95]],
  "Worli": [[18, 38], [100, 140], [160, 220]],
  "Mumbadevi": [[45, 60], [60, 80], [80, 120]],
  "Colaba": [[60, 80], [80, 150], [200, 360]],
  "Byculla": [[27, 43], [55, 85], [90, 130]],
  "Malabar Hill": [[55, 85], [95, 145], [160, 300]],
}


const App = () => {
  const [filters, setFilters] = useState({
    Banks: 0,
    Restaurants: 0,
    Malls: 0,
    Hospitals: 0,
    Schools: 0,
    Marketplaces: 0,
  });

  const [distValue, setDistValue] = useState(0);
  const [column, setColumn] = useState("Restaurants");
  const [openFilter, setOpenFilter] = useState(false);
  const [queryRegion, setQueryRegion] = useState(null);
  const [currentSuburb, setCurrentSuburb] = useState("");
  const [openBudget, setOpenBudget] = useState(false);
  const [budget, setBudget] = useState({ "budget": 0, "type": "1BHK" });

  // Function to render Mumbai GeoJSON Layer
  const RenderMumbai = () => {
    return (
      <GeoJSON
        onEachFeature={(feature, layer) => {
          layer.on("mouseover", () => setCurrentSuburb(feature.properties.AC_NAME));
          layer.on("mouseout", () => setCurrentSuburb(""));
        }}
        key="mumbai"
        data={mumbai}
      />
    );
  };

  const QueryToolbar = () => {
    return (
      <Grid container className="query-toolbar" alignItems="center">
        <Grid item className="query-button" onClick={() => setOpenBudget(true)} mr={1}>
          Add Budget
        </Grid>
        <Grid item className="query-button" onClick={() => setOpenFilter(true)}>
          Add Query
        </Grid>
        {Object.entries(filters).map(([key, value]) =>
          value > 0 ? (
            <Grid item mx={0.5} key={"Filters-" + key} className="query">
              <Grid container alignItems="center">
                {key}: {value} km &nbsp;
                <img
                  style={{ cursor: "pointer" }}
                  onClick={() => setFilters({ ...filters, [key]: 0 })}
                  src={close}
                  width="20px"
                />
              </Grid>
            </Grid>
          ) : null
        )}
        {budget.budget > 0 && (
          <Grid item mx={0.5} className="query">
            <Grid container alignItems="center">
              Budget: {budget.budget} Rs ({budget.type}) &nbsp;
              <img
                style={{ cursor: "pointer" }}
                onClick={() => setBudget({ budget: 0, type: "1BHK" })}
                src={close}
                width="20px"
              />
            </Grid>
          </Grid>
        )}
      </Grid>
    );
  };

  // Function to handle query and call backend
  const makeQuery = (filters, map) => {
    console.log(filters, budget);
    if (queryRegion !== null) map.removeLayer(queryRegion);

    const activeFilters = Object.keys(filters).filter((key) => filters[key] > 0);
    const filterParams = {};
    activeFilters.forEach((key) => {
      filterParams[key] = filters[key];
    });

    const formData = new FormData();
    Object.entries(filterParams).forEach(([key, value]) => formData.set(key, value));
    formData.set("budget", budget.budget);
    formData.set("type", budget.type);

    axios
      .post('/getRegion', formData)
      .then((response) => {
        const newLayer = L.geoJSON(response.data.region, {
          weight: 2,
          color: "#FFD700",
          fillColor: "#c21111",
          fillOpacity: 0.6,
        });
        setQueryRegion(newLayer);
        map.addLayer(newLayer);
      })
      .catch((err) => console.log(err));
  };

  // const MakeQuery = () => {
  //   const map = useMap();
  //   const realKeys = Object.keys(filters).filter((key) => filters[key] > 0);
  //   const realFilters = {};
  //   realKeys.forEach((key) => (realFilters[key] = filters[key]));
  //   if (Object.keys(realFilters).length > 0 || budget.budget > 0)
  //     return <div className="make-query" onClick={() => makeQuery(realFilters, map)}>Make Query</div>;

  //    // Always show the Make Query button if budget is set, even if filters are removed
  //   return budget.budget > 0 ? (
  //     <div className="make-query" onClick={() => makeQuery(realFilters, map)}>Make Query</div>
  //   ) : null;
  // };

  const MakeQuery = () => {
    const map = useMap();

    // Check if any filters are active or budget is set
    const realKeys = Object.keys(filters).filter((key) => filters[key] > 0);
    const realFilters = {};
    realKeys.forEach((key) => (realFilters[key] = filters[key]));

    const isDisabled = Object.keys(realFilters).length === 0 && budget.budget === 0;

    return (
        <div
            className={`make-query ${isDisabled ? "disabled" : ""}`} // Add a disabled class for styling
            onClick={() => {
                if (!isDisabled) makeQuery(realFilters, map);
            }}
        >
            Make Query
        </div>
    );
};


  const mapBounds = [
    [18.89472, 72.77601],
    [19.26871, 72.96776],
  ];

  return (
    <>
      <div className="instructions">
        <h2>Instructions:</h2>
          <p><strong>Hover Over Regions:</strong> Hover over any region on the map to view rent estimates for 1BHK, 2BHK, and 3BHK apartments in that area.</p>
          <p><strong>Add Budget:</strong> Click on the 'Add Budget' button to set your budget preferences (1BHK, 2BHK, or 3BHK) and specify a price range.</p>
          <p><strong>Add Query:</strong> Filter the map by selecting amenities such as Restaurants, Hospitals, Schools, and more. You can set a distance range for each filter.</p>
          <p><strong>Make Query:</strong> After adding filters, click on the 'Make Query' button to see highlighted regions (in red) that match your criteria (the max distance you want to be from this amenity).</p>
          <p><strong>Remove Filters:</strong> To remove a filter or budget, click the 'X' icon next to it in the query toolbar (make sure to click 'Make Query' to update).</p>
      </div>
      {currentSuburb.length > 0 && (
        <div className="suburb-name">
          {currentSuburb === "Vandre West"
            ? "Bandra West"
            : currentSuburb === "Vandre East"
            ? "Bandra East"
            : currentSuburb}
          <br />
          1BHK: &#8377;{rent_data[currentSuburb][0][0] * 1000} - &#8377;{rent_data[currentSuburb][0][1] * 1000} <br />
          2BHK: &#8377;{rent_data[currentSuburb][1][0] * 1000} - &#8377;{rent_data[currentSuburb][1][1] * 1000} <br />
          3BHK: &#8377;{rent_data[currentSuburb][2][0] * 1000} - &#8377;{rent_data[currentSuburb][2][1] * 1000} <br />
        </div>
      )}

      {/* Filter Modal */}
      <Modal open={openFilter} onClose={() => setOpenFilter(false)}>
        <Grid container className="modal-box" style={{ width: "400px" }} p={{ sm: 5, xs: 3 }}>
          <Grid item xs={12} className="filter-column" mb={2}>
            <Select fullWidth value={column} sx={{ fontFamily: "Poppins" }} onChange={(e) => setColumn(e.target.value)}>
              {Object.keys(filters).map((column) => (
                <MenuItem key={column} sx={{ fontFamily: "Poppins" }} value={column}>
                  {column}
                </MenuItem>
              ))}
            </Select>
          </Grid>
          <Grid item xs={12} className="filter-heading">
            Within (in km)
          </Grid>
          <Grid item xs={12} mt={2}>
            <TextField
              focused
              className="filter-label"
              type="number"
              fullWidth
              value={distValue}
              onChange={(event) => {
                setDistValue(event.target.value);
              }}
              inputProps={{
                style: {
                  padding: 10,
                },
              }}
            />
          </Grid>
          <Grid container justifyContent="flex-end" mt={3}>
            <Grid item className="filter-button" style={{ fontSize: "1rem" }} onClick={() => setOpenFilter(false)}>
              Delete
            </Grid>
            <Grid
              item
              style={{ color: "white", background: "#2863e3", fontSize: "1rem" }}
              className="filter-button"
              ml={1}
              onClick={() => {
                setFilters({ ...filters, [column]: Number(distValue) });
                setOpenFilter(false);
              }}
            >
              Confirm
            </Grid>
          </Grid>
        </Grid>
      </Modal>

      {/* Budget Modal */}
      <Modal open={openBudget} onClose={() => setOpenBudget(false)}>
        <Grid container className="modal-box" style={{ width: "400px" }} p={{ sm: 5, xs: 3 }}>
          <Grid item xs={12} className="filter-column" mb={2}>
            <Select
              fullWidth
              value={budget.type}
              sx={{ fontFamily: "Poppins" }}
              onChange={(e) => setBudget({ ...budget, type: e.target.value })}
            >
              <MenuItem sx={{ fontFamily: "Poppins" }} value="1BHK">1BHK</MenuItem>
              <MenuItem sx={{ fontFamily: "Poppins" }} value="2BHK">2BHK</MenuItem>
              <MenuItem sx={{ fontFamily: "Poppins" }} value="3BHK">3BHK</MenuItem>
            </Select>
          </Grid>
          <Grid item xs={12} className="filter-heading">
            Budget (in Rs)
          </Grid>
          <Grid item xs={12} mt={2}>
            <TextField
              focused
              className="filter-label"
              type="number"
              fullWidth
              value={budget.budget !== 0 ? budget.budget : ""}
              onChange={(event) => {
                const newValue = event.target.value; // Define newValue correctly
                setBudget({ ...budget, budget: newValue === "" ? 0 : Number(newValue) });
              }}
              inputProps={{
                style: {
                  padding: 10,
                },
              }}
            />
          </Grid>
          <Grid container justifyContent="flex-end" mt={3}>
            <Grid item className="filter-button" style={{ fontSize: "1rem" }} onClick={() => {
                setBudget({ budget: 0, type: "1BHK" });
                setOpenBudget(false);
              }}
            >
              Delete
            </Grid>
            <Grid
              item
              style={{ color: "white", background: "#2863e3", fontSize: "1rem" }}
              className="filter-button"
              ml={1}
              onClick={() => setOpenBudget(false)}
            >
              Confirm
            </Grid>
          </Grid>
        </Grid>
      </Modal>

      <QueryToolbar />

      <MapContainer bounds={mapBounds} style={{ height: "100vh" }}>
        <MakeQuery />
        <TileLayer
          url="http://{s}.google.com/vt?lyrs=m&x={x}&y={y}&z={z}"
          maxZoom={20}
          subdomains={['mt0', 'mt1', 'mt2', 'mt3']}
        />
        <RenderMumbai />
      </MapContainer>
    </>
  );
};

export default App;

