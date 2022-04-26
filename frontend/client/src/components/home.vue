<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-container>
        <b-form-group
          label-cols-lg="3"
          label="Calculate Travel Time"
          label-size="lg"
          label-class="font-weight-bold pt-0"
          class="mb-0"
        >
          <div key="">
            <b-form-group
              id="input-group-3"
              label="Departure"
              label-for="input-3"
            >
              <b-form-select
                id="input-3"
                v-model="form.from"
                :options="stationNames"
                required
              ></b-form-select>
            </b-form-group>

            <b-form-group
              id="input-group-4"
              label="Destination"
              label-for="input-4"
            >
              <b-form-select
                id="input-4"
                v-model="form.to"
                :options="stationNames"
                required
              ></b-form-select>
            </b-form-group>

            <div id="date">
              <label for="example-datepicker">Choose a date</label>
              <b-form-datepicker
                id="example-datepicker"
                v-model="form.date"
                class="mb-2"
              ></b-form-datepicker>
            </div>
            <div id="time">
              <b-time v-model="form.time" locale="en"></b-time>
            </div>

            <div><br /></div>

            <b-button type="submit" variant="primary">Calculate</b-button>

            <b-modal id="modal-1" ref="modal" title="Travel Time" ok-only>
              <div>
                Car: {{ travelTimeCar }} <br />
                Train: {{ travelTimeTrain }}
              </div>
            </b-modal>

            <b-button type="reset" variant="danger">Reset</b-button>
          </div>
          <div id="map">
            <br />
            <l-map :zoom="zoom" :center="center">
              <l-tile-layer
                :url="url"
                :attribution="attribution"
              ></l-tile-layer>
              <l-marker
                v-if="form.marker1 !== ''"
                :lat-lng="form.marker1"
              ></l-marker>
              <l-marker
                v-if="form.marker2 !== ''"
                :lat-lng="form.marker2"
              ></l-marker>
            </l-map>
          </div>
        </b-form-group>
      </b-container>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";
import L from "leaflet";
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import { Icon } from "leaflet";

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

export default {
  name: "HomeWord",
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data() {
    return {
      form: {
        from: "",
        to: "",
        time: "",
        date: "",
        marker1: "",
        marker2: "",
      },

      zoom: 13,
      center: L.latLng(51.2213, 4.4051),
      url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      travelTimeTrain: "",
      travelTimeCar: "",
      stations: [],
      stationNames: [],
      connections: [],
      show: true,
    };
  },
  methods: {
    getStationresponse() {
      axios
        .get("/api/stations")
        .then((response) => {
          this.stations = response.data["station"];
          for (let i = 0; i < this.stations.length; i++) {
            this.stationNames.push(this.stations[i]["name"]);
          }
          this.stationNames.sort();
        })
        .catch((err) => {
          console.error(err);
        });
    },
    getConnectionsresponse(date, time) {
      axios
        .get("/api/connections", {
          params: {
            _from: this.form.from,
            to: this.form.to,
            date: date,
            time: time,
          },
        })
        .then((response) => {
          if (response.status !== 200) {
            console.log("STATUS");
            console.log(response.status);
            this.$alert("Not possible to calculate");
            this.onReset();
            return;
          }
          this.connections = response.data["connection"][0];
          var date = new Date(null);
          date.setSeconds(this.connections["duration"]);
          this.travelTimeTrain = date.toISOString().substr(11, 8);
        })
        .catch(() => {
          this.$alert("Not possible to calculate by train");
        });
    },
    getHereresponse(lat1, long1, lat2, long2, date) {
      axios
        .get("/api/here", {
          params: {
            lat1: lat1,
            long1: long1,
            lat2: lat2,
            long2: long2,
            depTime: date,
          },
        })
        .then((response) => {
          console.log(response.data);
          if (response.status !== 200) {
            console.log("STATUS");
            console.log(response.status);
            this.$alert("Not possible to calculate by car");
            return;
          }
          let durations = [];
          for (var route in response.data["routes"]) {
            let dur = 0;
            for (var section in response.data["routes"][route]["sections"]) {
              dur += parseInt(
                response.data["routes"][route]["sections"][section]["summary"][
                  "duration"
                ]
              );
            }
            durations.push(dur);
          }
          var duration = Math.min(durations);
          var date = new Date(null);
          date.setSeconds(duration);
          this.travelTimeCar = date.toISOString().substr(11, 8);
        })
        .catch(() => {
          this.$alert("Not possible to calculate by car");
        });
    },
    onSubmit(event) {
      event.preventDefault();
      var year = this.form.date.substring(2, 4);
      var month = this.form.date.substring(5, 7);
      var day = this.form.date.substring(8, 10);
      var date = day + month + year;

      var hour = this.form.time.substring(0, 2);
      var minute = this.form.time.substring(3, 5);
      var time = hour + minute;
      this.getConnectionsresponse(date, time);

      year = "20" + year;
      var formattedDate =
        year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":00";
      console.log(formattedDate);
      var lat1 = "";
      var long1 = "";
      var lat2 = "";
      var long2 = "";
      for (let i = 0; i < this.stations.length; i++) {
        if (this.stations[i]["name"] == this.form.from) {
          lat1 = this.stations[i]["locationY"];
          long1 = this.stations[i]["locationX"];
        }
      }
      for (let i = 0; i < this.stations.length; i++) {
        if (this.stations[i]["name"] == this.form.to) {
          lat2 = this.stations[i]["locationY"];
          long2 = this.stations[i]["locationX"];
        }
      }
      this.form.marker1 = L.latLng(lat1, long1);
      this.form.marker2 = L.latLng(lat2, long2);
      this.getHereresponse(lat1, long1, lat2, long2, formattedDate);
      if (
        this.form.from != "" &&
        this.form.to != "" &&
        this.form.date != "" &&
        this.form.time != ""
      ) {
        this.$refs["modal"].show();
      }
    },
    onReset() {
      // Reset our form values
      this.form.from = "";
      this.form.to = "";
      this.travelTimeTrain = "";
      this.travelTimeCar = "";
      this.form.date = "";
      this.form.time = "";
      this.form.marker1 = "";
      this.form.marker2 = "";
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
  created() {
    this.getStationresponse();
  },
};
</script>
<style>
body {
  margin-top: 20px;
  background: #eee;
}
.container {
  margin-right: auto;
  margin-left: auto;
  padding-right: 15px;
  padding-left: 15px;
  width: 100%;
  height: 100%;
}

@media (min-width: 1200px) {
  .container {
    max-width: 1140px;
  }
}
@media (min-height: 1200px) {
  .container {
    max-height: 1140px;
  }
}
.card-columns .card {
  margin-bottom: 0.75rem;
  height: 100%;
}

@media (min-width: 576px) {
  .card-columns {
    column-count: 3;
    column-gap: 1.25rem;
  }
  .card-columns .card {
    display: inline-block;
    width: 100%;
  }
}
.text-muted {
  color: #9faecb !important;
}

p {
  margin-top: 0;
  margin-bottom: 1rem;
}
.mb-3 {
  margin-bottom: 1rem !important;
}

.input-group {
  position: relative;
  display: flex;
  width: 100%;
}
#map {
  height: 70%;
  margin: 10;
}
</style>
