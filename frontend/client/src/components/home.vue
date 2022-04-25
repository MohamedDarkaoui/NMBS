<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Email address:"
        label-for="input-1"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          placeholder="Enter email"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Your Name:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.name"
          placeholder="Enter name"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="Departure:" label-for="input-3">
        <b-form-select
          id="input-3"
          v-model="form.station1"
          :options="stations"
          required
        ></b-form-select>
      </b-form-group>

      <b-form-group id="input-group-4" label="Destination:" label-for="input-4">
        <b-form-select
          id="input-4"
          v-model="form.station2"
          :options="stations"
          required
        ></b-form-select>
      </b-form-group>

      <b-form-group id="input-group-4" v-slot="{ ariaDescribedby }">
        <b-form-checkbox-group
          v-model="form.checked"
          id="checkboxes-4"
          :aria-describedby="ariaDescribedby"
        >
          <b-form-checkbox value="me">Check me out</b-form-checkbox>
          <b-form-checkbox value="that">Check that out</b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
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
        email: "",
        name: "",
        station: null,
        checked: [],
      },
      stations: [],
      show: true,
    };
  },
  methods: {
    getStationResponce() {
      axios
        .get("/api/stations")
        .then((responce) => {
          console.log(responce.data);
          this.stations = responce.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    onSubmit(event) {
      event.preventDefault();
      alert(JSON.stringify(this.form));
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.form.email = "";
      this.form.name = "";
      this.form.station1 = null;
      this.form.station2 = null;
      this.form.checked = [];
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
