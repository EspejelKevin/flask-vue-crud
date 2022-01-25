<template>
  <div class="container">
    <h1 class="mt-4 mb-4">{{ msg }}</h1>
    <div class="row">
      <div class="col-8">
        <div class="card">
          <div class="card-body">
            <table class="table">
              <thead>
                <tr style="text-align: center">
                  <th scope="col">Id</th>
                  <th scope="col">User</th>
                  <th scope="col">Email</th>
                  <th scope="col">Operations</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ user.email }}</td>
                  <td>
                    <div class="btn-group" role="group" aria-label="">
                      <button
                        class="btn btn-warning"
                        data-bs-toggle="modal"
                        data-bs-target="#editmodal"
                        v-on:click="getUser(user.id)"
                      >
                        Edit
                      </button>
                      <button
                        type="button"
                        class="btn btn-danger"
                        v-on:click="deleteUser(user.id)"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Modal -->
      <div
        class="modal fade"
        id="editmodal"
        tabindex="-1"
        aria-labelledby="exampleModalLabel"
        aria-hidden="true"
      >
      <form v-on:submit.prevent="editUser">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">Edit user</h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label for="modalUsername" class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="modalUsername"
                  v-model="modal_user.username"
                />
              </div>
              <div class="mb-3">
                <label for="modalEmail" class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  id="modalEmail"
                  v-model="modal_user.email"
                />
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Close
              </button>
              <button type="submit" class="btn btn-primary">
                Save changes
              </button>
            </div>
          </div>
        </div>
        </form>
      </div>

      <div class="col">
        <form v-on:submit.prevent="postData">
          <div class="mb-3">
            <label for="inputUsername" class="form-label">Username</label>
            <input
              type="text"
              class="form-control"
              id="inputUsername"
              v-model="user.username"
            />
          </div>
          <div class="mb-3">
            <label for="inputEmail" class="form-label">Email</label>
            <input
              type="email"
              class="form-control"
              id="inputEmail"
              v-model="user.email"
            />
          </div>
          <div class="mb-3">
            <label for="inputPass" class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              id="inputPass"
              v-model="user.password"
            />
          </div>
          <button type="submit" class="btn btn-primary">Create user</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
  data() {
    return {
      users: [],
      user: { username: "", email: "", password: "" },
      modal_user: { id:"", username: "", email: ""}
    };
  },
  created() {
    this.getUsers();
  },
  methods: {
    getUsers() {
      fetch("http://localhost:5000/users")
        .then((respuesta) => respuesta.json())
        .then((datosRepuesta) => {
          this.users = [];
          if (typeof datosRepuesta[0].success === "undefined") {
            this.users = datosRepuesta;
            console.log(this.users);
          }
        })
        .catch(console.log);
    },
    postData() {
      axios
        .post("http://127.0.0.1:5000/users", this.user)
        .then((res) => {
          console.log(res.data);
          window.location.href = "home";
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deleteUser(id) {
      axios
        .post(`http://127.0.0.1:5000/user/delete/${id}`)
        .then((res) => {
          console.log(res.data);
          window.location.href = "home";
        })
        .catch((error) => {
          console.error(error);
        });
    },
    editUser() {
      axios
        .post(`http://localhost:5000/user/update/${this.modal_user.id}`, this.modal_user)
        .then((res) => {
          console.log(res.data)
          window.location.href = "home"
        })
        .catch((e) => {
          console.error(e)
        })
    },
    getUser(id){
      axios
        .get(`http://127.0.0.1:5000/users/${id}`)
        .then((res) => {
          const response = res.data
          this.modal_user = response
          console.log(this.modal_user)
        })
        .catch((e) => {
          console.error(e)
        })
    }
  },
};
</script>



