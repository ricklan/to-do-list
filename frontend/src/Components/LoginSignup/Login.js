import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./LoginSignup.css";
import boy from "../../images/boy.svg";

const axios = require("axios");

function handleLogin(e, navigate) {
  e.preventDefault();
  let username = document.getElementById("login-name");
  let pass = document.getElementById("login-password");
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
    <div className="login-signup">
      <section className="credentials">
        <h1>Tasque</h1>
        <form>
          <div>
            <label> Username:</label>
            <input type="text" name="username" id="login-name" required></input>
          </div>
          <div>
            <label id="login-password-label"> Password:</label>
            <input
              type="password"
              name="password"
              id="login-password"
              required
            ></input>
          </div>
          <button className="submit" onClick={(e) => handleLogin(e, navigate)}>
            Log In
          </button>
          <p id="error-login"></p>
        </form>
        <Link to="/signup">Sign Up</Link>
      </section>
      <section className="tasque-boy">
        <img src={boy} alt="Boy writing in notepad" />
      </section>
    </div>
  );
}
export default Login;
