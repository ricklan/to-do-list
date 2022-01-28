import React from "react";
import { Link, useNavigate } from "react-router-dom";

const axios = require("axios");

function handleLogin(e, navigate) {
  e.preventDefault();
  let username = document.getElementById("name");
  let pass = document.getElementById("password");
  let errorTag = document.getElementById("error-login");
  axios
    .post("http://127.0.0.1:5000/login", {
      username: username.value,
      password: pass.value,
    })
    .then(() => {
      errorTag.innerHTML = "";
      navigate("/dashboard", { state: { username: username.value } });
    })
    .catch((error) => {
      if (error.response.status === 404 || error.response.status === 400) {
        errorTag.innerHTML = "Username or password incorrect";
      } else {
        errorTag.innerHTML = error.response.data;
      }
    });
}

function Login() {
  const navigate = useNavigate();
  return (
    <>
      <h3>Log In</h3>
      <form>
        <div>
          <label> Username:</label>
          <input type="text" name="username" id="name" required></input>
        </div>
        <div>
          <label> Passsword:</label>
          <input type="password" name="password" id="password" required></input>
        </div>
        <button onClick={(e) => handleLogin(e, navigate)}>Log In</button>
        <p id="error-login"></p>
      </form>
      <Link to="/signup">Sign Up</Link>
    </>
  );
}
export default Login;
