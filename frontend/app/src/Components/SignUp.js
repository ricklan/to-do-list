import React from "react";
import { Link } from "react-router-dom";

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
    errorTag.innerHTML = errorList.get(tagName);
  } else {
    errorTag.innerHTML = "";
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
      .post("http://127.0.0.1:5000/signup", {
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
    <>
      <h3>Sign Up</h3>
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
          <p className="error" id="error-firstname"></p>
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
          <p className="error" id="error-lastname"></p>
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
          <p className="error" id="error-username"></p>
        </div>
        <div>
          <label> Passsword:</label>
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
          <p className="error" id="error-password"></p>
        </div>
        <button onClick={(e) => handleSubmit(e)}>Sign Up</button>
        <p className="error" id="error-submit"></p>
      </form>
      <p id="success-msg"></p>
      <Link to="/">Log In</Link>
    </>
  );
}

export default SignUp;
