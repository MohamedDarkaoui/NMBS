<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-container>
        <b-card bg-variant="light">
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

              <b-button v-b-modal.modal-1 type="submit" variant="primary"
                >Calculate</b-button
              >

              <b-modal
                v-if="
                  form.from !== '' &&
                  form.to !== '' &&
                  form.date !== '' &&
                  form.time !== ''
                "
                id="modal-1"
                title="Travel Time"
                ok-only
              >
                <div>
                  Car: {{ form.travelTimeCar }} <br />
                  Train: {{ form.travelTimeTrain }}
                </div>
              </b-modal>

              <b-button type="reset" variant="danger">Reset</b-button>
            </div>
          </b-form-group>
        </b-card>
      </b-container>
    </b-form>
    <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HomeWord",
  data() {
    return {
      form: {
        from: "",
        to: "",
        travelTimeTrain: "",
        travelTimeCar: "",
        time: "",
        date: "",
      },
      stations: [],
      stationNames: [],
      connections: [],
      show: true,
    };
  },
  methods: {
    getStationResponce() {
      axios
        .get("/api/stations")
        .then((responce) => {
          this.stations = responce.data;
          for (let i = 0; i < this.stations.length; i++) {
            this.stationNames.push(this.stations[i]["name"]);
          }
          this.stationNames.sort();
        })
        .catch((err) => {
          console.error(err);
        });
    },
    getConnectionsResponce(date, time) {
      axios
        .get("/api/connections", {
          params: {
            _from: this.form.from,
            to: this.form.to,
            date: date,
            time: time,
          },
        })
        .then((responce) => {
          console.log(responce.data);
          this.connections = responce.data;

          var date = new Date(null);
          date.setSeconds(responce.data["duration"]);
          this.form.travelTimeTrain = date.toISOString().substr(11, 8);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    getHereResponce(lat1, long1, lat2, long2) {
      axios
        .get("/api/here", {
          params: {
            lat1: lat1,
            long1: long1,
            lat2: lat2,
            long2: long2,
          },
        })
        .then((responce) => {
          console.log(responce.data);

          var date = new Date(null);
          date.setSeconds(responce.data);
          this.form.travelTimeCar = date.toISOString().substr(11, 8);
        })
        .catch((err) => {
          console.error(err);
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
      this.getConnectionsResponce(date, time);

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
      this.getHereResponce(lat1, long1, lat2, long2);
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.form.from = "";
      this.form.to = "";
      this.form.travelTimeTrain = "";
      this.form.date = "";
      this.form.time = "";
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
  created() {
    this.getStationResponce();
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
}

@media (min-width: 576px) {
  .container {
    max-width: 540px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 720px;
  }
}

@media (min-width: 992px) {
  .container {
    max-width: 960px;
  }
}

@media (min-width: 1200px) {
  .container {
    max-width: 1140px;
  }
}

.card-columns .card {
  margin-bottom: 0.75rem;
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
</style>
