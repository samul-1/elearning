<template>
  <div>
    <b-spinner
      style="position: fixed; top: 50%; left: 50%"
      v-if="loading"
      label="Loading..."
    ></b-spinner>
    <div class="mb-5">
      <font-awesome-icon class="mr-1" icon="search" />
      Cerca utenti
      <input v-model="searchText" placeholder="Nome utente" />
    </div>
    <ul class="user-list">
      <li
        v-for="(user, index) in usersDataFiltered"
        :key="user.id"
        :class="{
          'user-list-item': !user.isContributor,
          'shield-user-list-item': user.isContributor,
        }"
      >
        {{ user.username }} {{ user.firstName }} {{ user.lastName }}
        <b-button
          size="sm"
          variant="outline-primary"
          @click="
            toggledUserPermissions =
              toggledUserPermissions == user.id ? null : user.id
          "
          >{{ user.isContributor ? "Gestisci permessi" : "Aggiungi" }}</b-button
        >
        <!-- <b-button v-else size="sm" variant="outline-primary">Aggiungi</b-button> -->
        <div class="permissions" v-if="toggledUserPermissions == user.id">
          <div
            v-for="permission in Object.keys(
              usersDataFiltered[index].permissions
            )"
            :key="permission"
          >
            <span class="permission-name mr-2">{{
              getPermissionDescription(permission)
            }}</span>
            <input
              type="checkbox"
              v-model="usersDataFiltered[index].permissions[permission]"
            />
          </div>
          <b-button
            class="mt-2"
            variant="outline-success"
            @click="updateUserPermissions()"
            :disabled="
              Object.keys(usersDataFiltered[index].permissions).every(
                (k) => !usersDataFiltered[index].permissions[k]
              )
            "
            >Aggiorna permessi</b-button
          >
          <b-button
            v-if="user.isContributor"
            class="mt-2 ml-2"
            variant="outline-danger"
            @click="deleteUserPermissions()"
            >Rimuovi assistente</b-button
          >
        </div>
      </li>
    </ul>
    <transition name="overlay-text">
      <div class="overlay-card" v-if="success">
        <b-card bg-variant="light" text-variant="black">
          <b-card-text class="grid-card">
            <font-awesome-icon
              class="correct"
              icon="check-circle"
              style="width: 80px; height: 80px"
            />
            Operazione avvenuta con successo
          </b-card-text>
        </b-card>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";

// Fontawesome
import { library } from "@fortawesome/fontawesome-svg-core";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { faCheckCircle } from "@fortawesome/free-solid-svg-icons";

library.add(faSearch);
library.add(faCheckCircle);

export default {
  name: "CoursePermissionManager",
  props: {
    apiUsersUrl: String,
    updatePermissionApiUrl: String,
  },
  mounted() {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    // asynchronously fetch users when the component is mounted
    this.getCourseUsers();
  },
  data: () => {
    return {
      success: false,
      usersData: [],
      loading: false,
      searchText: "",
      toggledUserPermissions: null,
    };
  },
  computed: {
    usersDataFiltered() {
      return this.searchText.length
        ? this.usersData.filter(
            (u) =>
              u.username.includes(this.searchText) ||
              u.firstName.includes(this.searchText) ||
              u.lastName.includes(this.searchText)
          )
        : this.usersData;
    },
  },
  methods: {
    getCourseUsers() {
      this.loading = true;
      axios
        .get(this.apiUsersUrl)
        .then((response) => {
          this.loading = false;
          console.log(response.data);
          this.usersData = response.data;
          // for each users that isn't an assistant, generate a default permission object
          // (used to display permission checkboxes if that user is added as an assistant)
          for (const user of this.usersData) {
            if (!user.isContributor) {
              user.permissions = this.getDefaultPermissionObject();
            }
          }
        })
        .catch((error) => {
          // alert(error);
          console.log(error);
        });
    },
    getDefaultPermissionObject() {
      return {
        can_add_questions: false,
        can_edit_questions: false,
        can_add_contributors: false,
        can_edit_contributors: false,
      };
    },
    getPermissionDescription(desc) {
      switch (desc) {
        case "can_add_questions":
          return "Può aggiungere domande";
        case "can_edit_questions":
          return "Può modificare domande";
        case "can_add_contributors":
          return "Può aggiungere assistenti";
        case "can_edit_contributors":
          return "Può modificare i permessi degli assistenti";
      }
    },
    updateUserPermissions() {
      this.loading = true;
      const putData = {
        profile_id: this.toggledUserPermissions, // this is the user whose permissions were being edited
        permissions: this.usersDataFiltered.find(
          (u) => u.id === this.toggledUserPermissions
        ).permissions,
      };
      this.loading = true;

      console.log(putData);

      axios
        .put(this.updatePermissionApiUrl, putData)
        .then((response) => {
          console.log(response);
          this.showConfirmationAndClose();
          this.loading = false;
          // reload user info
          // TODO only reload the affected user
          this.getCourseUsers();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deleteUserPermissions() {
      const deleteData = {
        profile_id: this.toggledUserPermissions, // this is the user whose permissions were being edited
      };
      this.loading = true;

      console.log(deleteData);

      axios
        .delete(this.updatePermissionApiUrl, { data: deleteData })
        .then((response) => {
          console.log(response);
          this.showConfirmationAndClose();
          this.loading = false;
          // reload user info
          // TODO only reload the affected user
          this.getCourseUsers();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showConfirmationAndClose() {
      this.toggledUserPermissions = null;
      // show success message and hide it programmatically
      this.success = true;
      setTimeout(() => {
        this.success = false;
      }, 2000);
    },
  },
};
</script>

<style>
</style>