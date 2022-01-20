import React from "react";
import { Link } from "react-router-dom";

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
            id="name"
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
            required
            onChange={(e) => {
              checkValidInput(e);
            }}
          ></input>
          <p className="error" id="error-password"></p>
        </div>
        <button>Sign Up</button>
      </form>
      <Link to="/">Log In</Link>
    </>
  );
}

export default SignUp;
