import React from "react";
import { Link } from "react-router-dom";
import "./LoginSignup.css";
import boy from "../../images/boy.svg";

const axios = require("axios");

/**
 * Check if the input of the sign up form field is correct. If it's not, display an error
 * message.
 * @param {Event} e the event that triggers this function
 */
function checkValidInput(e) {
  let nameError = "Must contain alphabetic characters only";
  let userPassError =
    "Must be at least 8 characters long and only contain alphanumeric characters";
  let errorList = new Map();
  errorList.set("firstname", nameError);
  errorList.set("lastname", nameError);
  errorList.set("username", userPassError);
  errorList.set("password", userPassError);
  let tagName = e.target.getAttribute("name");
  let errorTag = document.getElementById(`error-${tagName}`);
  if (!e.target.validity.valid) {
    errorTag.classList.remove("hidden");
  } else {
    errorTag.classList.add("hidden");
  }
}

/**
 * Processes the user's request to create a new account, and will display a message
 * indicating if the signup was successfull or whether any errors occurred.
 * @param {Event} e The event that triggers this function
 */
function handleSubmit(e) {
  e.preventDefault();
  let firstnameTag = document.getElementById("first-name");
  let lastnameTag = document.getElementById("last-name");
  let usernameTag = document.getElementById("username");
  let passwordTag = document.getElementById("password");
  let errorTag = document.getElementById("error-submit");
  if (
    firstnameTag.validity.valid &&
    lastnameTag.validity.valid &&
    usernameTag.validity.valid &&
    passwordTag.validity.valid
  ) {
    axios
      .post("/signup", {
        firstname: firstnameTag.value,
        lastname: lastnameTag.value,
        username: usernameTag.value,
        password: passwordTag.value,
      })
      .then(() => {
        document.getElementById("error-submit").innerHTML =
          "Sign up successful. Please log in to continue.";
      })
      .catch((error) => {
        errorTag.innerHTML = error.response.data;
      });
  } else {
    errorTag.innerHTML = "Please check the validity of your input";
  }
}

function SignUp() {
  return (
    <div className="login-signup">
      <section className="credentials">
        <h1>Tasque</h1>
        <form id="signup-form">
          <div>
            <label> First Name:</label>
            <input
              type="text"
              name="firstname"
              pattern="[A-Za-z]*"
              id="first-name"
              required
              onChange={(e) => {
                checkValidInput(e);
              }}
            ></input>
            <p className="error hidden" id="error-firstname">
              Must contain alphabetic characters only
            </p>
          </div>
          <div>
            <label> Last Name:</label>
            <input
              type="text"
              name="lastname"
              pattern="[A-Za-z]*"
              id="last-name"
              required
              onChange={(e) => {
                checkValidInput(e);
              }}
            ></input>
            <p className="error hidden" id="error-lastname">
              Must contain alphabetic characters only
            </p>
          </div>
          <div>
            <label> Username:</label>
            <input
              type="text"
              name="username"
              minLength="8"
              pattern="[A-Za-z0-9]*"
              id="username"
              required
              onChange={(e) => {
                checkValidInput(e);
              }}
            ></input>
            <p className="error hidden" id="error-username">
              Must be at least 8 characters. Alphanumeric characters only.
            </p>
          </div>
          <div>
            <label> Password:</label>
            <input
              type="password"
              name="password"
              minLength="8"
              pattern="[A-Za-z0-9]*"
              id="password"
              autoComplete="new-password"
              required
              onChange={(e) => {
                checkValidInput(e);
              }}
            ></input>
            <p className="error hidden" id="error-password">
              Must be at least 8 characters. Alphanumeric characters only.
            </p>
          </div>
          <button className="submit" onClick={(e) => handleSubmit(e)}>
            Sign Up
          </button>
          <p className="error" id="error-submit"></p>
        </form>
        <Link to="/">Log In</Link>
      </section>
      <section className="tasque-boy">
        <img src={boy} alt="Boy writing in notepad" />
      </section>
    </div>
  );
}

export default SignUp;
